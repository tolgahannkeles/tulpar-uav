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
        frame = self.camera.get_frame()
        encoded_frame= FrameDecoder.encode(frame)
        self.video_client.send(encoded_frame)

    def __send_telemetry(self):
        telemetry = TelemetryUtil.get_telemetry()
        self.telemetry_client.send(telemetry)

    def start_communication(self):
        while True:
            try:
                self.__send_video()
                self.__send_telemetry()
            except Exception as e:
                print(f"Error: {e}")
                break