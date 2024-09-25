"""
CSE 434 Socket Project
Group 5
Vansh Gupta
Nora Alrajhi
"""

import socket
import json

registered_players = {}
ongoing_games = {}

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('10.0.1.11', 3500))

while True:
    print("Listening on ipv4 10.0.1.11 port 3500...")
    data, client_addr = server_sock.recvfrom(4096)
    data = data.decode('utf-8')
    print("Received command :", data, "by", client_addr)
    command = data.split(' ')
    if command[0] == 'register':
        player_name = command[1]
        player_ipv4 = command[2]
        player_tport = command[3]
        player_pport = command[4]
        if registered_players:
            player_present = False
            for i in registered_players:
                if i == player_name:
                    response = "FAILURE - Player already registered."
                    server_sock.sendto(response.encode('utf-8'), client_addr)
                    player_present = True
                    break
            if player_present is False:
                registered_players[player_name] = command[1:] + ['free',]
                response = "SUCCESS - Player registered."
                server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            registered_players[player_name] = command[1:] + ['free',]
            response = "SUCCESS - Player registered."
            server_sock.sendto(response.encode('utf-8'), client_addr)
    elif command[0] == 'de-register':
        if registered_players:
            player_present = False
            for i in registered_players:
                if i == command[1]:
                    if registered_players[command[1]][-1] != 'free':
                        response = "FAILURE - Player is playing a game."
                        server_sock.sendto(response.encode('utf-8'), client_addr)
                        player_present = True
                        break
                    else:
                        del registered_players[command[1]]
                        response = "SUCCESS - Player de-registered."
                        server_sock.sendto(response.encode('utf-8'), client_addr)
                        player_present = True
                        break
            if player_present is False:
                response = "FAILURE - Player not found."
                server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            response = "FAILURE - Player not found."
            server_sock.sendto(response.encode('utf-8'), client_addr)
    elif ((command[0] == 'query') and (command[1] == 'players')):
        response = json.dumps(registered_players)
        server_sock.sendto(response.encode('utf-8'), client_addr)
        response = str(len(registered_players))
        server_sock.sendto(response.encode('utf-8'), client_addr)
    elif ((command[0] == 'query') and (command[1] == 'games')):
        response = json.dumps(ongoing_games)
        server_sock.sendto(response.encode('utf-8'), client_addr)
        response = str(len(ongoing_games))
        server_sock.sendto(response.encode('utf-8'), client_addr)
    else:
        response = "FAILURE - Command not found."
        server_sock.sendto(response.encode('utf-8'), client_addr)
