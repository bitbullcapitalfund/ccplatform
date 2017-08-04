# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:24:22 2017

@author: Paúl Herrera
"""

import sys
from core.data_feeder import RealTimeFeeder
from core.mongo_handler import MongoClient



def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == '__main__':
    # Settig variables.
    key = ''
    secret = ''
    passphrase = ''
    product = get_arg(1, 'BTC-USD')
    db_name = get_arg(2, 'gdax')
    collection_name = get_arg(3, 'BTCUSD')
      
    # Initializing objects.
#    client = gdax.AuthenticatedClient(key, secret, passphrase)
    feeder = RealTimeFeeder()
    db = MongoClient(db_name, collection_name)
    feeder.subscribe(db)   
    
    # Trade.
    feeder.start()
    print('Connected and waiting for data')
    
