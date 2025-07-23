import easyocr
import cv2
import numpy as np

import torch
from torch.serialization import add_safe_globals
import torch.nn.modules.container as container
import torch.nn.modules.conv as torch_conv
import ultralytics.nn.tasks as tasks
import ultralytics.nn.modules.conv as ultra_conv
import torch.nn.modules.batchnorm as batchnorm

# Allowlist required classes/functions for model unpickling
add_safe_globals([
    tasks.DetectionModel,
    container.Sequential,
    ultra_conv.Conv,
    torch_conv.Conv2d,
    batchnorm.BatchNorm2d,
])

from ultralytics import YOLO

model = YOLO("weights/best.pt")
reader = easyocr.Reader(['en'])

def detect_serial_number(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    results = model.predict(img)[0]

    serials = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        roi = img[y1:y2, x1:x2]
        ocr_result = reader.readtext(roi)
        text = ' '.join([r[1] for r in ocr_result])
        serials.append({
            "box": [x1, y1, x2, y2],
            "text": text
        })

    return serials