# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 18:57:06 2017

@author: Paúl Herrera
"""

import matplotlib.pyplot as plt

import threading
import gdax


class OrderBook():
    """
    Order Book Abstract Base Class
    """
    def __init__(self, product='BTC-USD'):
        self._client = gdax.PublicClient()
        self.product = product
        self.subscribers = []
        
        # Updating order book.
        self.current_data = {}
        self.cumulative_data = []
        self._get_order_book()
        
        # Updating bid and ask.
        ticker = self._client.get_product_ticker(self.product)
        self.current_ask = ticker['ask']
        self.current_bid = ticker['bid']
    
    def _get_order_book(self):
        raise NotImplementedError
        
        
    def message_handler(self, msg):       
        raise NotImplementedError            
        
        
    def receive(self, msg):
        t = threading.Thread(target=self.message_handler, args=(msg,))
        t.start()

    
    def publish(self, msg):
        for s in self.subscribers:
            s.receive(msg)
            
        
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
        
        
class CumulativeOrderBook(OrderBook):
    def _get_order_book(self):
        pass
    
    def message_handler(self, msg):
        print(msg)
        if msg['type'] == 'match':
            tick = msg['price']
            print(tick)
            if (msg['side'] == 'sell'):
                data = (msg['time'], tick, 'ASK')
                self.cumulative_data.append(data)
                self.current_ask = tick
                self.publish(data)
            elif (msg['side'] == 'buy'):
                data = (msg['time'], tick, 'BID')
                self.cumulative_data.append(data)
                self.current_bid = tick
                self.publish(data)
            try:
                self.current_data[tick] += float(msg['size'])
            except KeyError:
                self.current_data[tick] = float(msg['size'])
        

class Level1OrderBook(OrderBook):
    def _get_order_book(self):
        pass
    
    def message_handler(self, msg):
        if msg['type'] == 'match':
            tick = msg['price']
            if (msg['side'] == 'sell'):
                data = (msg['time'], tick, 'ASK')
                self.cumulative_data.append(data)
                self.current_ask = tick
                self.publish(data)
            elif (msg['side'] == 'buy'):
                data = (msg['time'], tick, 'BID')
                self.cumulative_data.append(data)
                self.current_bid = tick
                self.publish(data)

    
class Level2OrderBook(OrderBook):
    def _get_order_book(self):
        ob = self._client.get_product_order_book(self.product, level=2)
        self.data.update({x[0]:float(x[1]) for x in ob['asks']})
        self.data.update({x[0]:float(x[1]) for x in ob['bids']})
    
    
class Level3OrderBook(OrderBook):
    def _get_order_book(self):
        ob = self._client.get_product_order_book(self.product, level=3)
        print('Updating current order book...')
        for i in ob['asks'] + ob['bids']:
            try: 
                self.current_data[i[0]] += float(i[1])
            except KeyError: 
                self.current_data[i[0]] = float(i[1])
        print('Order book updated. Collecting live data')
        

    def message_handler(self, msg):       
        if msg['type'] == 'match':
            tick = msg['price']
            if (msg['side'] == 'sell'):
                data = (msg['time'], tick, 'ASK')
                self.current_ask = tick
                self.publish(data)
            elif (msg['side'] == 'buy'):
                data = (msg['time'], tick, 'BID')
                self.current_bid = tick
                self.publish(data)
            try: 
                self.current_data[msg['price']] -= float(msg['remaining_size'])
                if self.current_data[msg['price']] < 0:
                    self.current_data[msg['price']] = 0
            except KeyError: 
                pass #self.data[msg['price']] = 0
        elif msg['type'] == 'open':
            try: 
                self.current_data[msg['price']] += float(msg['remaining_size'])
            except KeyError: 
                self.current_data[msg['price']] = float(msg['remaining_size'])
        elif (msg['type'] == 'done') and (msg['reason'] == 'canceled'):
            try: 
                self.current_data[msg['price']] -= float(msg['remaining_size'])
                if self.current_data[msg['price']] < 0:
                    self.current_data[msg['price']] = 0
            except KeyError: 
                pass #self.data[msg['price']] = 0
        
        self.cumulative_data.append(msg)
    

if __name__ == '__main__':
    ob = Level3OrderBook()
    barHeight = 0.4
    
    yask = [float(x) for x in list(ob.current_data.keys()) if float(x) >= float(ob.current_ask)]
    ybid = [float(x) for x in list(ob.current_data.keys()) if float(x) <= float(ob.current_bid)]
    xAsk = [v for k,v in ob.current_data.items() if float(k) >= float(ob.current_ask)]
    xBid = [v for k,v in ob.current_data.items() if float(k) <= float(ob.current_bid)]
    plt.barh(yask, xAsk, height=barHeight, color='green')
    plt.barh(ybid, xBid, height=barHeight, color='red')
    plt.ylim([2200, 2600])
    plt.xlim([0, 5])
    plt.title('GDAX exchange order book')
    plt.ylabel('Price')
    plt.xlabel('Volume')
    plt.show()
    
    