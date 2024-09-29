"""
CSE 434 Socket Project
Group 5
Vansh Gupta
Nora Alrajhi
"""

import socket
import json

server_ipv4 = input("Enter the ipv4 address for the tracker: ")
server_addr = (server_ipv4, 3500)

client_ipv4 = input("Enter the ipv4 address for this peer: ")
client_tport = int(input("Enter the t-port number for this peer: "))
client_pport = int(input("Enter the p-port number for this peer: "))

c2s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2s_sock.bind((client_ipv4, client_tport))

c2c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2c_sock.bind((client_ipv4, client_pport))

while True:
    command = input("Enter command here: ")
    if command == 'exit':
        print('Exiting...')
        break
    c2s_sock.sendto(command.encode('utf-8'),  server_addr)
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
