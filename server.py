import io
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
print("Model loaded.")

def create_summary(detections):
    if not detections:
        return "I could not find any objects."
    labels = [f"a {d['label']}" for d in detections]
    if len(labels) == 1:
        return f"I see {labels[0]}."
    elif len(labels) == 2:
        return f"I see {labels[0]} and {labels[1]}."
    else:
        return f"I see {', '.join(labels[:-1])}, and {labels[-1]}."

def handle_image(img_bytes):
    #bytes -> OpenCV image
    arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        return "Invalid image data."

    results = model(frame, conf=0.45)
    detections = []
    for box in results[0].boxes:
        label = model.names[int(box.cls)]
        confidence = round(box.conf.item() * 100)
        detections.append({'label': label, 'confidence': confidence})

    print(f"Detected: {', '.join([d['label'] for d in detections]) or 'nothing'}")
    return create_summary(detections)

print('server up')

while True:

    img_len = int(input('len> '))
    img_bytes = bytes.fromhex(input('data> '))

    summary = handle_image(img_bytes)
    print(summary)
