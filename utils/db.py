import csv
from datetime import datetime
from core.config import CSV_FILE

def init_db():
    try:
        open(CSV_FILE, 'x').close()
    except:
        return

    with open(CSV_FILE, 'w', newline='') as f:
        csv.writer(f).writerow(["time", "face_id", "emotion"])


def save_to_db(face_id, emotion):
    with open(CSV_FILE, 'a', newline='') as f:
        csv.writer(f).writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            face_id,
            emotion
        ])

