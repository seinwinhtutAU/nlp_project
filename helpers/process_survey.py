with open("survey_results.csv") as f:
    data = f.read()
    rows = ["File,AudioID,Emotion,Intensity,Gender\n"]
    for x in data.splitlines():
        values = x.split(",")
        rows.append(f"{",".join(values[2:7])}\n")
    
with open("survey_cleaned.csv","w") as out:
    out.writelines(rows)