import time

import cv2

class Camera:
    HEIGHT = 480
    WIDTH = 640
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, self.WIDTH)
        self.camera.set(4, self.HEIGHT)

    def get_frame(self):
        ret, frame = self.camera.read()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cv2.putText(frame, current_time, (10, self.HEIGHT-50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
        return frame
