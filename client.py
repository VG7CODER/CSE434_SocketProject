"""
CSE 434 Socket Project
Group 5
Vansh Gupta
Nora Alrajhi
"""

import socket
import json

c2s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2s_sock.bind(('10.0.1.12', 3510))

c2c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2c_sock.bind(('10.0.1.12', 3511))

while True:
    command = input("Enter command here: ")
    if command == 'exit':
        print('Exiting...')
        break
    c2s_sock.sendto(command.encode('utf-8'),  ('10.0.1.11', 3500))
    if command.split(' ')[0] == 'query':
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        data = json.loads(data)
        print("Received :")
        for k, v in data.items():
            print(k, ':', v)
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        print("RETURN CODE :", data)
    elif command.split(' ')[0] == 'de-register':
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        print("Received :", data)
        if data[:7] == 'SUCCESS':
            print('Exiting...')
            break
    else:
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        print("Received :", data)
