import socket
import os
from _thread import *

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

clients = []

try:
	ServerSideSocket.bind((host, port))
except socket.error as e:
	print(str(e))

print('Socket is listening...')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
	connection.send(str.encode('Server is working:'))
	while True:
		data = connection.recv(2048)
		response = 'Server message: ' + data.decode('utf-8')
		if not data:
			break

		connection.sendall(str.encode(response))
	connection.close()
	clients.remove((connection, client_id))

def send_message_to_client(client_id, message):
    for client, cid in clients:
        if cid == client_id:
            client.sendall(str.encode(message))
            break

while True:
	Client, address = ServerSideSocket.accept()
	clients.append((Client, ThreadCount))
	print('Connected to: ' + address[0] + ':' + str(address[1]))
	start_new_thread(multi_threaded_client, (Client, ))
	ThreadCount += 1
	print('Thread Number: ' + str(ThreadCount))

ServerSideSocket.close()