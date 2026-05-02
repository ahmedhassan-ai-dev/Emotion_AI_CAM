import cv2
import os
from datetime import datetime
from core.config import SAVE_DIR, FACE_DIR

def save_frame(frame):
    name = datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
    cv2.imwrite(os.path.join(SAVE_DIR, name), frame)


def save_face(face, emotion, face_id):
    name = f"{datetime.now().strftime('%H%M%S')}_{face_id}_{emotion}.jpg"
    cv2.imwrite(os.path.join(FACE_DIR, name), face)
