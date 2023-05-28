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
	action = input("(ORDERS), (ACCOUNT), or (MAKE) an order: ")
	if action == "MAKE":
		valuation = input("What valuation? ")
		spread = input("What spread? ")

		data = {
			"valuation": valuation,
			"spread": spread
		}

		json_data = json.dumps(data)
		encoded_data = json_data.encode('utf-8')
		return encoded_data
	else:
		return action.encode('utf-8')