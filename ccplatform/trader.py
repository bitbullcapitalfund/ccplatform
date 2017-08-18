# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:56:48 2017

@author: Paúl Herrera
"""

import pandas as pd
import gdax

from common import Subscriber, Publisher
from data_feeder import GDAXFeeder
import models
                    
    
class Trader(Subscriber):
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
        
    def update(self, msg):
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
        
        
if __name__ == '__main__':
    f = GDAXFeeder()
    s = models.Strategy()
    t = Trader(gdax.PublicClient())
    
    f.pub.register('gdax_data', s)
    s.pub.register('signals', t)
    
    f.start()    
        
        
