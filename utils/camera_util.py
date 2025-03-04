import time

import cv2

from utils.camera import Camera


class CameraUtil:

    @staticmethod
    def generate_frame_for_comm(frame):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cv2.putText(frame, current_time, (10, Camera.HEIGHT-50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
        return frame
