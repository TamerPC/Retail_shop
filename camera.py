import os
import cv2
from base_camera import BaseCamera
from imutils.video import FPS
import time
from product_detector import ProductDetector

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        # Camera.set_video_source('rtsp://admin:Qq12345678@172.16.3.52/Streaming/Channels/101')
        # Camera.set_video_source('rtsp://admin:Khc1234567@192.168.90.13/Streaming/Channels/101')
        Camera.set_video_source('media/video.mp4')
        
        super(Camera, self).__init__()
        

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        COUNTER_LIMIT = 200
        counter = 0
        fps = FPS().start()
        prod_tracker = ProductDetector()
        while True:
            start_fps = time.time()
            
            #====================================================================
            # Read current frame
            ret, frame = camera.read()
            # If not frame rerun VideoCapture
            if not ret:
                print("cannot read frame")
                camera = cv2.VideoCapture(Camera.video_source)
                continue
            
            #=====================================================================
            tracker_time = time.time()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = prod_tracker.run_product_detection(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #=====================================================================
            # Crop frame to small size
            # x_sh=int(frame.shape[1]/6)
            # y_sh=int(frame.shape[0]/6)
            # cv2.rectangle(frame, (x_sh*2, y_sh), (x_sh*6, y_sh*5), (0, 0, 255), 2)
            # crop_rrec = frame[y_sh:y_sh*5, x_sh:x_sh*5]

            # =====================================================================
            # FPS worker
            fps.update()
            fps.stop()
            end_fps = time.time()
            custom_fps = 1/(end_fps-start_fps)
            cv2.putText(frame, f"Approx. FPS: {fps.fps()}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Custom FPS: {custom_fps}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # =====================================================================
            # Runner log worker
            now = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            counter+=1
            if counter%COUNTER_LIMIT == 0:
                with open("running_checker.log", 'w+') as runner_log:
                    runner_log.write(f"[INFO] -- 'Last writed time' - [{now}]; Frame counter is - {counter};")
            
            # Counter worker
            with open("counter.log", 'w+') as counter_log:
                counter_log.writelines(f"[{now}]; Tracked time: {time.time()-tracker_time} sec. Frame number is - {counter};")

            #======================================================================
            # Frame generator | encode as a jpeg image and return it
            yield cv2.imencode('.jpg', frame)[1].tobytes()