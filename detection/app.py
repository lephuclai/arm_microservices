import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson import ObjectId 
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# default_mongo_uri = "mongodb://172.16.42.11:27017/detection"
# app.config["MONGO_URI"] = os.getenv("MONGO_URI", default_mongo_uri)

app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE'] + '?authSource=admin'

mongo = PyMongo(app)
db = mongo.db

INPUT_MODEL_WEIGHTS = "/conf/yolov3-tiny.weights"
INPUT_MODEL_CONFIG = "/conf/yolov3-tiny.cfg"
INPUT_MODEL_CLASSES = "/conf/yolov3-tiny.txt"

# INPUT_MODEL_WEIGHTS = "/home/kien/arm-tiny-yolo/yolov3-tiny.weights"
# INPUT_MODEL_CONFIG = "/home/kien/arm-tiny-yolo/yolov3-tiny.cfg"
# INPUT_MODEL_CLASSES = "/home/kien/arm-tiny-yolo/yolov3-tiny.txt"

ROOT_DIR = os.path.abspath("/")
MODEL_WEIGHTS_PATH = os.path.join(ROOT_DIR, INPUT_MODEL_WEIGHTS)
MODEL_CONFIG_PATH = os.path.join(ROOT_DIR, INPUT_MODEL_CONFIG)
MODEL_CLASSES_PATH = os.path.join(ROOT_DIR, INPUT_MODEL_CLASSES)

with open(MODEL_CLASSES_PATH, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

np.random.seed(42)
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNet(MODEL_WEIGHTS_PATH, MODEL_CONFIG_PATH)

def get_output_layers(net):
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        return output_layers

@app.route('/process', methods=['POST','PUT'])
def upload_file():
        file = request.files['image_file']

        image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        Width = image.shape[1]
        Height = image.shape[0]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416,416), (0,0,0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.4
        nms_threshold = 0.3

        for out in outs:
                for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        if confidence > conf_threshold :
                                class_ids.append(class_id)
                                confidences.append(float(confidence))

        output = ""
        for i in range(0,len(class_ids)):
                output = output + "Class: " + classes[class_ids[i]] + " with confidence: " + str(confidences[i]) + "\n"
                db.object.insert_one({ "Name":classes[class_ids[i]], "Confidence":confidences[i], "DateTime":datetime.datetime.now()})

        return output

@app.route('/video', methods=['POST','PUT'])
def video_detect():
        file = request.files['video_file']

        video_path = os.path.join('/tmp', file.filename)
        file.save(video_path)

        cap = cv2.VideoCapture(video_path)

        output = ""

        while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                        break

                # cv2.imwrite("/tmp/frame.jpg", frame)
                # image = cv2.imread("frame.jpg", cv2.IMREAD_UNCHANGED)

                image = frame

                Width = image.shape[1]
                Height = image.shape[0]

                blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416,416), (0,0,0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(get_output_layers(net))

                class_ids = []
                confidences = []
                boxes = []
                conf_threshold = 0.4
                nms_threshold = 0.3

                for out in outs:
                        for detection in out:
                                scores = detection[5:]
                                class_id = np.argmax(scores)
                                confidence = scores[class_id]
                                if confidence > conf_threshold :
                                        class_ids.append(class_id)
                                        confidences.append(float(confidence))

                for i in range(0,len(class_ids)):
                        output = output + "Class: " + classes[class_ids[i]] + " with confidence: " + str(confidences[i]) + "\n"
                        db.object.insert_one({ "Name":classes[class_ids[i]], "Confidence":confidences[i], "DateTime":datetime.datetime.now()})

        cap.release()
        os.remove(video_path)

        return output

if __name__ == '__main__':
        app.run()
