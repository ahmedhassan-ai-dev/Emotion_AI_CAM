import os

BASE_DIR = "data"
SAVE_DIR = os.path.join(BASE_DIR, "images")
FACE_DIR = os.path.join(BASE_DIR, "faces")
CSV_FILE = os.path.join(BASE_DIR, "emotions_log.csv")

SESSION_DURATION = 60

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(FACE_DIR, exist_ok=True)
