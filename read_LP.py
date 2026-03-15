from ultralytics import YOLO
import cv2
import numpy as np

# Load mô hình YOLO
model = YOLO('Model_ReaderLP/LP_reader_ver4.pt')

def format_license_plate(license_plate_text):
    """
    Định dạng biển số Việt Nam với dấu gạch ngang (-)
    """
    if len(license_plate_text) <= 2:
        return license_plate_text  # Nếu chuỗi quá ngắn, không chỉnh sửa

    # Tìm vị trí đầu tiên xuất hiện chữ cái (phần mã tỉnh)
    for i, char in enumerate(license_plate_text):
        if char.isalpha():
            break

    # Chèn dấu '-' ngay sau phần mã tỉnh
    formatted_text = license_plate_text[:i+1] + '-' + license_plate_text[i+1:]
    return formatted_text



def read_LP(image_processed):
    results = model(image_processed, conf = 0.2)
    for result in results:
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            detections = []
            for box in boxes:
                x1, y1, x2, y2, confidence, class_index = box.data.cpu().numpy()[0]
                license_text = model.names[int(class_index)]  # Lấy ký tự
                detections.append(((x1, y1, x2, y2), license_text))

            # Sắp xếp các ký tự theo y trước (trục dọc), sau đó theo x (trục ngang)
            detections.sort(key=lambda x: (x[0][1], x[0][0]))

            # Phân chia các ký tự thành các dòng dựa trên khoảng cách y
            lines = []
            current_line = []
            mean_y = detections[0][0][1]  # y1 của bounding box đầu tiên
            for detection in detections:
                y_center = (detection[0][1] + detection[0][3]) / 2  # Tính trung tâm y của bounding box
                if abs(y_center - mean_y) < (detection[0][3] - detection[0][1]) * 1.5:
                    current_line.append(detection)
                else:
                    lines.append(current_line)
                    current_line = [detection]
                    mean_y = y_center
            lines.append(current_line)  # Thêm dòng cuối cùng

            # Sắp xếp lại từng dòng theo x (trục ngang)
            for line in lines:
                line.sort(key=lambda x: x[0][0])

            # Phân biệt loại biển số 1 dòng và 2 dòng
            if len(lines) == 1:
                # Biển số loại 1 dòng
                raw_text = "".join([text for _, text in lines[0]])
                license_plate_text = format_license_plate(raw_text)
            elif len(lines) == 2:
                # Biển số loại 2 dòng
                top_line = "".join([text for _, text in lines[0]])
                bottom_line = "".join([text for _, text in lines[1]])
                license_plate_text = f"{top_line}-{bottom_line}"

            else:
                # Nếu có hơn 2 dòng (không hợp lệ), trả về None
                return None

            return license_plate_text

    return None  # Trả về None nếu không phát hiện được biển số
