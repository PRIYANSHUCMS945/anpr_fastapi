from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, LicensePlate
from schemas import LicensePlateOut
from yolo_detector import detect_plate
from ocr import extract_text_from_image
import shutil
import os

app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads/raw_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ocr", response_model=LicensePlateOut)
def process_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    plate_img_path = detect_plate(image_path)
    if not plate_img_path:
        plate_text = "No plate detected"
    else:
        plate_text = extract_text_from_image(plate_img_path)

    record = LicensePlate(image_name=file.filename, plate_text=plate_text)
    db.add(record)
    db.commit()
    db.refresh(record)

    return record
