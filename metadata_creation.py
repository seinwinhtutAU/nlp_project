import csv,os, wave, contextlib
from pathlib import Path


def get_duration_wave(file_path):
    with contextlib.closing(wave.open(file_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


dir = "audio_files"


header_row = ["file_name","emotion","intensity","gender","statement","duration"]

emotions = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}

emotion_intensity = {
    "01": "normal",
    "02": "strong",
}

statements = {
    "01":"Kids are talking by the door", 
    "02": "Dogs are sitting by the door",
}

with open("metadata.csv","w",newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(header_row)
    rows = []
    for _,_, filenames in os.walk(dir):
        for f in filenames:
            filename = Path(f).stem
            identifiers = filename.split("-")
            emotion = emotions[identifiers[2]]
            intensity = emotion_intensity[identifiers[3]]
            statement = statements[identifiers[4]]
            gender = ""
            if int(identifiers[-1]) % 2 == 0:
                gender = "female"
            else:
                gender = "male"
            duration = get_duration_wave(f"audio_files/{f}")
            
            rows.append([filename,emotion,intensity,gender,statement,duration])
    
    csv_writer.writerows(rows)
            
            
            
