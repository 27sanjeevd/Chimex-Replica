import socket
import client_controls

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')

try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientMultiSocket.recv(1024)

while True:

	input_data = client_controls.user_actions()
	ClientMultiSocket.sendall(input_data)

	#Input = input('Hey there: ')
	#ClientMultiSocket.send(str.encode(Input))
	
	res = ClientMultiSocket.recv(1024)
	print(res.decode('utf-8'))

ClientMultiSocket.close()