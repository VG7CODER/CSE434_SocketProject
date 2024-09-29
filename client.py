"""
CSE 434 Socket Project
Group 5
Vansh Gupta
Nora Alrajhi

Description : This code needs to be executed on the client side (i.e., on the peer machines), and
              would ask user for commands that will be sent via the particular UDP socket to tracker.
"""

# importing modules
import socket
import json

# asking for the server's ipv4 and creating the address tuple
server_ipv4 = input("Enter the ipv4 address for the tracker: ")
server_addr = (server_ipv4, 3500)

# asking for the client's ipv4 and port numbers to be used
client_ipv4 = input("Enter the ipv4 address for this peer: ")
client_tport = int(input("Enter the t-port number for this peer: "))
client_pport = int(input("Enter the p-port number for this peer: "))

# creating a UDP socket for client-server communication
c2s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2s_sock.bind((client_ipv4, client_tport))

# creating a UDP socket for client-client communication
c2c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2c_sock.bind((client_ipv4, client_pport))

# while loop to keep sending commands until user enters "exit"
while True:
    command = input("Enter command here: ")

    # if user enters "exit", break from the loop and exit the program
    if command == 'exit':
        print('Exiting...')
        break

    # otherwise send the command to the server (tracker)
    c2s_sock.sendto(command.encode('utf-8'),  server_addr)

    # code to be executed if command sent is quering players or games
    if command.split(' ')[0] == 'query':
        # receiving the response with the client-server UDP socket
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        # decode the received dictionary using the json module
        data = json.loads(data)
        print("Received :")
        # print the key-value pairs of information present in the dictionary
        for k, v in data.items():
            print(k, ':', v)
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        # print statement displaying the return code accordingly
        print("RETURN CODE :", data)

    # code to be executed if command sent is de-registering the player
    elif command.split(' ')[0] == 'de-register':
        # receiving the response with the client-server UDP socket
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        print("Received :", data)
        # if response is SUCCESS then exit the program
        if data[:7] == 'SUCCESS':
            print('Exiting...')
            break
    else:
        # code to be executed if command sent is registering player or something else
        data, _ = c2s_sock.recvfrom(4096)
        data = data.decode('utf-8')
        print("Received :", data)
