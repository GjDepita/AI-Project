from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from easyocr import Reader
from io import BytesIO
from PIL import Image
import numpy as np
import re
import cv2

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize EasyOCR reader
reader = Reader(['en'], gpu=False)

# === Utility Functions ===

def clean_text(text: str) -> str:
    return text.strip().replace(" ", "").upper()

def is_valid_serial(text: str) -> bool:
    if len(text) < 6:
        return False
    if not re.search(r'[A-Z]', text):
        return False
    if not re.search(r'[0-9]', text):
        return False
    junk_words = ["FC", "PATP", "ROHS", "CE", "CHINA", "QR", "SERIAL", "LOGO"]
    return text not in junk_words

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# === Endpoint ===

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    image_np = np.array(image)

    processed = preprocess_image(image_np)
    ocr_result = reader.readtext(processed)

    raw_ocr = []
    serials = []

    for _, text, conf in ocr_result:
        cleaned = clean_text(text)
        raw_ocr.append({
            "text": cleaned,
            "confidence": round(conf, 2)
        })

        if conf >= 0.5 and is_valid_serial(cleaned):
            serials.append(cleaned)

    return {
        "serials": serials,
        "raw_ocr": raw_ocr
    }
