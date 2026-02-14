# Emotion Detection of Speech Audio Files

## Description

## How to Run

### 1. Getting the Dataset

Download the [RAVDESS Emotional speech audio](https://www.kaggle.com/datasets/uwrfkaggler/ravdess-emotional-speech-audio) dataset running the following command in CLI:

```bash
curl -L -o ./ravdess-emotional-speech-audio.zip\ https://www.kaggle.com/api/v1/datasets/download/uwrfkaggler/ravdess-emotional-speech-audio
```

After unzipping, delete folders starting with 'Actor' and make a folder called `audio_files`. Then run the following command:

```bash
mv ./audio_speech_actors_01-24/*/* ./audio_files/
```

If successful, there will be 1440 wave files in the `audio_files` directory.

After that, there is a file called `metadata_creation.py`. Although there is a `metadata.csv`, the python file is included in case some features are needed. In that case, the python file can be modified minimally to extract
additional metadata.

### 2. Installing Python Dependencies

For installing Python dependencies, it is recommended to use a virtual environment. Take a look at the Python documentation [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html).

Alternatively, you can use Python dependencies managers like [uv](https://github.com/astral-sh/uv) or [poetry](https://python-poetry.org/).

### File names explanation

The filename consists of a 7-part numerical identifier (e.g., 03-01-06-01-02-01-12.wav).

Filename identifiers

- Modality (01 = full-AV, 02 = video-only, 03 = audio-only).
- Vocal channel (01 = speech, 02 = song).
- Emotion (01 = neutral, 02 = calm, 03 = happy, 04 = sad, 05 = angry, 06 = fearful, 07 = disgust, 08 = surprised).
- Emotional intensity (01 = normal, 02 = strong). NOTE: There is no strong intensity for the 'neutral' emotion.
- Statement (01 = "Kids are talking by the door", 02 = "Dogs are sitting by the door").
- Repetition (01 = 1st repetition, 02 = 2nd repetition).
- Actor (01 to 24. Odd numbered actors are male, even numbered actors are female).
