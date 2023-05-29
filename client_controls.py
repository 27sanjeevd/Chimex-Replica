import json
import socket

class Client:
	def __init__(self):
		self.account_value = 0
		self.amount_bought = 0
		self.amount_shorted = 0

def is_json(message):
	try:
		json.loads(message)
		return True
	except ValueError:
		return False

def user_actions():
	action = input("(MARKET), (ACCOUNT), (ORDERS), or (MAKE) an order: ")
	data = {}

	if action == "MAKE":
		valuation = input("What valuation? ")
		spread = input("What spread? ")

		data = {
			"MAKE": True,
			"valuation": valuation,
			"spread": spread
		}
	else:
		data[action] = True


	json_data = json.dumps(data)
	encoded_data = json_data.encode('utf-8')
	return encoded_data