import easyocr
import cv2
import os
import re
import csv
from datetime import datetime

# Initialize EasyOCR (CPU only)
reader = easyocr.Reader(['en'], gpu=False)

# Output CSV path
CSV_PATH = os.path.join("uploads", "outputs", "detected_plates.csv")


def clean_text(text: str) -> str:
    """Clean OCR text to remove unnecessary characters."""
    text = text.upper().strip()
    text = re.sub(r"[^A-Z0-9]", "", text)
    return text[:12]  # limit to 12 chars


def extract_text_from_image(image_path: str) -> str:
    """Extract number plate text from image, log with confidence and timestamp."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")

    results = reader.readtext(img)
    if not results:
        plate_text = "No text detected"
        avg_conf = 0.0
    else:
        # Combine all detected text pieces and average confidence
        combined_text = " ".join([res[1] for res in results])
        plate_text = clean_text(combined_text)
        avg_conf = sum([res[2] for res in results]) / len(results)

    # Ensure output directory exists
    output_dir = os.path.join("uploads", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Determine serial number (increment automatically)
    serial_no = 1
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, "r") as f:
            existing = list(csv.reader(f))
            serial_no = len(existing)  # continue numbering

    # Write or append data to CSV
    with open(CSV_PATH, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if serial_no == 1:  # Add header only for new file
            writer.writerow(["S.No", "Timestamp", "Plate Number", "Confidence", "Image Path"])
        writer.writerow([serial_no, timestamp, plate_text, f"{avg_conf:.3f}", image_path])

    print(f"[INFO] Entry saved: {serial_no} | Plate: {plate_text} | Conf: {avg_conf:.3f} | Time: {timestamp}")
    return plate_text
