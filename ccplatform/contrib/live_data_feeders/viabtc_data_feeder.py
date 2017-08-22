# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 20:54:30 2017

@author: Paúl Herrera
"""
import requests
import logging
import json
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread
# Custom libraries.
# from libraries.common import PubSubPattern

class ViaBtcWebsocket():
    """
    Main class. Has all the websocket implementations.
    """
    listOfTradingPairs = {'BTC-CNY':'BTCCNY','BCC-BTC':'BCCBTC','LTC-CNY':'LTCCNY','ETH-CNY':'ETHCNY','ZEC-CNY':'ZECCNY'}
	
    def __init__(self, channels=[]):
        # Disabbling logging.
        self.channels=channels
        self.check_tradepair()
        logger = logging.getLogger()
        logger.disabled = True
        self.pub = Publisher(channels)
        # Populates the channels dictionary with all the different channels instances as values.
		
    def check_tradepair(self):
        for c in self.channels:
            if c in ViaBtcWebsocket.listOfTradingPairs.keys():
                pass
            else:
                self.channels.remove(c)
                print("{} is not ViaBtc TradePair List".format(c))
				
    def fetch_ticker(self, currency):
        url = "https://www.viabtc.com/api/v1/market/ticker"
        params = {'market':''+currency+''}
        response = requests.get(url=url,params=params)
        data = response.json()
        return data['data']
        
    def connect(self):
        while True:
            for c in channels:
                channel = Subscriber(c)
                self.pub.register(c, channel)
                tradepair = ViaBtcWebsocket.listOfTradingPairs.get(c)
                temp=self.fetch_ticker(tradepair)['ticker']
                if(self.fetch_ticker(tradepair)['ticker'] == temp):
                    pass
                else:
                    temp = self.fetch_ticker(tradepair)
                    channel.update(temp)
   


    
if __name__ == "__main__":
    # Variables.
    channels=['BTC-CNY','BCC-BTC']
    ws = ViaBtcWebsocket(channels=channels)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x=input("Press any key to exit")
    