# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:42:36 2017

@author: Paúl Herrera
"""

import numpy as np
import pandas as pd
import datetime as dt
import tensorflow.contrib.keras as k


class Strategy():
    """
    Abstract Base Class for strategies.
    """
    def __init__(self):
        self.subscribers = []
        self.accountState = 'CLOSE'
        self.ask = [0]
        self.bid = [0]
        self.lastAskTimestamp = dt.datetime(1975,1,1)
        self.lastBidTimestamp = dt.datetime(1975,1,1)
        
        setattr(self, 'prediction', getattr(self,'prediction'))
        
    
    def calculate (self, _time, price, _type):
        # Updating data.
        
        if (_type == 'ask') and (price != self.ask[-1]) \
        and (_time >= self.lastAskTimestamp + dt.timedelta(seconds=1)):    
            self.ask.append(price)
            self.lastAskTimestamp = _time
        elif (_type == 'bid') and (price != self.bid[-1]) \
        and (_time >= self.lastBidTimestamp + dt.timedelta(seconds=1)):
            self.bid.append(price)
            self.lastBidTimestamp = _time
        
        self.prediction(_time, price, _type)

    
    def prediction(self, _time, price, _type):
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

 
              
    def prediction(self, _time, price, _type):
        """
        Main method. It has the core logic of the strategy.
        """
        
        # Entry logic.
        if self.accountState == 'CLOSE':
            # Mean calculations.
            if (len(self.ask) > self.period) and (_type == 'ask'):
                mean = np.mean(self.ask[-self.period:])
                std = np.std(self.ask[-self.period:])
                lowStd = mean - self.entryStd * std
                print('Ask Std Dev: {} - {}'.format(lowStd, price))
                if price < lowStd:
                    self.publish((_time, 'BUY', price))
            elif (len(self.ask) < self.period) and (_type == 'ask'):
                print("Collecting initial data: {}/{}".format(len(self.ask),
                                                              self.period))
                
        # Exit logic.
        elif self.accountState != 'CLOSE':
            if (len(self.bid) >= self.period + 1) and (_type == 'bid'):
                mean = np.mean(self.bid[-self.period:])
                std = np.std(self.bid[-self.period:])
                highStd = mean + self.exitStd * std
                print('Bid Std Dev: {} - {}'.format(highStd, price))
                if (price > highStd) & (self.accountState == 'BUY'):
                    self.publish((_time, 'CLOSE', price))
        
        
class TestStrategy(Strategy):
    def calculate(self, _time, price, _type):
        print(_time, price, _type)
        

class MA30N5Strategy(Strategy):
    """
    Moving average Strategy. 
    this class return BUY or CLOSE depending on the probability that 
    the average price of the next five minutes would be greater than 
    the average price of the last 30 minutes. Base on RNN with LSTM.
    Cutpoint to buy 0.5
    @author: Rafael Arias
    """
    def __init__(self):
        super().__init__()
        self.data = []
        self.normalised = np.array([])
        self.model = k.models.load_model("trained_models/categorical_model_v006.h5")
        

    def receive(self,msg):
        _transaction,_type,_time,_price,_volume = self.json_parse(msg)
        
        if _transaction == "match":            
            if len(self.data) == 30:
                self.data.append(_price)
                self.data = self.data[1:]
                self.normalised = self.normalize_data()
            else:
                self.data.append(_price)
            
            print(len(self.data))
            self.prediction(_time,_price, _type)
        

    def prediction(self, _time, price, _type):
        """
        Return the signal BUY or CLOSE from the model. Injected Method.  
        :execute: publish method 
        """
        if len(self.normalised.shape) == 3:
            prediction = self.model.predict(self.normalised)
            result = "BUY" if np.argmax(prediction) == 1 else "CLOSE"
        else:
            result = "CLOSE"
        
        if (result == 'CLOSE') and (self.accountState == 'BUY'):
            self.publish((_time, result, price))
        if (result == 'BUY') and (self.accountState == 'CLOSE'):
            self.publish((_time, result, price))


    def normalize_data(self):
        """
        Transform the price vector into a normalize vector. (Px/P0 - 1) 
        :return: A array with dimetion [1,window,1] 
        """
        data = self.data
        p0 = data[0]        
        normalised = np.array([(pi/p0)-1 for pi in data])
        normalised = normalised[np.newaxis,:,np.newaxis] 
        return normalised
    
    def json_parse(self,json_string):
        """
        Parse JSON string to a Dictionary. JSON String only represent one point in the time.
        :param json_string: String with information abour the price
        :return: match or done, Bid or Ask, price, Volume
        """
        json_string = str(json_string).lower()
        json_string = json_string.replace("{","").replace("}","").replace("'","").replace(" ","")
        json_string = json_string.split(",")
        
        json_data = np.array([ p.split(":",1) for p in json_string])
        json_dict = {v[0]:v[1] for v in json_data}
                
        _transaction = json_dict.get('type')
        _type = 'bid' if json_dict.get('side') == "buy" else 'ask'
        _time = dt.datetime.strptime(json_dict.get('time'), "%Y-%m-%dt%H:%M:%S.%fz").replace(microsecond=0)
        try:
            _price = float(json_dict.get('price'))
        except TypeError:
            _price = 0
        try:
            _volume = float(json_dict.get('size'))
        except TypeError:
            _volume = 0
        
        return _transaction,_type,_time,_price,_volume
