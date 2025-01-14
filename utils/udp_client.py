import socket

class UDPClient:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000)

    def send(self, data):
        self.s.sendto(data, (self.ip, self.port))

    def close(self):
        self.s.close()
    

