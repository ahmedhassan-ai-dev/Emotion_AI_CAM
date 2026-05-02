from datetime import datetime
import os
import csv
from core.config import CSV_FILE, SAVE_DIR, FACE_DIR
from services.face_service import reset_faces_memory

session_start_time = datetime.now()

def reset_data():
    global session_start_time

    with open(CSV_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["time", "face_id", "emotion"])

    for folder in [SAVE_DIR, FACE_DIR]:
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))

    reset_faces_memory()  # مهم

    session_start_time = datetime.now()
