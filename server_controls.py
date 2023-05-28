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

			return True, json_data
		else:
			decoded = message.decode('utf-8')
			if decoded == "ORDERS":
				order_book.print_orderbook()
				return False, None

			elif decoded == "ACCOUNT":
				return True, "ACCOUNT"

	except:
		return False, None

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
