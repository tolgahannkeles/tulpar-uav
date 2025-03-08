import cv2
import time

from vision.camera import Camera


class FrameProcessor:

    @staticmethod
    def preprocess(frame):
        frame = cv2.resize(frame, (Camera.WIDTH, Camera.HEIGHT))
        return frame

    @staticmethod
    def draw_boxes(frame,confidence, x1, y1, x2, y2):
        FrameProcessor.__draw_hit_area(frame)
        FrameProcessor.__draw_bounding_box(frame, confidence, int(x1), int(y1), int(x2), int(y2))
        FrameProcessor.__add_timestamp(frame)
        return frame

    @staticmethod
    def __draw_hit_area(frame):
        frame_height, frame_width = frame.shape[:2]
        rect_x1, rect_y1 = int(frame_width * 0.25), int(frame_height * 0.1)
        rect_x2, rect_y2 = int(frame_width * 0.75), int(frame_height * 0.9)
        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 255, 255), 2)
        return frame

    @staticmethod
    def __draw_bounding_box(frame,confidence, x1, y1, x2, y2, color=(0, 0, 255), thickness=2):
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        if confidence is not None:
            cv2.putText(frame, "Confidence: {:.2f}".format(confidence), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 255), 2)
        return frame

    @staticmethod
    def __add_timestamp(frame):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cv2.putText(frame, current_time, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 255), 2)
        return frame

    @staticmethod
    def add_fps(frame, fps):
        cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 255), 2)
        return frame

    @staticmethod
    def display_lock_status(frame, status):
        cv2.putText(frame, status, (frame.shape[1] // 2 - 100, frame.shape[0] // 2), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        return frame

    @staticmethod
    def display_lock_time(frame, time):
        cv2.putText(frame, f"Locked on target for {int(time)} seconds", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 100, 255), 2)
        return frame