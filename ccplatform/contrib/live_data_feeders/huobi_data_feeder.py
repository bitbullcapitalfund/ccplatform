# -*- coding: utf-8 -*-

import ccxt
import logging
import json
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread


class HuobiWebsocket():
    """
    Main class. Has all the websocket implementations.
    """
    listOfTradingPairs = {'BTC-CNY':'BTC/CNY','LTC-CNY':'LTC/CNY'}
	
    def __init__(self, channels=[]):
        
        self.channels=channels
        self.check_tradepair()
		
		# Disabbling logging.
        logger = logging.getLogger()
        logger.disabled = True
		
        self.huobi=ccxt.huobi()
        self.huobi.load_products()
        self.pub = Publisher(channels)
        
	#checking the existence of tradepair	
    def check_tradepair(self):
        for c in self.channels:
            if c in HuobiWebsocket.listOfTradingPairs.keys():
                pass
            else:
                self.channels.remove(c)
                print("{} is not Huboi TradePair List".format(c))
        
    def connect(self):
        while True:
            for c in channels:
                channel = Subscriber(c)
                self.pub.register(c, channel)
                tradepair = HuobiWebsocket.listOfTradingPairs.get(c)
                temp=self.huobi.fetch_ticker(tradepair)
                if(self.huobi.fetch_ticker(tradepair) == temp):
                    pass
                else:
                    temp = self.huobi.fetch_ticker(tradepair)
                    channel.update(temp)
   


    
if __name__ == "__main__":
    # Variables.
    channels=['BTC-NY','LTC-CNY']
    ws = HuobiWebsocket(channels=channels)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x=input("Press any key to exit")
    