"""
CSE 434 Socket Project
Group 5
Vansh Gupta
Nora Alrajhi

Description: This code needs to be executed on the server side (i.e., on the tracker machine), and
             would keep listening on the particular UDP socket for commands from clients (peers).
"""

# importing modules
import socket
import json
import random

# declaring storage dictionaries and other variables
registered_players = {}
ongoing_games = {}
unique_counter = 0

# asking for the server's current ipv4 address from the user
server_ipv4 = input("Enter the ipv4 address of this end-host: ")

# creating a UDP socket for the server with the correct address and port number 3500
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((server_ipv4, 3500))

# while loop to keep listening on the UDP socket
while True:
    # print statement for easier trace of messages
    print("Listening on ipv4", server_ipv4, "port 3500...")

    #reading the response sent by clients
    data, client_addr = server_sock.recvfrom(4096)
    data = data.decode('utf-8')

    # print statement for easier trace of messages
    print("Received command :", data, "by", client_addr)

    # spliting the response to handle parameters properly
    command = data.split(' ')

    # code to be executed if register command is received
    if command[0] == 'register':
        # storing the parameters into respective variables
        player_name = command[1]
        player_ipv4 = command[2]
        player_tport = command[3]
        player_pport = command[4]
        # code to be executed if registered_players is not empty
        if registered_players:
            player_present = False
            for i in registered_players:
                if i == player_name:
                    # if player is already registered, send response as FAILURE
                    response = "FAILURE - Player already registered."
                    server_sock.sendto(response.encode('utf-8'), client_addr)
                    player_present = True
                    break
            if player_present is False:
                # if player is not register, send response as SUCCESS after registering it
                registered_players[player_name] = command[1:] + ['free',]
                response = "SUCCESS - Player registered."
                server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            # if no players are registered yet, simply register the player
            registered_players[player_name] = command[1:] + ['free',]
            response = "SUCCESS - Player registered."
            server_sock.sendto(response.encode('utf-8'), client_addr)

    # code to be executed if de-register command is received
    elif command[0] == 'de-register':
        # code to be executed if registered_players is not empty
        if registered_players:
            player_present = False
            for i in registered_players:
                if i == command[1]:
                    if registered_players[command[1]][-1] != 'free':
                        # if player's status is not free, send response as FAILURE
                        response = "FAILURE - Player is playing a game."
                        server_sock.sendto(response.encode('utf-8'), client_addr)
                        player_present = True
                        break
                    else:
                        # if player's status is free, send response as SUCCESS after de-registering
                        del registered_players[command[1]]
                        response = "SUCCESS - Player de-registered."
                        server_sock.sendto(response.encode('utf-8'), client_addr)
                        player_present = True
                        break
            # if player is not even registered, send response as FAILURE
            if player_present is False:
                response = "FAILURE - Player not found."
                server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            # if no players are registered yet, send response as FAILURE
            response = "FAILURE - Player not found."
            server_sock.sendto(response.encode('utf-8'), client_addr)
    
    # code to be executed if query players command is received
    elif ((command[0] == 'query') and (command[1] == 'players')):
        # encoding the dictionary as a json before sending it to client
        response = json.dumps(registered_players)
        server_sock.sendto(response.encode('utf-8'), client_addr)
        response = str(len(registered_players))
        server_sock.sendto(response.encode('utf-8'), client_addr)
    
    # code to be executed if query games command is received
    elif ((command[0] == 'query') and (command[1] == 'games')):
        # encoding the dictionary as a json before sending it to client
        response = json.dumps(ongoing_games)
        server_sock.sendto(response.encode('utf-8'), client_addr)
        response = str(len(ongoing_games))
        server_sock.sendto(response.encode('utf-8'), client_addr)

    # code to be executed if start game command is received
    elif command[0] == 'start':
        dealer = command[2]
        n = int(command[3])
        if len(command) == 5:
            holes = int(command[4])
        else:
            holes = 9
        player_present = False
        for i in registered_players:
            if i == dealer:
                player_present = True
                break
        if player_present is False:
            response = 'FAILURE - Player not found.'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        elif ((n < 1) or (n > 3)):
            response = 'FAILURE - Parameter n is not in the proper range of [1, 3].'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        elif (n >= len(registered_players)):
            response = 'FAILURE - There are not at least n other players registered.'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        elif ((holes < 1) or (holes > 9)):
            response = 'FAILURE - Parameter holes is not in the proper range of [1, 9].'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            c = 0
            for p_name, p_info in registered_players.items():
                if p_info[-1] == 'free':
                    c += 1
            if c <= n:
                response = 'FAILURE - There are not at least n other players free.'
                server_sock.sendto(response.encode('utf-8'), client_addr)
            else:
                free_players = [p_name for p_name, p_info in registered_players.items() if (p_info[-1] == 'free' and p_name != dealer)]
                selected_players = random.sample(free_players, n)
                unique_counter += 1
                ongoing_games[unique_counter] = [dealer] + selected_players
                registered_players[dealer][-1] = 'in-play'
                players_playing = [(registered_players[dealer][0], registered_players[dealer][1], registered_players[dealer][3])]
                for i in selected_players:
                    registered_players[i][-1] = 'in-play'
                    players_playing.append((registered_players[i][0], registered_players[i][1], registered_players[i][3]))
                response = "SUCCESS - Game with identifier '" + str(unique_counter) + "' started."
                server_sock.sendto(response.encode('utf-8'), client_addr)
                response = json.dumps(players_playing)
                server_sock.sendto(response.encode('utf-8'), client_addr)

    # code to be executed if end game command is received
    elif command[0] == 'end':
        game_id = int(command[1])
        game_dealer = command[2]
        game_present = False
        for i in ongoing_games:
            if i == game_id:
                game_present = True
                break
        if game_present is False:
            response = 'FAILURE - Game not found.'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        elif ongoing_games[game_id][0] != game_dealer:
            response = 'FAILURE - Parameter player is not the dealer of this game.'
            server_sock.sendto(response.encode('utf-8'), client_addr)
        else:
            for i in ongoing_games[game_id]:
                registered_players[i][-1] = 'free'
            del ongoing_games[game_id]
            response = "SUCCESS - Game '" + str(game_id) + "' ended."
            server_sock.sendto(response.encode('utf-8'), client_addr)
    
    # code to be executed if no valid command is received
    else:
        response = "FAILURE - Command not found."
        server_sock.sendto(response.encode('utf-8'), client_addr)
