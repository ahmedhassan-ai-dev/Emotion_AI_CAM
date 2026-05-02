from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import cv2
import torch

model_name = "mo-thecreator/vit-Facial-Expression-Recognition"

processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)


def predict_emotion(face_img):
    image = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    class_id = outputs.logits.argmax(-1).item()
    return model.config.id2label[class_id]
