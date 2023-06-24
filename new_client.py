import socket
import client_controls
import json
import os
import threading
from threading import Thread
import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
data = {}
bid = 0
ask = 0
orders = ""
prev_orders = ""
balance = "Balance: N/A"
owned = "Position: N/A"

position_orders = [[], []]
position_amts = [[], []]
fig = plt.Figure(figsize=(6, 4), dpi=100)

data_lock = threading.Lock()

print('Waiting for connection response')

try:
	ClientMultiSocket.connect((host, port))
except socket.error as e:
	print(str(e))

res = ClientMultiSocket.recv(1024)


def on_button_click():
	valuation = valuation_entry.get()
	spread = spread_entry.get()

	if not valuation or not spread:
		error_entry.config(text="Error: Please fill in all fields")
	else:
		error_entry.config(text="")

		ClientMultiSocket.sendall(client_controls.client_order(valuation, spread))

def update_prev_orders():
	global prev_orders
	prev_orders = "Previous Orders:\n"
	if "PREVIOUS" in data:
		for prev in data['PREVIOUS']:
			prev_orders += prev


	prev_orders_label.config(text=prev_orders)


def update_best_orders():
	global bid
	global ask
	if "Bid" in data:
		bid = data['Bid']
	if "Sell" in data:
		ask = data['Sell']

	data_label.config(text="Top Bid: " + str(bid) + "\nTop Ask: " + str(ask))

def update_curr_orders():
    global orders
    orders = "My Orders:\n"
    if "ORDERS" in data:
    	orders1 = data['ORDERS']
    	for x in orders1:
    		if x[0] == "BUY":
    			orders += f"Buying {x[1]} for {x[2]}\n"
    		else:
    			orders += f"Selling {x[1]} for {x[2]}\n"
    		#orders += str(x)

    	orders_label.config(text=str(orders))

def update_positions():
	global balance
	global owned

	if "BALANCE" in data:
		balance = "Balance: " + str(data['BALANCE'])
	if "ACCOUNT" in data:
		owned = data['ACCOUNT']

	balance_label.config(text=str(balance))
	position_label.config(text=str(owned))

def update_charts():
	global position_orders
	global position_amts
	global data
	global fig, bar1, bar2, canvas, ax1, ax2
	if "MARKET" in data:

		position_orders = [[], []]
		position_amts = [[], []]

		orders1 = data['MARKET']

		for order in orders1["BUY"]:
			if order["Price"] in position_orders[0]:
				position_amts[0][position_orders[0].index(order["Price"])] += order["Quantity"]
			else:
				position_orders[0].append(order["Price"])
				position_amts[0].append(order["Quantity"])

		for order in orders1["SELL"]:
			if order["Price"] in position_orders[1]:
				position_amts[1][position_orders[1].index(order["Price"])] += order["Quantity"]
			else:
				position_orders[1].append(order["Price"])
				position_amts[1].append(order["Quantity"])


		for bar in bar1:
			bar.set_height(0)

		for bar in bar2:
			bar.set_height(0)

		bar1 = ax1.bar(position_orders[0], position_amts[0], color='green')
		bar2 = ax2.bar(position_orders[1], position_amts[1], color='red')

		max_height = 2
		if len(position_amts[0]) > 0:
			max_height = max(max_height, max(position_amts[0]))
		if len(position_amts[1]) > 0:
			max_height = max(max_height, max(position_amts[1]))

		max_height *= 1.5
		
		ax1.set_ylim(0, max_height)
		ax2.set_ylim(0, max_height)
		canvas.draw()

		#ax2 = ax1.twinx()
		#ax2.bar(position_orders[1], position_amts[1], color='red')

		#fig.tight_layout()
		print(position_orders)
		print(position_amts)


def receive_updates():
	while True:
		res = ClientMultiSocket.recv(1024)
		if client_controls.is_json(res):
			decoded_data = res.decode('utf-8')
			json_data = json.loads(decoded_data)

			data_lock.acquire()

			global data
			if json_data != data:
				data = json_data

				update_best_orders()
				update_curr_orders()
				update_prev_orders()
				update_positions()
				update_charts()

			data_lock.release()

window = tk.Tk()
window.title("Value Calculator")

# Calculate the default size of the window as 40% of the screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = int(screen_width * 0.4)
window_height = int(screen_height * 0.6)

# Set the default window size
window.geometry(f"{window_width}x{window_height}")

# Create labels for valuation and spread
valuation_label = tk.Label(window, text="Valuation:")
valuation_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

valuation_entry = tk.Entry(window)
valuation_entry.grid(row=1, column=0, padx=10, pady=5, sticky="e")

spread_label = tk.Label(window, text="Spread:")
spread_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")

spread_entry = tk.Entry(window)
spread_entry.grid(row=1, column=1, padx=10, pady=5, sticky="e")

button = tk.Button(window, text="Send Values", command=on_button_click)
button.grid(row=2, column=0, padx=10, pady=5, sticky="e")

error_entry = tk.Label(window)
error_entry.grid(row=3, column=0, padx=10, pady=5, sticky="e")

data_label = tk.Label(window, text="Top Bid: " + str(bid) + "\nTop Ask: " + str(ask))
data_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
data_label.configure(background="skyblue")

orders_label = tk.Label(window, text=str(orders))
orders_label.grid(row=4, column=1, padx=10, pady=5, sticky="e")
orders_label.configure(background="skyblue")

balance_label = tk.Label(window, text=str(balance))
balance_label.grid(row=4, column=2, padx=10, pady=5, sticky="e")
balance_label.configure(background="skyblue")

prev_orders_label = tk.Label(window, text=str(prev_orders))
prev_orders_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
prev_orders_label.configure(background="skyblue")

position_label = tk.Label(window, text=str(owned))
position_label.grid(row=5, column=2, padx=10, pady=5, sticky="e")
position_label.configure(background="skyblue")

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
total_amts = [50, 75, 60, 80, 70, 90, 40, 55, 65, 85]

# Split the data and total_amts into two separate lists
list1_data = [data[i] for i in range(len(data)) if i % 2 == 0]
list1_total_amts = [total_amts[i] for i in range(len(total_amts)) if i % 2 == 0]
list2_data = [data[i] for i in range(len(data)) if i % 2 == 1]
list2_total_amts = [total_amts[i] for i in range(len(total_amts)) if i % 2 == 1]

fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="e")

ax1 = fig.add_subplot(111)
bar1 = ax1.bar(position_orders[0], position_amts[0], color='green')
ax1.set_xlabel('Prices')
ax1.set_ylabel('Total Amount')

ax2 = ax1.twinx()
bar2 = ax2.bar(position_orders[1], position_amts[1], color='red')
ax2.set_ylabel('Total Amount')

ax1.set_ylim(0, 2)
ax2.set_ylim(0, 2)


receive_thread = Thread(target=receive_updates)
receive_thread.start()

window.mainloop()

receive_thread.join()
ClientMultiSocket.close()