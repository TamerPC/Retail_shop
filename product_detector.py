import torch
import cv2
import matplotlib.pyplot as plt
from collections import Counter

class ProductDetector():
    yolo = torch.hub.load("ultralytics/yolov5", "custom", path="runs/train/exp/weights/best.pt") #init Model yolov5

    def get_detections(self, img):
        return self.yolo(img).pandas().xyxy[0].to_dict('records')

    def draw_boxes(self, frame, detections):
        for detection in detections:
            cv2.putText(frame, detection['name'], (int(detection['xmin']), int(detection['ymin'])+15), 1, 0.7, (255,255,255), 1)
            cv2.rectangle(frame,(int(detection['xmin']), int(detection['ymin'])), (int(detection['xmax']), int(detection['ymax'])), (0,255,0), 2)

    def run_product_detection(self, frame):
        x_sh=int(frame.shape[1]/6)
        y_sh=int(frame.shape[0]/6)
        cv2.rectangle(frame, (x_sh, y_sh), (x_sh*4, y_sh*5), (0, 0, 255), 2)
        crop_rrec = frame[y_sh:y_sh*5, x_sh:x_sh*4]
        
        detections = self.get_detections(crop_rrec)
        self.draw_boxes(crop_rrec, detections)

        return frame
    