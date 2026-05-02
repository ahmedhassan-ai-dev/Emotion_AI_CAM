import cv2
from datetime import datetime
from services.face_service import detect_faces, get_face_id
from services.emotion_service import predict_emotion
from utils.file_utils import save_face
from utils.db import save_to_db
from core.session import reset_data, session_start_time
from core.config import SESSION_DURATION


def run_webcam():
    cap = cv2.VideoCapture(0)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        frame_count += 1

        # reset session
        if (datetime.now() - session_start_time).seconds > SESSION_DURATION:
            reset_data()

        faces = detect_faces(frame)
        results = {}

        if frame_count % 10 == 0:
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]

                face_id = get_face_id(face)
                if face_id is None:
                    continue

                emotion = predict_emotion(face)

                save_face(face, emotion, face_id)
                save_to_db(face_id, emotion)

                results[face_id] = emotion

        # draw
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face_id = get_face_id(face)

            label = "Detecting..."
            if face_id in results:
                label = f"ID {face_id}: {results[face_id]}"
            elif face_id is not None:
                label = f"ID {face_id}"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow("Emotion AI Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
