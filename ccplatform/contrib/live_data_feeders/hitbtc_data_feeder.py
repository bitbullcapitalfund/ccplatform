# -*- coding: utf-8 -*-

import ccxt
import logging
import json
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread


class HitBtcWebsocket():
    """
    Main class. Has all the websocket implementations.
    """
    listOfTradingPairs = {'BTC-USD':'BTCUSD','BTC-EUR':'BTCEUR','LTC-BTC':'LTCBTC','LTC-USD':'LTCUSD','LTC-EUR':'LTCEUR','DSH-BTC':'DSHBTC','ETH-BTC':'ETHBTC','ETH-EUR':'ETHEUR','NXT-BTC':'NXTBTC','BCN-BTC':'BCNBTC','XDN-BTC':'XDNBTC','DOGE-BTC':'DOGEBTC','XMR-BTC':'XMRBTC','QCN-BTC':'QCNBTC','FCN-BTC':'FCNBTC','LSK-BTC':'LSKBTC','LSK-EUR':'LSKEUR','STEEM-BTC':'STEEMBTC','STEEM-EUR':'STEEMEUR','SBD-BTC':'SBDBTC','DASH-BTC':'DASHBTC','XEM-BTC':'XEMBTC','EMC-BTC':'EMCBTC','SC-BTC':'SCBTC','ARDR-BTC':'ARDRBTC','ZEC-BTC':'ZECBTC','WAVES-BTC':'WAVESBTC'}
	
    def __init__(self, channels=[]):
        
        self.channels=channels
        self.check_tradepair()
		# Disabbling logging.
        logger = logging.getLogger()
        logger.disabled = True
		
        self.hitbtc=ccxt.hitbtc()
        self.hitbtc.load_products()
        self.pub = Publisher(channels)
        
	#checking the existence of tradepair	
    def check_tradepair(self):
        for c in self.channels:
            if c in HitBtcWebsocket.listOfTradingPairs.keys():
                pass
            else:
                self.channels.remove(c)
                print("{} is not HitBtc TradePair List".format(c))
        
    def connect(self):
        while True:
            for c in channels:
                channel = Subscriber(c)
                self.pub.register(c, channel)
                tradepair = HitBtcWebsocket.listOfTradingPairs.get(c)
                temp=self.hitbtc.fetch_ticker(tradepair)
                if(self.hitbtc.fetch_ticker(tradepair) == temp):
                    pass
                else:
                    temp = self.hitbtc.fetch_ticker(tradepair)
                    channel.update(temp)
   


    
if __name__ == "__main__":
    # Variables.
    channels=['LTC-BTC','BTC-USD']
    ws = HitBtcWebsocket(channels=channels)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x=input("Press any key to exit")
    