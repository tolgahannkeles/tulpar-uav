import numpy as np
from vision.camera import Camera

class TargetSelector:

    @staticmethod
    def select_target(boxes):
        valid_targets = []
        max_confidence = 0
        max_confidence_box = None
        for box in boxes:
            if TargetSelector.is_valid_target(box):
                valid_targets.append(box)
            if  max_confidence < box.conf.item():
                max_confidence = box.conf.item()
                max_confidence_box = box

        if len(valid_targets) > 0:
            return valid_targets[0]
        else:
            return max_confidence_box

    @staticmethod
    def is_valid_target(box):
        frame_height, frame_width = Camera.HEIGHT, Camera.WIDTH
        rect_x1, rect_y1 = int(frame_width * 0.25), int(frame_height * 0.1)
        rect_x2, rect_y2 = int(frame_width * 0.75), int(frame_height * 0.9)

        # Convert tensor to numpy array
        xyxy = box.xyxy.cpu().numpy().flatten()
        x1, y1, x2, y2 = xyxy
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        if rect_x1 < center_x < rect_x2 and rect_y1 < center_y < rect_y2:
            return True
        else:
            return False