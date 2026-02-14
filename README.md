# Emotion Detection of Speech Audio Files

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

### 2. Installing Python Dependencies

For installing Python dependencies, it is recommended to use a virtual environment. Take a look at the Python documentation [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html).

Alternatively, you can use Python dependencies managers like [uv](https://github.com/astral-sh/uv) or [poetry](https://python-poetry.org/).
