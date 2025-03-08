from autonomy.hunter import HunterMission
from communication.uav_communication import UAVCommunication
from vision.camera import Camera


class UAV:

    ip="127.0.0.1"
    video_server_port={
        "video_port": 6666,
        "control_port": 6667,
        "telemetry_port": 1234
    }

    def __init__(self):
        self.communication = UAVCommunication(self.ip, self.video_server_port)
        self.hunter = HunterMission()
        self.camera = Camera()

    def start(self):
        #self.communication.start_communication()
        self.hunter.start()




if __name__ == "__main__":
    uav = UAV()
    uav.start()