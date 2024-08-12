import os
import cv2
import torch
import numpy as np

# Загрузка модели YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Функция для увеличения контрастности изображения
def increase_contrast(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Функция для обнаружения лиц на изображении
def detect_faces(image):
    results = model(image)
    faces = results.pandas().xyxy[0]
    faces = faces[faces['name'] == 'person']
    return faces

# Функция для обнаружения номеров автомобилей на изображении
def detect_car_plates(image):
    car_plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
    car_plates = car_plate_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return car_plates

# Функция для обработки изображения и удаления конфиденциальной информации
def process_image(input_path, output_path):
    img = cv2.imread(input_path)
    img = increase_contrast(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц и размытие
    faces = detect_faces(img)
    for _, row in faces.iterrows():
        x_min, y_min, x_max, y_max = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        face_img = img[y_min:y_max, x_min:x_max]
        face_gray = gray[y_min:y_max, x_min:x_max]
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        detected_faces = face_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (fx, fy, fw, fh) in detected_faces:
            img[y_min + fy:y_min + fy + fh, x_min + fx:x_min + fx + fw] = cv2.GaussianBlur(face_img[fy:fy + fh, fx:fx + fw], (99, 99), 30)

    # Обнаружение номеров автомобилей и размытие
    car_plates = detect_car_plates(gray)
    for (x, y, w, h) in car_plates:
        car_plate = img[y:y+h, x:x+w]
        blurred_car_plate = cv2.GaussianBlur(car_plate, (99, 99), 30)
        img[y:y+h, x:x+w] = blurred_car_plate

    # Сохранение результата в папку output
    output_image_path = os.path.join(output_path, os.path.basename(input_path))
    cv2.imwrite(output_image_path, img)

# Папки для ввода и вывода изображений
input_folder = 'input'
output_folder = 'output'

# Убедитесь, что папка вывода существует или создайте ее
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Обработка каждого изображения из папки ввода
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        input_image_path = os.path.join(input_folder, filename)
        process_image(input_image_path, output_folder)
