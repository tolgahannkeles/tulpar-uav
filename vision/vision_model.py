import cv2
from ultralytics import YOLO
import torch
import time

from utils.target_selector import TargetSelector
from vision.frame_processor import FrameProcessor


class VisionModel:
    def __init__(self):
        self.model = YOLO("./models/best_yolov8n.pt")  # Load trained YOLO model
        self.model.to("cuda")  # Move model to GPU for faster inference
        self.locked_on_target = False
        self.lock_start_time = None

    def predict(self, frame):
        results = self.model.track(frame)

        if isinstance(results, list):
            result = results[0]
        else:
            result = results

        box = TargetSelector.select_target(result.boxes)

        if box is not None and box.xyxy.numel() == 4:
            x1, y1, x2, y2 = box.xyxy.cpu().numpy().flatten()
            confidence = box.conf.cpu().flatten().item()
            FrameProcessor.draw_boxes(frame, confidence, x1, y1, x2, y2)

            if TargetSelector.is_valid_target(box):
                if not self.locked_on_target:
                    self.locked_on_target = True
                    self.lock_start_time = time.time()
                else:
                    elapsed_time = time.time() - self.lock_start_time
                    FrameProcessor.display_lock_time(frame, elapsed_time)
                    if elapsed_time >= 4:
                        FrameProcessor.display_lock_status(frame, "Lock successful")
                        print("Lock successful| Time: ", time.time())
                        self.locked_on_target = False
                        self.lock_start_time = None
            else:
                self.locked_on_target = False
                self.lock_start_time = None
        else:
            FrameProcessor.draw_boxes(frame, None, 0, 0, 0, 0)
            self.locked_on_target = False
            self.lock_start_time = None
            print("No target detected")

        return frame