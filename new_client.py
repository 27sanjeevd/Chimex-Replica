import socket
import client_controls
import json
import os
from threading import Thread

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
data = {}

print('Waiting for connection response')

try:
	ClientMultiSocket.connect((host, port))
except socket.error as e:
	print(str(e))

res = ClientMultiSocket.recv(1024)

def receive_updates():
	while True:
		res = ClientMultiSocket.recv(1024)
		if client_controls.is_json(res):
			decoded_data = res.decode('utf-8')
			json_data = json.loads(decoded_data)

			data = json_data

def send_updates():
	while True:
		print(data)
		input_data = client_controls.user_actions()
		ClientMultiSocket.sendall(input_data)

receive_thread = Thread(target=receive_updates)
receive_thread.start()

send_thread = Thread(target=send_updates)
send_thread.start()

receive_thread.join()
send_thread.join()

ClientMultiSocket.close()