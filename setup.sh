#!/bin/bash

ZIP_FILE=./ravdess-audio.zip
DIR=audio_files

if [ -d "$DIR" ] && [ "$(ls -A $DIR)" ]; then
    echo "audio_files already exists and has files, skipping download."
else
    curl -L -o $ZIP_FILE https://www.kaggle.com/api/v1/datasets/download/uwrfkaggler/ravdess-emotional-speech-audio
    mkdir -p $DIR
    unzip $ZIP_FILE
    mv ./audio_speech_actors_01-24/*/* ./audio_files/
    rm -r ./Actor* ./audio_speech_actors_01-24
fi

git clone https://github.com/karolpiczak/ESC-50.git