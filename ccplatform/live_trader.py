# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:23:10 2017

@author: Paúl Herrera
"""

import sys
import os
import gdax

from data_feeder import GDAXFeeder
import models
from trader import RealTimeTrader
from mongo_handler import MyMongoClient 


def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == '__main__':
    # Settig variables.
    key = 'c2c736241299f78327809504d2ffb0e7'
    secret = 'xzYSvcKvfP8Nx1uS+FxK7yWtoSfJplenN0vv9zGywfQcjTqEfqTmvGWsGixSQHCtkh9JdNoncEU1rEL1MXDWkA=='
    passphrase = 'si3b5hm7609'
    key = '9116261f62d68797d0d81a58a7b52936'
    secret = 'ccJBCbwaivcElWTA0g4n5pKmKCSpzYeE7Lac0cx4NuKfFn9BW0jOlZm76nLR3v90DmiUh4AjEp2vzw9uMeg49g=='
    passphrase = 'znp4ddpgxmb'        
    product = get_arg(1, 'BTC-USD')
    startDate = '2017-06-19'
    endDate = '2017-06-26'
    period = int(get_arg(2, 10))
    entry_std = float(get_arg(3, 0.5))
    exit_std = float(get_arg(4, 0.5))
    size = float(get_arg(5, 0.01))
  
    # Setting client and data.
#    data = pd.read_csv('BTC-USD_20170619-20170626.csv', index_col=0)

    
    # Initializing objects.
    client = gdax.AuthenticatedClient(key, secret, passphrase)
    strategy = models.DeviationStrategy(10, 1, 1)
    feeder = GDAXFeeder()
    trader = RealTimeTrader(client, product=product, size=0.01)
    
    # Initializing database.
    try:
        db_user = 'Writeuser'
        db_password = os.environ['MONGO-WRITE-PASSWORD']
        host = 'mongodb://{}:{}@127.0.0.1'.format(db_user, db_password)
    except KeyError:
        host = 'localhost'
    db = MyMongoClient('cc_trades', strategy.name, host=host)
    
    # Subscribing.
    feeder.subscribe(strategy)
    strategy.subscribe(trader)
    strategy.subscribe(db)
    
    # Backtest.
#    feeder.start()
    print('Connected and waiting for data')
    
    
    
    
