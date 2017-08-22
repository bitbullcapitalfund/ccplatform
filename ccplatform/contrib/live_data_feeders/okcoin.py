import threading
import websocket
import time
import sys
import json
import hashlib
import zlib
import base64
import logging
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread

class OkCoinWebSocket():
	#dictionary of tradings supported by huobi
	listOfTradingPairs = {'BTC-USD':'btc','LTC-USD':'ltc','ETH-USD':'eth'}
	
	def __init__(self, channels=[]):
		self.channels=channels
		self.check_tradepair()
		self.api_key=''
		self.secret_key = ""
		self.url = "wss://real.okcoin.com:10440/websocket/okcoinapi"
		self.host = self.url
		self.tradepair=''
		self.ws=websocket.create_connection(self.host)
		# Disabbling logging.
		logger = logging.getLogger()
		logger.disabled = True

		self.pub = Publisher(channels)
	
	
	#checking the existence of tradepair	
	def check_tradepair(self):
		for c in self.channels:
			if c in OkCoinWebSocket.listOfTradingPairs.keys():
				pass
			else:
				self.channels.remove(c)
				print("{} is not OkCoin TradePair List".format(c))
	
	def ticker(self,c):
		lost=threading.local()
		lost.v=c
		currency = OkCoinWebSocket.listOfTradingPairs.get(lost.v)
		self.tradepair = "ok_sub_spotusd_"+currency+"_ticker"
		self.ws.send("{'event':'addChannel','channel':'"+self.tradepair+"'}")
		self.ws.recv()
		time.sleep(1)
		temp=self.receiver()
		channel = Subscriber(lost.v)
		self.pub.register(lost.v, channel)
		while True:
			if(self.receiver()==temp):
				pass
			else:
				temp=self.receiver()
				channel.update(temp)
		return
			
	def receiver(self):
		temp=json.loads(self.ws.recv())[0]
		try:
			del temp['data']['timestamp']
		except KeyError:
			pass
		return temp
	
		
if __name__ == "__main__":
    # Variables.
	channels=['BTC-USD','LTC-USD']
	threads=[]
	k = OkCoinWebSocket(channels=channels)
	print(k.channels)
	for c in k.channels:
		t = threading.Thread(target=k.ticker,args=(c,))
		threads.append(t)
		t.daemon=True
		t.start()
	x=input("Press any key to exit")