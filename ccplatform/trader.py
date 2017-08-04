# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:56:48 2017

@author: Paúl Herrera
"""

import pandas as pd


class Trader():
    """
    Abstract Base Class. A trader receives the signals from
    the strategy.
    """
    def notify(self, msg):
        raise NotImplementedError
        
    def publish(self, msg):
        for s in self.subscribers:
            s.receive(msg)        

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)


class PaperTrader(Trader):
    """
    Saves the signals in a pandas dataframe.
    """
    def __init__(self):
        super().__init__()
        self._columns = ['time', 'type', 'price']
        self.trades = pd.DataFrame(columns=self._columns)
        self.subscribers = []
        
    
    def notify(self, msg):
        self.trades = pd.concat([self.trades, pd.DataFrame([msg], 
                                              columns=self._columns)])
        self.publish(msg)
                    
    
class RealTimeTrader(Trader):
    """
    Trades in real time through the gdax API.
    It takes a client object as first initialization parameter, so a
    'sandbox' client could be passed.
    """
    def __init__(self, client, product='BTC-USD', size=0.01):
        self.client = client
        self.product = product
        self.size = size
        self.orderId = 0
        self.orderType = 'CLOSE'
        self.subscribers = []
        
    def receive(self, msg):
        print('\n\n')
        print(msg)
        print('\n\n')
        
        if msg[1] == 'BUY':
            r = self.client.buy(price=msg[2], size=self.size, 
                                product_id=self.product)
            try:
                self.orderId = r['id']
            except AttributeError:
                print(r)
            self.orderType = 'BUY'
        elif msg[1] == 'SELL':
            r = self.client.sell(price=msg[2], size=self.size, 
                                 product_id=self.product)
            try:
                self.orderId = r['id']
            except AttributeError:
                print(r)
            self.orderType = 'SELL'
        elif msg[1] == 'CLOSE':
            if self.orderType == 'BUY':
                r = self.client.sell(price=msg[2], size=self.size, 
                                     product_id=self.product)
            elif self.orderType == 'SELL':
                r = self.client.buy(price=msg[2], size=self.size, 
                                    product_id=self.product)
        self.publish(msg)
        
        
