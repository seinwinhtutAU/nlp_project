#!/bin/bash

ZIP_FILE=./ravdess-audio.zip
DIR=audio_files

curl -L -o $ZIP_FILE https://www.kaggle.com/api/v1/datasets/download/uwrfkaggler/ravdess-emotional-speech-audio
mkdir $DIR
unzip $ZIP_FILE
mv ./audio_speech_actors_01-24/*/* ./audio_files/
rm -r Actor* /audio_speech_actors_01-24