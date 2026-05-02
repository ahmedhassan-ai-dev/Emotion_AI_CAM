import cv2
import face_recognition
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

known_encodings = []
known_ids = []
next_id = 0


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.1, 5)


def get_face_id(face_img):
    global next_id

    rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)

    if len(encodings) == 0:
        return None

    current_encoding = encodings[0]

    for i, known_encoding in enumerate(known_encodings):
        distance = np.linalg.norm(known_encoding - current_encoding)

        if distance < 0.6:
            return known_ids[i]

    # new person
    known_encodings.append(current_encoding)
    known_ids.append(next_id)

    next_id += 1
    return known_ids[-1]


def reset_faces_memory():
    global known_encodings, known_ids, next_id
    known_encodings.clear()
    known_ids.clear()
    next_id = 0
