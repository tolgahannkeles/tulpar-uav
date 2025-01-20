import threading
import time

from utils.telemetry import TelemetryUtil
from utils.udp_client import UDPClient
from utils.camera import Camera
from utils.frame_decoder import FrameDecoder


class UAVCommunication:

    def __init__(self, ip, ports):
        self.ip = ip
        self.ports = ports
        self.video_client = UDPClient(self.ip, self.ports["video_port"])
        self.telemetry_client = UDPClient(self.ip, self.ports["telemetry_port"])
        self.camera = Camera()


    def __send_video(self):
        print("Sending Video")
        while True:
            try:
                frame = self.camera.get_frame()
                encoded_frame = FrameDecoder.encode(frame)
                self.video_client.send(encoded_frame)
            except Exception as e:
                print(f"Video Error: {e}")

    def __send_telemetry(self):
        print("Sending Telemetry")
        while True:
            try:
                telemetry = TelemetryUtil.get_telemetry()
                self.telemetry_client.send(telemetry)
                time.sleep(.2)
            except Exception as e:
                print(f"Telemetry Error: {e}")

    def start_communication(self):
        video_thread = threading.Thread(target=self.__send_video)
        telemetry_thread = threading.Thread(target=self.__send_telemetry)
        video_thread.start()
        telemetry_thread.start()
        video_thread.join()
        telemetry_thread.join()