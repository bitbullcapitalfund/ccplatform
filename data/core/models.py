# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:42:36 2017

@author: Paúl Herrera
"""

import numpy as np
import pandas as pd
import datetime as dt


class Strategy():
    """
    Abstract Base Class for strategies.
    """
    def __init__(self):
        self.subscribers = []
        self.accountState = 'CLOSE'
        self.ask = [0]
        self.bid = [0]
        
    
    def calculate (self, _time, price, _type):
        raise NotImplementedError
        
    
    def receive(self, msg):
        """
        Receives the msg and parses it.
        """
        # Using only the match type messages.
        if msg['type'] == 'match':
        
            # Parsing message.
            _type = 'bid' if msg['side'] == 'buy' else 'ask'
            price = float(msg['price'])
            
            try:
                _time = dt.datetime.strptime(msg['time'], "%Y-%m-%dT%H:%M:%S.%fZ")\
                              .replace(microsecond=0)
            except ValueError:
                _time = pd.to_datetime(msg['time'])
                
            # Invoking main calculation
            self.calculate(_time, price, _type)
        
        
    def publish(self, signal):
        for s in self.subscribers:
            s.receive(signal)
        self.accountState = signal[1]

                
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)    


class DeviationStrategy(Strategy):
    """
    Trading strategy that enters and exits the market when the price
    deviates X standard deviations from the Y period mean. 
    """
    def __init__(self, period=20, entry_std=2, exit_std=1):
        super().__init__()
        self.period = period
        self.entryStd = entry_std
        self.exitStd = exit_std
        self.lastAskTimestamp = dt.datetime(1975,1,1)
        self.lastBidTimestamp = dt.datetime(1975,1,1)

 
              
    def calculate(self, _time, price, _type):
        """
        Main method. It has the core logic of the strategy.
        """
        # Updating data.
        if (_type == 'sell') and (price != self.ask[-1]) \
        and (_time >= self.lastAskTimestamp + dt.timedelta(seconds=1)):
            self.ask.append(price)
            self.lastAskTimestamp = _time
        elif (_type == 'buy') and (price != self.bid[-1]) \
        and (_time >= self.lastBidTimestamp + dt.timedelta(seconds=1)):
            self.bid.append(price)
            self.lastBidTimestamp = _time
            
        # Entry logic.
        if self.accountState == 'CLOSE':
            # Mean calculations.
            if (len(self.ask) >= self.period + 1) and (_type == 'sell'):
                mean = np.mean(self.ask[-self.period:])
                std = np.std(self.ask[-self.period:])
                lowStd = mean - self.entryStd * std
                print('Ask Std Dev: {} - {}'.format(lowStd, price))
                if price < lowStd:
                    self.publish((_time, 'BUY', price))
        # Exit logic.
        elif self.accountState != 'CLOSE':
            if (len(self.bid) >= self.period + 1) and (_type == 'buy'):
                mean = np.mean(self.bid[-self.period:])
                std = np.std(self.bid[-self.period:])
                highStd = mean + self.exitStd * std
                print('Bid Std Dev: {} - {}'.format(highStd, price))
                if (price > highStd) & (self.accountState == 'BUY'):
                    self.publish((_time, 'CLOSE', price))
        
        
class TestStrategy(Strategy):
    def calculate(self, _time, price, _type):
        print(_time, price, _type)
        
