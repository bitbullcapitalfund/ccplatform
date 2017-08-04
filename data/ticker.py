# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:53:52 2017

@author: Paúl Herrera
"""

import sys

from core.data_feeder import RealTimeFeeder
from core.order_book import Level1OrderBook


def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == '__main__':
    # Settig variables.
    product = get_arg(1, 'BTC-USD')
     
    # Initializing objects.
    feeder = RealTimeFeeder()
    order_book = Level1OrderBook()
    feeder.subscribe(order_book)
    
    
    # Trade.
    feeder.start()
    print('Connected and waiting for data')
