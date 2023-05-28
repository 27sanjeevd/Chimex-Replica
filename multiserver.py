import socket
import os
from _thread import *
import orderbook
import server_controls
import time

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0

clients = []
users = []
order_book = orderbook.OrderBook()

try:
	ServerSideSocket.bind((host, port))
except socket.error as e:
	print(str(e))

print('Socket is listening...')
ServerSideSocket.listen(5)

def server_sided_actions():
	while True:
		order_book.match_orders()
		time.sleep(10)

def multi_threaded_client(connection, user, arr_pos):
	connection.send(str.encode('Server is working:'))
	try:
		while True:
			data = connection.recv(2048)

			if not data:
				break

			json_data = server_controls.decode_message(data, order_book)
			if json_data:
				response = 'Valuation: ' + json_data['valuation'] + " Spread: " + json_data['spread']
				print(response)

				buy_order, sell_order = server_controls.make_orders(user, float(json_data['valuation']), float(json_data['spread']))
				order_book.add_order(buy_order)
				order_book.add_order(sell_order)
			else:
				response = "Printed Order"

			connection.sendall(str.encode(response))
	except ConnectionResetError:
		pass
	connection.close()

def send_message_to_client(client_id, message):
    for client, cid in clients:
        if cid == client_id:
            client.sendall(str.encode(message))
            break

start_new_thread(server_sided_actions, ())
try:
	while True:
		Client, address = ServerSideSocket.accept()
		clients.append((Client, ThreadCount))
		users.append(orderbook.User(client_id=str(address[1]), client_add=Client))

		print('Connected to: ' + address[0] + ':' + str(address[1]))
		start_new_thread(multi_threaded_client, (Client, users[-1], ThreadCount, ))
		ThreadCount += 1
		print('Thread Number: ' + str(ThreadCount))
except KeyboardInterrupt:
	ServerSideSocket.close()


ServerSideSocket.close()







