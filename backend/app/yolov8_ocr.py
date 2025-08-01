# app/yolov8_ocr.py

import easyocr
import numpy as np
from PIL import Image
import io
import re

# Initialize EasyOCR with detection enabled
ocr_reader = easyocr.Reader(["en"], detector=True)

# Clean + validate logic
def clean_text(text: str) -> str:
    return text.strip().replace(" ", "").upper()

def is_valid_serial(text: str) -> bool:
    if len(text) < 6:
        return False
    if not re.search(r'[A-Z]', text):
        return False
    if not re.search(r'[0-9]', text):
        return False
    junk_words = ["FC", "PATP", "ROHS", "CE", "CHINA"]
    return text not in junk_words

# 🎯 This is the function your FastAPI app imports
def detect_serial_number(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_np = np.array(image)

        ocr_results = ocr_reader.readtext(img_np)

        serials = []
        raw_ocr = []

        for _, text, _ in ocr_results:
            cleaned = clean_text(text)
            raw_ocr.append(cleaned)
            if is_valid_serial(cleaned):
                serials.append(cleaned)

        return {
            "serials": serials,
            "raw_ocr": raw_ocr
        }

    except Exception as e:
        return {
            "serials": [],
            "raw_ocr": [],
            "error": str(e)
        }
