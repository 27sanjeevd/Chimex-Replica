class OrderBook:
	def __init__(self):
		self.buy_orders = []
		self.sell_orders = []

	def add_order(self, order):
		if order.isBuy:
			self.buy_orders.append(order)
		else:
			self.sell_orders.append(order)

	def print_orderbook(self):
		print("Buy Orders:")
		for order in self.buy_orders:
			print(f"Bid Price: {order.price}, Quantity: {order.quantity}")

		print("Sell Orders:")
		for order in self.sell_orders:
			print(f"Sell Price: {order.price}, Quantity: {order.quantity}")


	def match_orders(self):
		self.buy_orders.sort(key=lambda x: x.price, reverse=True)
		self.sell_orders.sort(key=lambda x: x.price)

		while(len(self.buy_orders) != 0 and len(self.sell_orders) != 0 
			and self.buy_orders[0].price >= self.sell_orders[0].price):

			sold_price = (self.buy_order[0].price + self.sell_orders[0].price)/2

			if self.buy_orders[0].amount > self.sell_orders[0].amount:
				self.buy_orders[0].amount -= self.sell_orders[0].amount

				self.buy_orders[0].client.balance -= sold_price * self.sell_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.sell_orders[0].amount

				self.sell_orders.pop(0)

			elif self.buy_orders[0].amount < self.sell_orders[0].amount:
				self.sell_orders[0].amount -= self.buy_orders[0].amount

				self.buy_orders[0].client.balance -= sold_price * self.buy_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.buy_orders[0].amount

				self.buy_orders.pop(0)
			else:
				self.buy_orders[0].client.balance -= sold_price * self.buy_orders[0].amount
				self.sell_orders[0].client.balance += sold_price * self.buy_orders[0].amount

				self.buy_orders.pop(0)
				self.sell_orders.pop(0)




class Order:
	def __init__(self, price, amount, user):
		self.price = price
		self.amount = amount
		self.client = user


class User:
	def __init__(self, client_id):
		self.balance = 1000;
		self.orders = []
		self.client_id = client_id;