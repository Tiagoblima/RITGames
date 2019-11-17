import ast
import socket
import sys
import json


# Create a UDP socket


class Server:
    _source_address = ()
    _dst_address = ()
    _listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _server_address = ()
    data = False

    def __init__(self, server_address=('localhost', 5005)):
        # Bind the socket to the port
        self._server_address = server_address
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def listen(self, source_port):

        print('starting up on {} port {}'.format(*self._server_address))
        self._listener.bind(self._server_address)

        while True:
            print('\nwaiting to receive message')
            data, address = self._listener.recvfrom(source_port)
            self._source_address = address
            print('received {} bytes from {}'.format(len(data), address))
            str_data = str(data, encoding='utf8')

            self.data = json.loads(str_data)
            s = json.dumps(self.data, indent=4, sort_keys=True)
            self._listener.close()
            return s

    def sent(self, str_data, dst_address=('localhost', 5005)):
        self._dst_address = dst_address
        if str_data:
            # Bind the socket to the port
            self._sender.bind(self._server_address)
            sent = self._sender.sendto(bytearray(str_data, encoding='utf8'), self._dst_address)
            print('sent {} bytes back to {}'.format(sent, self._dst_address))
            self._sender.close()

    def get_data(self):
        return self.data


while True:
    listener = Server(('localhost', 9000))
    data = listener.listen(5005)

    data_dic = json.loads(data)
    print(int(data_dic['tipo']) is 2)
    if int(data_dic['tipo']) is 2:

        with open('data_user.json', 'r') as file:
            user = file.read()
            print(user)
            sender = Server(('localhost', 9000))
            sender.sent(user)
