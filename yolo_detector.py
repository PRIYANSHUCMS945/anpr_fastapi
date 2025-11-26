from ultralytics import YOLO
import cv2
import os

model_path = "models/best.pt"
model = YOLO(model_path)

def detect_plate(image_path, output_folder="uploads/processed_images"):
    os.makedirs(output_folder, exist_ok=True)
    results = model.predict(image_path, save=False, conf=0.5)
    boxes = results[0].boxes.xyxy.cpu().numpy()

    img = cv2.imread(image_path)
    plate_img_path = None

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box[:4])
        cropped = img[y1:y2, x1:x2]
        plate_img_path = os.path.join(output_folder, f"plate_{i}.jpg")
        cv2.imwrite(plate_img_path, cropped)

    return plate_img_path
