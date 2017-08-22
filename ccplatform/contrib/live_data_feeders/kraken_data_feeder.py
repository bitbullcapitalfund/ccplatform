# -*- coding: utf-8 -*-

import ccxt
import logging
import json
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread


class KrakenWebsocket():
    """
    Main class. Has all the websocket implementations.
    """
    listOfTradingPairs = {'BTC-EUR':'BTC/EUR','ETH-USD':'ETH/USD','BTC-USD':'BTC/USD','ETH-EUR':'ETH/EUR','ETH-BTC':'ETH/BTC','LTC-EUR':'LTC/EUR','LTC-USD':'LTC/USD','ICN-BTC':'ICN/BTC','XRP-EUR':'XRP/EUR','LTC-BTC':'LTC/BTC','XRP-USD':'XRP/USD','ETC-EUR':'ETC/EUR','ICN-ETH':'ICN/ETH','DASH-USD':'DASH/USD','DASH-BTC':'DASH/BTC','DASH-EUR':'DASH/EUR','EOS-EUR':'EOS/EUR','ETC-USD':'ETC/USD','USDT-USD':'USDT/USD','XRP-BTC':'XRP/BTC','ETC-BTC':'ETC/BTC','ZEC-EUR':'ZEC/EUR','EOS-USD':'EOS/USD','XMR-EUR':'XMR/EUR','EOS-BTC':'EOS/BTC','XLM-EUR':'XLM/EUR','EOS-ETH':'EOS/ETH','XMR-BTC':'XMR/BTC','BTC-GBP':'BTC/GBP','XLM-BTC':'XLM/BTC','ETC-ETH':'ETC/ETH','ZEC-BTC':'ZEC/BTC','BTC-JPY':'BTC/JPY','XMR-USD':'XMR/USD','ZEC-USD':'ZEC/USD','REP-EUR':'REP/EUR','BTC-CAD':'BTC/CAD','REP-BTC':'REP/BTC','ETH-GBP':'ETH/GBP','ETH-JPY':'ETH/JPY','XLM-USD':'XLM/USD','ETH-CAD':'ETH/CAD','MLN-ETH':'MLN/ETH','REP-ETH':'REP/ETH','GNO-BTC':'GNO/BTC','REP-USD':'REP/USD','XRP-JPY':'XRP/JPY','GNO-EUR':'GNO/EUR','GNO-ETH':'GNO/ETH','GNO-USD':'GNO/USD','MLN-BTC':'MLN/BTC','XRP-CAD':'XRP/CAD'}
	
    def __init__(self, channels=[]):
        
        self.channels=channels
        self.check_tradepair()
		
		# Disabbling logging.
        logger = logging.getLogger()
        logger.disabled = True
		
        self.kraken=ccxt.kraken()
        self.kraken.load_products()
        self.pub = Publisher(channels)
        
	#checking the existence of tradepair	
    def check_tradepair(self):
        for c in self.channels:
            if c in KrakenWebsocket.listOfTradingPairs.keys():
                pass
            else:
                self.channels.remove(c)
                print("{} is not Bittrex TradePair List".format(c))
        
		
    def connect(self):
        while True:
            for c in channels:
                channel = Subscriber(c)
                self.pub.register(c, channel)
                tradepair = KrakenWebsocket.listOfTradingPairs.get(c)
                temp=self.kraken.fetch_ticker(tradepair)
                if(self.kraken.fetch_ticker(tradepair) == temp):
                    pass
                else:
                    temp = self.kraken.fetch_ticker(tradepair)
                    channel.update(temp)
   


    
if __name__ == "__main__":
    # Variables.
    channels=['BTC-EUR','ETH-USD']
    ws = KrakenWebsocket(channels=channels)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x=input("Press any key to exit")
    