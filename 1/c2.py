import socket

csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
csock.connect(('127.0.0.1', 5555))

while True:
    data = csock.recv(1024).decode()
    print(data, end='')

    if 'Your final balance is' in data or 'Authentication failed' in data:
        break

    user_input = input()
    csock.send(user_input.encode())

csock.close()

