import json
import socket
import orderbook

def is_json(message):
	try:
		json.loads(message)
		return True
	except ValueError:
		return False

def decode_message(message, order_book):
	try:
		if is_json(message):
			decoded_data = message.decode('utf-8')
			json_data = json.loads(decoded_data)

			return json_data
		else:
			if message.decode('utf-8') == "ORDERS":
				order_book.print_orderbook()

			return None
	except:
		return None

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
