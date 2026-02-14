import csv,os
from pathlib import Path

dir = "audio_files"


header_row = ["file_name","emotion","intensity","gender","statement"]

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
            
            rows.append([filename,emotion,intensity,gender,statement])
    
    csv_writer.writerows(rows)
            
            
            
