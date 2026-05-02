from flask import Blueprint, request
import cv2
import numpy as np
from utils.file_utils import save_frame
from services.face_service import detect_faces
from services.emotion_service import predict_emotion

api = Blueprint("api", __name__)

@api.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']

    npimg = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    save_frame(frame)

    faces = detect_faces(frame)
    data = []

    for i, (x, y, w, h) in enumerate(faces):
        face = frame[y:y+h, x:x+w]
        emotion = predict_emotion(face)

        data.append({
            "face_id": i,
            "emotion": emotion
        })

    return {"status": "ok", "data": data}
