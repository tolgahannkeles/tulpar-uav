import pickle
import cv2
class FrameDecoder:

    @staticmethod
    def decode(frame):
        data = pickle.loads(frame)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return data
    
    @staticmethod
    def encode(frame):
        _, data = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
        frame_as_bytes = pickle.dumps(data)
        return frame_as_bytes