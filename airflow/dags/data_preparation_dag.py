from __future__ import annotations

import contextlib
import csv
import os
import wave
from datetime import datetime
from pathlib import Path

import librosa
import numpy as np
import pandas as pd
import soundfile as sf
from airflow import DAG
from airflow.operators.python import PythonOperator

# DAG file location: <repo>/airflow/dags/data_preparation_dag.py
# Repo root is two levels up from this file.
REPO_ROOT = Path(__file__).resolve().parents[2]


def get_duration_wave(file_path: Path) -> float:
    with contextlib.closing(wave.open(str(file_path), "r")) as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)


def run_metadata_creation() -> None:
    audio_dir = REPO_ROOT / "audio_files"
    output_csv = REPO_ROOT / "metadata.csv"

    header_row = ["file_name", "emotion", "intensity", "gender", "statement", "duration"]

    emotions = {
        "01": "neutral",
        "02": "calm",
        "03": "happy",
        "04": "sad",
        "05": "angry",
        "06": "fearful",
        "07": "disgust",
        "08": "surprised",
    }

    emotion_intensity = {
        "01": "normal",
        "02": "strong",
    }

    statements = {
        "01": "Kids are talking by the door",
        "02": "Dogs are sitting by the door",
    }

    rows: list[list[object]] = []

    for _, _, filenames in os.walk(audio_dir):
        if len(filenames) == 0:
            print("no file found")

        for filename in filenames:
            if filename.startswith("."):
                continue

            try:
                file_stem = Path(filename).stem
                identifiers = file_stem.split("-")
                emotion = emotions[identifiers[2]]
                intensity = emotion_intensity[identifiers[3]]
                statement = statements[identifiers[4]]

                repetition = int(identifiers[-2])
                if repetition == 2:
                    continue

                gender = "female" if int(identifiers[-1]) % 2 == 0 else "male"
                duration = get_duration_wave(audio_dir / filename)

                rows.append([file_stem, emotion, intensity, gender, statement, duration])
            except Exception as error:
                print(filename)
                print(error)

    with open(output_csv, "w", newline="") as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(header_row)
        csv_writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_csv}")


def run_audio_augmentation() -> None:
    in_dir = REPO_ROOT / "audio_files"
    out_dir = REPO_ROOT / "audio_files_augmented"
    esc50_audio_dir = REPO_ROOT / "ESC-50" / "audio"
    esc50_meta = REPO_ROOT / "ESC-50" / "meta" / "esc50.csv"
    audio_files_meta = REPO_ROOT / "metadata.csv"

    sample_rate = 22050
    times = 4
    seed = 42

    def mix(speech: np.ndarray, noise_path: Path, snr_db: int, rng: np.random.Generator) -> np.ndarray:
        noise = librosa.load(str(noise_path), sr=sample_rate, mono=True)[0]

        if len(noise) < len(speech):
            times_to_repeat = int(np.ceil(len(speech) / len(noise)))
            noise = np.tile(noise, times_to_repeat)

        start = rng.integers(0, len(noise) - len(speech) + 1)
        noise = noise[start : start + len(speech)]

        speech_power = np.mean(speech**2)
        noise_power = np.mean(noise**2) + 1e-6
        target_snr = 10 ** (snr_db / 10)
        scale = np.sqrt(speech_power / noise_power / target_snr)
        mixed = speech + noise * scale

        return np.clip(mixed, -1.0, 1.0)

    df = pd.read_csv(audio_files_meta)
    df = df[df["emotion"] != "neutral"]

    samples = df.shape[0]
    final = samples * times
    print(f"Total original files: {samples}, Total final augmented files: {final}")

    rng = np.random.default_rng(seed)

    os.makedirs(out_dir, exist_ok=True)

    esc50_categories = {
        "crowd": ["laughing", "clapping", "footsteps", "coughing", "breathing"],
        "traffic": ["car_horn", "engine", "airplane"],
        "rain": ["rain", "thunderstorm", "water_drops", "sea_waves", "pouring_water"],
        "wind": ["wind", "crackling_fire"],
        "keyboard": ["keyboard_typing", "mouse_click", "knocking"],
        "indoor": ["clock_tick", "door_wood_knock", "washing_machine", "vacuum_cleaner"],
    }

    snr_map = {
        "crowd": 15,
        "traffic": 10,
        "rain": 15,
        "wind": 10,
        "keyboard": 15,
        "indoor": 15,
    }

    meta = pd.read_csv(esc50_meta)
    noise_index: dict[str, list[Path]] = {}

    for group, categories in esc50_categories.items():
        paths = meta[meta["category"].isin(categories)]["filename"].tolist()
        noise_index[group] = [
            esc50_audio_dir / filename
            for filename in paths
            if os.path.isfile(esc50_audio_dir / filename)
        ]

    new_rows: list[dict[str, object]] = []
    count = 0

    for _, row in df.iterrows():
        src_path = in_dir / f"{row['file_name']}.wav"
        speech, _ = librosa.load(str(src_path), sr=sample_rate, mono=True)
        stem = row["file_name"]

        chosen_groups = rng.choice(list(noise_index.keys()), size=times, replace=False)

        for group in chosen_groups:
            noise_path = Path(rng.choice(noise_index[group]))
            y_aug = mix(speech, noise_path, snr_map[group], rng)

            new_fname = f"{stem}__{group}.wav"
            sf.write(str(out_dir / new_fname), y_aug, sample_rate)

            new_rows.append({**row.to_dict(), "file_name": new_fname, "augmentation": group})
            count += 1
            progress = int(count * 100 / final) if final else 100
            if progress % 25 == 0:
                print(f"Completed {count} files. {progress}% done.")

    aug_df = pd.DataFrame(new_rows)
    df["augmentation"] = "original"
    full_df = pd.concat([df, aug_df], ignore_index=True)
    output_csv = REPO_ROOT / "metadata_augmented.csv"
    full_df.to_csv(output_csv, index=False)

    print(f"Wrote {len(full_df)} rows to {output_csv}")


default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="prepare_audio_training_data",
    description="Prepare metadata and augmented audio before ML training",
    default_args=default_args,
    start_date=datetime(2026, 3, 17),
    schedule=None,
    catchup=False,
    tags=["data-prep", "ml-training"],
) as dag:
    metadata_creation_task = PythonOperator(
        task_id="create_metadata_csv",
        python_callable=run_metadata_creation,
    )

    audio_augmentation_task = PythonOperator(
        task_id="augment_audio_and_metadata",
        python_callable=run_audio_augmentation,
    )

    metadata_creation_task >> audio_augmentation_task
