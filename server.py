import socket
import sys
import json
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 5005)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    print('received {} bytes from {}'.format(
        len(data), address))
    print(data.decode('utf8'))
    data = json.loads(data.decode('utf8'))
    s = json.dumps(data, indent=4, sort_keys=True)

    with open('data_user.json', 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=4)
    if data:
        sent = sock.sendto(bytearray(str(data), encoding='utf8'), address)
        print('sent {} bytes back to {}'.format(sent, address))