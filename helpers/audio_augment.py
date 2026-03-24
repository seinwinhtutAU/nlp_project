# La Min Oo 6540039
# Set Kaung Lwin 6632017
# Sein Win Htut  6611040
import librosa
import numpy as np
import os
import pandas as pd
import soundfile as sf


# Audio Augmentation to expand dataset

def mix(speech, noise_path, snr_db):
    noise = librosa.load(noise_path, sr=sample_rate, mono=True)[0]

    if len(noise) < len(speech):
        times_to_repeat = int(np.ceil(len(speech) / len(noise)))
        noise = np.tile(noise, times_to_repeat)

    start = rng.integers(0, len(noise) - len(speech) + 1)
    noise = noise[start: start + len(speech)]
    speech_power = np.mean(speech**2)           
    noise_power = np.mean(noise**2) + 1e-6      
    target_snr = 10 ** (snr_db / 10)            
    scale = np.sqrt(speech_power / noise_power / target_snr)
    mixed = speech + noise * scale
    
    return np.clip(mixed, -1.0, 1.0)

in_dir = "audio_files"
out_dir = "audio_files_augmented"
esc50 = "ESC-50/audio"
esc50_meta = "ESC-50/meta/esc50.csv"
sample_rate = 22050
times = 4


audio_files_meta = "metadata.csv"

df = pd.read_csv(audio_files_meta)

df = df[df["emotion"] != "neutral"]
samples = df.shape[0]
final = samples * times
print(f"Total original files: {samples}, Total final augmented files: {final}")

seed = 42

rng = np.random.default_rng(seed)

os.makedirs(out_dir, exist_ok=True)

esc50_categories = {
    "crowd":    ["laughing", "clapping", "footsteps", "coughing", "breathing"],
    "traffic":  ["car_horn", "engine", "airplane"],
    "rain":     ["rain", "thunderstorm", "water_drops", "sea_waves", "pouring_water"],
    "wind":     ["wind", "crackling_fire"],
    "keyboard": ["keyboard_typing", "mouse_click", "knocking"],
    "indoor":   ["clock_tick", "door_wood_knock", "washing_machine", "vacuum_cleaner"],
}

SNR_MAP = {
    "crowd": 15, "traffic": 10, "rain": 15,
    "wind": 10,  "keyboard": 15, "indoor": 15,
}

meta = pd.read_csv(esc50_meta)
noise_index = {}
for group, categories in esc50_categories.items():
    paths = meta[meta["category"].isin(categories)]["filename"].tolist()
    noise_index[group] = [os.path.join(esc50, f) for f in paths if os.path.isfile(os.path.join(esc50, f))]

new_rows = []

count = 0 

for _, row in df.iterrows():
    src_path = os.path.join(in_dir, row["file_name"] + ".wav")
    speech, _ = librosa.load(src_path, sr=sample_rate, mono=True)
    stem = row["file_name"]

    chosen_groups = rng.choice(list(noise_index.keys()), size=times, replace=False)

    for group in chosen_groups:
        noise_path = rng.choice(noise_index[group])
        y_aug      = mix(speech, noise_path, SNR_MAP[group])

        new_fname  = f"{stem}__{group}.wav"
        sf.write(os.path.join(out_dir, new_fname), y_aug, sample_rate)

        new_rows.append({**row.to_dict(), "file_name": new_fname, "augmentation": group})
        count += 1
        progress = int(count*100/final)
        if progress%25 == 0:
            print(f"Completed {count} files. {progress}% done.")

aug_df = pd.DataFrame(new_rows)
df["augmentation"] = "original"
full_df = pd.concat([df, aug_df], ignore_index=True)
full_df.to_csv("metadata_augmented.csv", index=False)