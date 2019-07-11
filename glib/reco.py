import os
import cv2
from PIL import Image
import numpy as np
import pickle
import json


def prepare_dir(name):
    try:
        name = name.replace(' ', '_').lower()
        save_to = '../data/' + name
        os.mkdir(save_to)
    except FileExistsError:
        pass
    return name


def gscan(name, count=100):
    name = str(prepare_dir(name))
    cascade = cv2.CascadeClassifier('../classifiers/face.xml')
    cap = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, 6)
        detection = cascade.detectMultiScale(gray_frame, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in detection:
            img_location = '../data/' + name + '/' + str(i) + '.png'
            cv2.imwrite(img_location, gray_frame)
            i += 1
            scan_indicator_color = (255, 0, 0)
            stroke = 1
            end_coord_x = x + w
            end_coord_y = y + h
            cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), scan_indicator_color, stroke)
        cv2.imshow('Scanning...', frame)
        if cv2.waitKey(20) & i == count:
            break
    cap.release()
    cv2.destroyAllWindows()


def gtrain():
    cascade = cv2.CascadeClassifier('../classifiers/face.xml')
    lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
    name_id = 0  # label_id
    train_data = []  # x_train
    names = []  # y_labels
    id_names = {}  # label_dict
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../data')
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                path = os.path.join(root, file)
                name = os.path.basename(root)  # label
                if name in id_names:
                    pass
                else:
                    id_names[name] = name_id
                    name_id += 1
                id_ = id_names[name]
                pil_image = Image.open(path)
                np_image_array = np.array(pil_image, 'uint8')
                detection = cascade.detectMultiScale(np_image_array, scaleFactor=1.5, minNeighbors=5)
                for (x, y, w, h) in detection:
                    region_of_interest = np_image_array[y: y + h, x: x + w]
                    train_data.append(region_of_interest)
                    names.append(id_)
    with open('../config/total.bin', 'w') as file:
        file.write(str(len(id_names)))
    with open('../config/names.bin', 'w') as file:
        file.write(str({v: k for k, v in id_names.items()}))
    with open('../serve/names.json', 'w') as file:
        name_list = []
        for name in id_names:
            name_list.append(name)
        name_json = json.dumps(str(name_list).replace("'", '"'))
        file.write(name_json)
        pass
    with open('../config/data_binary.bin', 'wb') as file:
        pickle.dump(id_names, file)
    lbph_recognizer.train(train_data, np.array(names))
    lbph_recognizer.save('../models/net_model.yml')


def gdetect():
    name_id = -1
    cascade = cv2.CascadeClassifier('../classifiers/face.xml')
    lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
    lbph_recognizer.read('../models/net_model.yml')
    with open('../config/data_binary.bin', 'rb') as file:
        label_dict = pickle.load(file)
        students = {v: k for k, v in label_dict.items()}
    with open('../config/total.bin', 'r') as file:
        total = int(file.read())
    report = []
    for i in range(total):
        report.append('Absent')
    print(report)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        detection = cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        gray_frame = cv2.cvtColor(frame, 6)
        for (x, y, w, h) in detection:
            region_of_interest = gray_frame[y:y + h, x:x + w]
            name_id, confidence = lbph_recognizer.predict(region_of_interest)
            if 45 <= confidence:
                name = students[name_id]
                report[name_id] = 'Present'
                cv2.putText(frame, name, (x, y), 3, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.imshow('Taking Attendance....', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            # print(students[name_id])
            with open('../serve/report.json', 'w') as file:
                file.write(json.dumps(str(report).replace("'", '"')))
            break
