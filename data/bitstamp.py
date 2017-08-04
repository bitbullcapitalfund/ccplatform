import pusherclient
import sys
import time

# Add a logging handler so we can see the raw communication data
import logging
import sys
#root = logging.getLogger()
#root.setLevel(logging.INFO)
#ch = logging.StreamHandler(sys.stdout)
#root.addHandler(ch)

global pusher

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler_live_trades(data):
	if currency == "btcusd":
		channel1 = "live_trades"
	else:
		channel1 = "live_trades_"+currency
	#print (channel1)
	channel = pusher.subscribe(channel1)
	channel.bind('trade', callback)

def connect_handler_order_book(data):
	if currency == "btcusd":
		channel1 = "order_book"
	else:
		channel1 = "order_book_"+currency
	print (channel1)
	channel = pusher.subscribe(channel1)
	channel.bind('data', callback)
	
def connect_handler_diff_order_book(data):
	if currency == "btcusd":
		channel1 = "diff_order_book"
	else:
		channel1 = "diff_order_book_"+currency
	print (channel1)
	channel = pusher.subscribe(channel1)
	channel.bind('data', callback)
	
def connect_handler_live_orders(data):
	if currency == "btcusd":
		channel1 = "live_orders"
	else:
		channel1 = "live_orders_"+currency
	print (channel1)
	channel = pusher.subscribe(channel1)
	channel.bind('order_created, order_changed or order_deleted', callback)

def callback(data):
	print (data)

def live_ticker(tradepair):
	global currency
	print ("Ticker of Currency Pair",tradepair)
	listOfTradingPairs = {'BTC-USD':'btcusd','BTC-EUR':'btceur','EUR-USD':'eurusd','XRP-USD':'xrpusd','XRP-EUR':'xrpeur','XRP-BTC':'xrpbtc','LTC-USD':'ltcusd','LTC-EUR':'ltceur','LTC-BTC':'ltcbtc'}
	currency = listOfTradingPairs.get(tradepair)
	if currency in listOfTradingPairs.values():
		pusher.connection.bind('pusher:connection_established', connect_handler_live_trades)
		#pusher.connection.bind('pusher:connection_established', connect_handler_order_book)
		#pusher.connection.bind('pusher:connection_established', connect_handler_diff_order_book)
		#pusher.connection.bind('pusher:connection_established', connect_handler_live_orders)
		pusher.connect()
		while True:
			time.sleep(1)
		print("finished")
	else:
		print ("Currency Pair is not from the below list \n",listOfTradingPairs.keys())
	
appkey = "de504dc5763aeef9ff52"
pusher = pusherclient.Pusher(appkey)
currency = ""
live_ticker('BTC-USD')