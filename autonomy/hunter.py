import cv2
import time
from ultralytics import YOLO
from vision.camera import Camera
from vision.frame_processor import FrameProcessor
from vision.vision_model import VisionModel


class HunterMission:

    def __init__(self):
        self.camera = Camera()  # Camera object to get frames
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.video_writer = None
        self.vision_model = VisionModel()

    def start(self):
        # Initialize VideoWriter with MP4 codec
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

        while True:
            # Get the frame from the camera
            frame = self.camera.get_frame()

            # Preprocess the frame
            frame = FrameProcessor.preprocess(frame)

            frame = self.vision_model.predict(frame)

            # Update FPS counter
            self.frame_count += 1
            if time.time() - self.start_time >= 1.0:  # 1 second elapsed
                self.fps = self.frame_count
                self.frame_count = 0
                self.start_time = time.time()

            FrameProcessor.add_fps(frame, self.fps)

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