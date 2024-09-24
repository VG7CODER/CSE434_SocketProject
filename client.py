import socket


c2s_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2s_sock.bind(('localhost', 3510))

c2c_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c2c_sock.bind(('localhost', 3511))

while True:
    command = input("Enter command here: ")
    if command == 'exit':
        print('Exiting...')
        break
    c2s_sock.sendto(command.encode('utf-8'),  ('locality', 3500))
    data, _ = c2s_sock.recvfrom(4096)
    print("Received :", data.decode('utf-8'))