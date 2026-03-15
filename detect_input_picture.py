import cv2
from ultralytics import YOLO
from read_LP import *  # Import hàm đọc biển số
import os  # Import the os module for path manipulation
from flask import url_for

def preprocess_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    l_clahe = clahe.apply(l)
    enhanced = cv2.merge((l_clahe, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

# Cấu hình YOLO models
model_cars = YOLO('Model_detect_xe/yolo11n.pt')  # Mô hình phát hiện xe
model_plates = YOLO('Model_DetectorLP/LP_detect_ver2.pt')  # Mô hình phát hiện biển số

def process_license_plate(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")

        scale_factor = 5  # Hệ số phóng to ảnh được cắt

        results_cars = model_cars(image, classes=[2, 3, 5, 7], iou=0.5, conf=0.2)

        # Lặp qua từng vùng phát hiện xe
        for result in results_cars:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])
                cropped_vehicle = image[y1:y2, x1:x2]

                # Phát hiện biển số trong vùng xe
                results_plates = model_plates(cropped_vehicle, conf=0.5, iou=0.652)

                for plate_result in results_plates:
                    for plate_box in plate_result.boxes.xyxy:
                        px1, py1, px2, py2 = map(int, plate_box[:4])
                        cropped_plate = cropped_vehicle[py1:py2, px1:px2]

                        # Xử lý ảnh trước khi đọc biển số
                        resized_plate = cv2.resize(cropped_plate, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
                        final_plate = preprocess_image(resized_plate)

                        # Đọc biển số
                        kq = read_LP(final_plate)

                        # Vẽ kết quả lên ảnh gốc
                        cv2.rectangle(image, (x1 + px1, y1 + py1), (x1 + px2, y1 + py2), (0, 255, 0), 1)
                        cv2.putText(image, kq, (x1 + px1, y1 + py1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

        # Tạo thư mục 'static/uploads' nếu nó không tồn tại
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        # Lưu ảnh sau khi xử lý  (Using os.path.join for safer path construction)
        processed_image_path = os.path.join(upload_folder, 'processed_' + os.path.basename(image_path))
        cv2.imwrite(processed_image_path, image)

        # Trả về đường dẫn hợp lệ để truy cập ảnh đã xử lý
        return processed_image_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # or raise the exception if you prefer to stop execution
