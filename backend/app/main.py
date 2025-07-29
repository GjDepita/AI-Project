# backend/app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.yolov8_ocr import detect_serial_number

app = FastAPI()

# ✅ Allow Vue frontend (localhost:5173) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = detect_serial_number(image_bytes)
    return result
