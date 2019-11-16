import socket

MESSAGE = "Hello, World!"


class Connection:
    send_sock = None
    recv_sock = None

    _dest_port = 5005
    _dest_ip = "127.0.0.1"

    _source_ip = "127.0.0.1"
    _source_port = 5005

    def __init__(self):
        self.send_sock = socket.socket(socket.AF_INET,  # Internet
                                       socket.SOCK_DGRAM)  # UDP
        self.recv_sock = socket.socket(socket.AF_INET,  # Internet
                                       socket.SOCK_DGRAM)  # UDP

    def send_obj(self, obj):
        self.send_sock.sendto(bytearray(str(obj), encoding='utf8'), (self._dest_ip, int(self._dest_port)))

    def set_dest_ip(self, ip):
        self._dest_ip = ip

    def set_dest_port(self, port):
        self._dest_port = port

    def set_origin_ip(self, ip):
        self._source_ip = ip

    def set_origin_port(self, port):
        self._source_port = port

    def listening(self):

        self.recv_sock.bind((self._source_ip, int(self._source_port)))

        while True:
            data, addr = self.recv_sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.recv_sock.close()
            return data

    def close(self):
        self.send_sock.close()
