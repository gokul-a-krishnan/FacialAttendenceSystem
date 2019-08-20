import json
import os
import pickle
from datetime import datetime

import cv2
import numpy as np
from PIL import Image

from FaceRecognizer import api_path


def prepare_dir(name):  # Creates Directory to store Scanned Data
    try:
        name = name.replace(' ', '_').lower()
        save_to = api_path.image_path + name
        os.mkdir(save_to)
    except FileExistsError:
        pass
    return name


def scan(name, count=100):
    name = str(prepare_dir(name))
    cascade = cv2.CascadeClassifier(api_path.classifier_path + api_path.classifiers['face'])  # Specify the Classifier
    cap = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, 6)
        detection = cascade.detectMultiScale(gray_frame, scaleFactor=1.5,
                                             minNeighbors=5)  # Specify the Region of Interest
        for (x, y, w, h) in detection:  # Getting Co-Ordinates of ROI
            img_location = api_path.image_path + name + '/' + str(i) + '.png'
            cv2.imwrite(img_location, gray_frame)
            i += 1
            scan_indicator_color = (255, 0, 0)
            stroke = 1
            end_coord_x = x + w
            end_coord_y = y + h
            cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), scan_indicator_color, stroke)
        cv2.imshow('Scanning...', frame)
        if cv2.waitKey(20) & i == count:
            cap.release()
            cv2.destroyAllWindows()
            break


def train():
    cascade = cv2.CascadeClassifier(api_path.classifier_path + api_path.classifiers['face'])
    lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
    name_id = 0  # label_id
    train_data = []  # x_train
    names = []  # y_labels
    id_names = {}  # label_dict
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, api_path.image_path)
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
    with open(api_path.total_bin, 'wb') as file:
        file.write(bytes([len(id_names)]))
    with open(api_path.names_json, 'w') as file:
        name_list = []
        for name in id_names:
            name_list.append(name)
        name_json = json.dumps(str(name_list).replace("'", '"'))
        file.write(name_json)
        pass
    with open(api_path.data_bin, 'wb') as file:
        pickle.dump(id_names, file)
    lbph_recognizer.train(train_data, np.array(names))
    lbph_recognizer.save(api_path.model_path)


def current_time():
    g_current_time = datetime.now().strftime("%I:%M %p")
    return g_current_time


def detect():
    cascade = cv2.CascadeClassifier(api_path.classifier_path + api_path.classifiers['face'])
    lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
    lbph_recognizer.read(api_path.model_path)
    with open(api_path.data_bin, 'rb') as file:
        label_dict = pickle.load(file)
        students = {v: k for k, v in label_dict.items()}
    with open(api_path.total_bin, 'rb') as file:
        total = int.from_bytes(file.read(), byteorder='little')
    report = []
    in_time = []
    g_out_time = []
    for i in range(total):
        report.append('Absent')
        in_time.append('----')
        g_out_time.append('----')
    with open(api_path.out_time_json, 'w') as file:
        file.write(json.dumps(str(g_out_time).replace("'", '"')))
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
                in_time[name_id] = current_time()
                cv2.putText(frame, name, (x, y), 3, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.imshow('Taking Attendance....', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            with open(api_path.report_json, 'w') as file:
                file.write(json.dumps(str(report).replace("'", '"')))
            with open(api_path.in_time_json, 'w') as file:
                file.write(json.dumps(str(in_time).replace("'", '"')))
            break


def out_time():
    cascade = cv2.CascadeClassifier(api_path.classifier_path + api_path.classifiers['face'])
    lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
    lbph_recognizer.read(api_path.model_path)
    with open(api_path.data_bin, 'rb') as file:
        label_dict = pickle.load(file)
        students = {v: k for k, v in label_dict.items()}
    with open(api_path.total_bin, 'rb') as file:
        total = int.from_bytes(file.read(), byteorder='little')
    g_out_time = []
    for i in range(total):
        g_out_time.append('----')
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
                g_out_time[name_id] = current_time()
                cv2.putText(frame, name, (x, y), 3, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
        cv2.imshow('Recording...', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            with open(api_path.out_time_json, 'w') as file:
                file.write(json.dumps(str(g_out_time).replace("'", '"')))
            break
