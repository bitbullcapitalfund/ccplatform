There are two simple steps to follow: create a new strategy and running the trading platform.


A. Creating a new strategy.
	1 - Create a class that inherits Strategy in the file models.py.
		Example:

		class ToyStrategy(Strategy):
			pass

	2- Override the method calculate(). This method will be called each time a new trade is executed on the exchange. 
		Example:

		class ToyStrategy(Strategy):
			def calculate(self, _time, price, _type): 	# Always use these parameters.
				pass

	3- Use the parameters '_time', 'price', and '_type' to calculate the trading logic. '_time' is a datetime object, price is a float with the last price traded, and '_type' will be a string containing 'bid' or 'ask'.
		Example:

		class ToyStrategy(Strategy):
			def calculate(self, _time, price, _type): 	
				if float(price) >= 3000:
					print(price)

	4- Send signals to the exchange calling the publish(tuple) method. The tuple the send_signal method receives as the only parameter has this format (time, type, price).
		Example:

		class ToyStrategy(Strategy):
			def calculate(self, _time, price, _type): 	
				if float(price) >= 3000:
					self.send_signal((_time, 'BUY', 3000.00))

	5- You can check the attribute 'accountState' to know if you are in or out of the market. This attribute can have to states: 'CLOSE' (out of the market) or 'BUY' (in the market).
		Example:

		class ToyStrategy(Strategy):
			def calculate(self, _time, price, _type): 	
				if (float(price) >= 3000) and (self.accountState == 'CLOSE'):
					self.send_signal((_time, 'BUY', 3000.00))
				elif float(price) <= 2000 and (self.accountState == 'BUY'):
					self.send_signal((_time, 'CLOSE', 2000.00))


B. Running the trading platform.
	1 - Change line 41 of the script so it will instantiate your strategy.
		Example:

		strategy = models.ToyStrategy()

	2 - Run the script on the command line. Optionally you can change the currency you want to trade with.
		Example:

		C://Codebase/data> python live_trader.py BTC-USD



Event-driven backtesting coming soon!

