import json
import socket

def is_json(message):
	try:
		json.loads(message)
		return True
	except ValueError:
		return False

def user_actions():
	action = input("(ORDERS) or (MAKE) an order: ")
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