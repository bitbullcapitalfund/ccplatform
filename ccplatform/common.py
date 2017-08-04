# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:27:21 2017

@author: Paúl Herrera
"""

class PubSubPattern():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers = []

    def publish(self, message):
        for s in self.subscribers:
            s.receive(message)
            
    def receive(self, message):
        raise NotImplementedError
    
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    
    
            
    
