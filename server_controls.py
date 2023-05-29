import json
import socket
import orderbook

def is_json(message):
	try:
		json.loads(message)
		return True
	except ValueError:
		return False

def decode_message(message, order_book, user):
	try:
		if is_json(message):
			decoded_data = message.decode('utf-8')
			json_data = json.loads(decoded_data)

			return json_data

	except:
		return None

def server_action(json_data, order_book, user):
	response = {}
	if json_data:
		if "ACCOUNT" in json_data:
			if user.owned > 0:
				response['ACCOUNT'] = f"You own {user.owned} shares"
			elif user.owned < 0:
				response['ACCOUNT'] = f"You shorted {user.owned * -1} shares"
			else:
				response['ACCOUNT'] = f"You are market neutral"
		elif "MARKET" in json_data:
			order_book.print_orderbook()
			market = order_book.return_orderbook()
			response['MARKET'] = market

		elif "ORDERS" in json_data:
			list1 = user.orders
			response['ORDERS'] = []
			for order1 in list1:
				if order1.isBuy:
					response['ORDERS'].append(f"Buying {order1.amount} for {order1.price}\n")
				else:
					response['ORDERS'].append(f"Selling {order1.amount} for {order1.price}\n")

		elif "MAKE" in json_data:
			response['MAKE'] = {}
			response['MAKE']['Valuation'] = json_data['valuation']
			response['MAKE']['Spread'] = json_data['spread']
			print(response)

			buy_order, sell_order = make_orders(user, float(json_data['valuation']), float(json_data['spread']))
			order_book.add_order(buy_order)
			order_book.add_order(sell_order)
		else:
			response['PRINTED'] = "Printed Order"

	response['Bid'] = order_book.best_buy
	response['Sell'] = order_book.best_sell

	json_data = json.dumps(response)
	encoded_data = json_data.encode('utf-8')
	return encoded_data


def make_orders(user, valuation, spread):
	lower_val = valuation - spread
	upper_val = valuation + spread

	lower_order = None
	upper_order = None
	if lower_val > 0:
		lower_order = orderbook.Order(lower_val, 1, user, True)
		user.add_order(lower_order)

	upper_order = orderbook.Order(upper_val, 1, user, False)
	user.add_order(upper_order)


	return lower_order, upper_order
