import socket

registered_players = {}
ongoing_games = {}

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('localhost', 3500))

while True:
    data, client_addr = server_sock.recvfrom(4096)
    data = data.decode('utf-8')
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
        response = registered_players
	server_sock.sendto(response.encode('utf-8'), client_addr)
	response = len(registered_players)
	server_sock.sendto(response.encode('utf-8'), client_addr)
    elif ((command[0] == 'query') and (command[1] == 'games')):
        response = ongoing_games
	server_sock.sendto(response.encode('utf-8'), client_addr)
	response = len(ongoing_games)
	server_sock.sendto(response.encode('utf-8'), client_addr)
    else:
        response = "FAILURE - Command not found."
	server_sock.sendto(response.encode('utf-8'), client_addr)