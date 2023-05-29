class OrderBook:
	def __init__(self):
		self.buy_orders = []
		self.sell_orders = []

		self.best_buy = 0
		self.best_sell = 0

	def add_order(self, order):
		if order.isBuy:
			self.buy_orders.append(order)
			self.buy_orders.sort(key=lambda x: x.price, reverse=True)
			self.best_buy = self.buy_orders[0].price
		else:
			self.sell_orders.append(order)
			self.sell_orders.sort(key=lambda x: x.price)
			self.best_sell = self.sell_orders[0].price

	def return_orderbook(self):
		output = {}
		output['BUY'] = []
		output['SELL'] = []
		for order in self.buy_orders:
			curr = {
				"Price": order.price,
				"Quantity": order.amount,
				"User": order.client.client_id
			}
			output['BUY'].append(curr)

		for order in self.sell_orders:
			curr = {
				"Price": order.price,
				"Quantity": order.amount,
				"User": order.client.client_id
			}
			output['SELL'].append(curr)

		return output

	def print_orderbook(self):
		print("\nBuy Orders:")
		for order in self.buy_orders:
			print(f"Bid Price: {order.price}, Quantity: {order.amount}, User: {order.client.client_id}")

		print("Sell Orders:")
		for order in self.sell_orders:
			print(f"Sell Price: {order.price}, Quantity: {order.amount}, User: {order.client.client_id}")


	def match_orders(self):
		while(len(self.buy_orders) != 0 and len(self.sell_orders) != 0 
			and self.buy_orders[0].price >= self.sell_orders[0].price):

			sold_price = (self.buy_orders[0].price + self.sell_orders[0].price)/2
			"""
			if self.buy_orders[0].client.client_add.fileno() != -1:
				self.buy_orders[0].client.client_add.sendall(str.encode("Matched!\n"))

			if self.sell_orders[0].client.client_add.fileno() != -1:
				self.sell_orders[0].client.client_add.sendall(str.encode("Matched!\n"))
			"""


			if self.buy_orders[0].amount > self.sell_orders[0].amount:
				self.buy_orders[0].amount -= self.sell_orders[0].amount

				self.buy_orders[0].client.balance -= sold_price * self.sell_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.sell_orders[0].amount

				self.sell_orders[0].client.owned -= 1
				self.sell_orders.pop(0)

			elif self.buy_orders[0].amount < self.sell_orders[0].amount:
				self.sell_orders[0].amount -= self.buy_orders[0].amount

				self.buy_orders[0].client.balance -= sold_price * self.buy_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.buy_orders[0].amount

				self.buy_orders[0].client.owned += 1
				self.buy_orders.pop(0)
			else:
				self.buy_orders[0].client.balance -= sold_price * self.buy_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.buy_orders[0].amount


				self.sell_orders[0].client.owned -= 1
				self.buy_orders[0].client.owned += 1
				self.buy_orders.pop(0)
				self.sell_orders.pop(0)


			if len(self.buy_orders) > 0:
				self.best_buy = self.buy_orders[0].price
			else:
				self.best_buy = 0

			if len(self.sell_orders)> 0:
				self.best_sell = self.sell_orders[0].price
			else:
				self.best_sell = 0




class Order:
	def __init__(self, price, amount, user, isBuy):
		self.price = price
		self.amount = amount
		self.client = user
		self.isBuy = isBuy


class User:
	def __init__(self, client_id, client_add):
		self.balance = 1000
		self.orders = []
		self.client_id = client_id
		self.client_add = client_add
		self.owned = 0

	def add_order(self, order):
		self.orders.append(order)









