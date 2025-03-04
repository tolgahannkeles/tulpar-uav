import cv2
import time
from ultralytics import YOLO
import torch
from utils.camera import Camera

class HunterMission:

    def __init__(self):
        self.camera = Camera()  # Camera object to get frames
        self.model = YOLO("./models/best_yolov8n.pt")  # Load trained YOLO model
        self.model.to("cuda")
        self.use_gpu = torch.cuda.is_available()  # Check if GPU is available
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.video_writer = None

    def start(self):
        # Initialize VideoWriter with MP4 codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

        while True:
            # Get the frame from the camera
            frame = self.camera.get_frame()

            # Ensure the frame is the correct size
            frame = cv2.resize(frame, (640, 480))  # Resize to 640x480

            # Run inference on the frame
            results = self.model.track(frame)

            # Check if results is a list (common with YOLOv8)
            if isinstance(results, list):
                result = results[0]  # The first item in the list is the relevant result
            else:
                result = results

            # Extract bounding box coordinates, confidence, and class
            boxes = result.boxes.xywh.cpu().numpy()  # xywh format (x, y, width, height)
            confidences = result.boxes.conf.cpu().numpy()  # Confidence score
            classes = result.boxes.cls.cpu().numpy()  # Class labels (IDs)

            # Iterate through each detection and draw the bounding box
            for box, conf, cls in zip(boxes, confidences, classes):
                x, y, w, h = box
                x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)

                # Draw the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue box with thickness of 2

                # Draw a red dot at the center of the detected object
                center_x, center_y = int(x), int(y)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Red dot with radius 5

                # Optionally, add the confidence score and class label as text
                label = f"Class: {int(cls)} | Conf: {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Draw a red rectangle covering 50% width and 80% height of the frame
            frame_height, frame_width = frame.shape[:2]
            rect_x1, rect_y1 = int(frame_width * 0.25), int(frame_height * 0.1)
            rect_x2, rect_y2 = int(frame_width * 0.75), int(frame_height * 0.9)
            cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 255), 2)  # Red rectangle

            # Update FPS counter
            self.frame_count += 1
            if time.time() - self.start_time >= 1.0:  # 1 second elapsed
                self.fps = self.frame_count
                self.frame_count = 0
                self.start_time = time.time()

            # Display FPS and GPU usage information
            fps_text = f"FPS: {self.fps}"
            gpu_text = f"Using GPU: {self.use_gpu}"

            # Add FPS and GPU info as text on the frame
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, gpu_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Write the frame to the video file
            self.video_writer.write(frame)

            # Display the frame with bounding boxes and additional info
            cv2.imshow("Detection", frame)

            # Exit the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera, VideoWriter, and close the OpenCV window
        self.camera.release()
        self.video_writer.release()
        cv2.destroyAllWindows()