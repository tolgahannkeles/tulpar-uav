import cv2

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 640)
        self.camera.set(4, 480)

    def get_frame(self):
        ret, frame = self.camera.read()
        return frame
