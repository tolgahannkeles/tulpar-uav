import time

import cv2

class Camera:
    HEIGHT = 640
    WIDTH = 480
    def __init__(self):
        self.camera = cv2.VideoCapture("./video/test-3.mp4")
        self.camera.set(3, self.WIDTH)
        self.camera.set(4, self.HEIGHT)

    def get_frame(self):
        ret, frame = self.camera.read()
        return frame
