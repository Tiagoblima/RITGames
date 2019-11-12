import socket

MESSAGE = "Hello, World!"


class Connection:
    send_sock = None
    recv_sock = None

    dest_port = 5005
    dest_ip = "127.0.0.1"

    origin_ip = "127.0.0.1"
    origin_port = 5005

    def __init__(self):
        self.send_sock = socket.socket(socket.AF_INET,  # Internet
                                       socket.SOCK_DGRAM)  # UDP

    def send_obj(self, obj):

        self.send_sock.sendto(bytearray(str(obj), encoding='utf8'), (self.dest_ip, int(self.dest_port)))

    def set_dest_ip(self, ip):
        self.dest_ip = ip

    def set_dest_port(self, port):
        self.dest_port = port

    def set_origin_ip(self, ip):
        self.origin_ip = ip

    def set_origin_port(self, port):
        self.origin_port = port

    def listening(self):
        self.recv_sock = socket.socket(socket.AF_INET,  # Internet
                                       socket.SOCK_DGRAM)  # UDP
        self.recv_sock.bind((self.origin_ip, int(self.origin_port)))

        while True:
            data, addr = self.recv_sock.recvfrom(1024)  # buffer size is 1024 bytes
            return data
