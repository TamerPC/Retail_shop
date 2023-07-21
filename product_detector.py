import torch
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from shelf import Shelf
from product_tracker import Product_tracker


class ProductDetector():
    yolo = torch.hub.load("ultralytics/yolov5", "custom", path="product_weights/weights/best.pt") #init Model yolov5

    __prev_det = dict()
    __cur_det = dict()
    
    def get_detections(self, img):
        return self.yolo(img).pandas().xyxy[0].to_dict('records')

    def draw_boxes(self, frame, detections):
        for detection in detections:
            cv2.putText(frame, detection['name'], (int(detection['xmin']), int(detection['ymin'])+15), 1, 0.7, (255,255,255), 1)
            cv2.rectangle(frame,(int(detection['xmin']), int(detection['ymin'])), (int(detection['xmax']), int(detection['ymax'])), (0,255,0), 2)

    def run_product_detection(self, frame):
        x_sh=int(frame.shape[1]/6)
        y_sh=int(frame.shape[0]/6)
        cv2.rectangle(frame, (x_sh, y_sh), (x_sh*4, y_sh*5), (255, 0, 0), 5)
        crop_rrec = frame[y_sh:y_sh*5, x_sh:x_sh*4]


#===========================================================================================
        shelf1 = Shelf(0, 0, x_sh*4, y_sh*1.4)
        cv2.line(crop_rrec, (0, int(y_sh*1.4)), (x_sh*4, int(y_sh*1.4)), (255,0,0), 5)

        shelf2 = Shelf(0, y_sh*1.5, x_sh*4, y_sh*2,)
        cv2.line(crop_rrec, (0, int(y_sh*2)), (x_sh*4, int(y_sh*2)), (255,0,0), 5)
#============================================================================================
        
        detections = self.get_detections(crop_rrec) #xmin, xmax, ymin, ymax, confidence, class, name
        self.draw_boxes(crop_rrec, detections)

        tracker = Product_tracker()
        tracker.run_shelf_monitoring(crop_rrec, detections)

        return frame
    
    def get_statistic(self, detections):
        return Counter(d['name'] for d in detections)
    