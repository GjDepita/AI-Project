from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.yolov8_ocr import detect_serial_number

app = FastAPI()

# Allow Vue dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    serials = detect_serial_number(image_bytes)
    return {"serials": serials}

@app.get("/test")
def test():
    return {"status": "backend OK"}