import cv2
import os
import csv
import re
from datetime import datetime
from paddleocr import PaddleOCR

# Initialize OCR model (CPU)
ocr_model = PaddleOCR(lang='en')

# CSV output file
CSV_PATH = os.path.join("uploads", "outputs", "detected_plates.csv")


def clean_text(text: str) -> str:
    """Clean OCR result string."""
    text = text.upper().strip()
    text = re.sub(r"[^A-Z0-9]", "", text)  # Allow only letters + digits
    return text[:12]  # Max plate size


def extract_text_from_image(image_path: str) -> str:
    """Run OCR on cropped number plate and store logs."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    # Run OCR
    results = ocr_model.ocr(img, cls=False)

    if not results:
        plate_text = "NOTEXT"
        avg_conf = 0.0
    else:
        all_text = []
        confs = []

        # Flatten results
        for line in results:
            for item in line:              # item = [box, (text, conf)]
                text, conf = item[1]
                all_text.append(text)
                confs.append(conf)

        combined = " ".join(all_text)
        plate_text = clean_text(combined)
        avg_conf = sum(confs) / len(confs) if confs else 0.0

    # Ensure output folder exists
    os.makedirs(os.path.join("uploads", "outputs"), exist_ok=True)

    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Serial number (auto increment)
    serial_no = 1
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, "r") as f:
            serial_no = len(list(csv.reader(f)))

    # Write CSV
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if serial_no == 1:  # First time → add header
            writer.writerow(["S.No", "Timestamp", "Plate Number", "Confidence", "Image Path"])
        writer.writerow([serial_no, timestamp, plate_text, f"{avg_conf:.3f}", image_path])

    print(f"[OCR] #{serial_no} | {plate_text} | conf={avg_conf:.3f} | {timestamp}")
    return plate_text
