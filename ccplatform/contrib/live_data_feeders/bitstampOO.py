import pusherclient
import sys
import time
import threading

class BistampWebsocket():
	#dictionary of tradings supported by bitstamp
	listOfTradingPairs = {'BTC-USD':'btcusd','BTC-EUR':'btceur','EUR-USD':'eurusd','XRP-USD':'xrpusd','XRP-EUR':'xrpeur','XRP-BTC':'xrpbtc','LTC-USD':'ltcusd','LTC-EUR':'ltceur','LTC-BTC':'ltcbtc'}
	def __init__(self,channels=[]):
		self.channels=channels
		self.check_tradepair()
		self.currency=''
		self.appkey = "de504dc5763aeef9ff52"
		self.pusher = pusherclient.Pusher(self.appkey)
		
		
	def check_tradepair(self):
		for c in self.channels:
			if c in BistampWebsocket.listOfTradingPairs.keys():
				pass
			else:
				self.channels.remove(c)
				print("{} is not OkCoin TradePair List".format(c))

	# We can't subscribe until we've connected, so we use a callback handler
	# to subscribe when able
	def connect_handler_live_trades(self,data):
		if self.currency == "btcusd":
			channel1 = "live_trades"
		else:
			channel1 = "live_trades_"+self.currency
		#print (channel1)
		channel = self.pusher.subscribe(channel1)
		channel.bind('trade', self.callback)

	#callback function for pusher
	def callback(self,data):
		print(data)

	#function to get ticker of speficied tradepair
	def live_ticker(self,tradepair):
		self.currency = BistampWebsocket.listOfTradingPairs.get(tradepair)
		self.pusher.connection.bind('pusher:connection_established', self.connect_handler_live_trades)
		self.pusher.connect()
		while True:
			time.sleep(1)
		print("finished")


		
if __name__ == "__main__":
	# Variables.
	channels=['BTC-USD','BTC-EUR']
	threads=[]
	k = BistampWebsocket(channels=channels)
	for c in k.channels:
		t = threading.Thread(target=k.live_ticker,args=(c,))
		threads.append(t)
		t.daemon=True
		t.start()
	x=input("Press any key to exit")
