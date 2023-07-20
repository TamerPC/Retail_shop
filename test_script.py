import torch
import cv2
import matplotlib.pyplot as plt



def main():
    yolo = torch.hub.load("ultralytics/yolov5", "custom", path="yolov5/runs/train/exp/weights/best.pt") #init Model yolov5

    img = cv2.imread("yolov5/test_imgs/305_nwpmmhptjg.jpg")

    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()


def get_detections(img, model):
    return model(img).pandas().xyxy[0].to_dict('records')


if __name__ == "__main__":
    main()