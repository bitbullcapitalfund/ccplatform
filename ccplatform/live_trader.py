# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:23:10 2017

@author: Paúl Herrera
"""

import sys
import gdax

from data_feeder import GDAXFeeder
from models import MA30N5Strategy
from trader import RealTimeTrader    


def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == '__main__':
    # Settig variables.
    key = 'c2c736241299f78327809504d2ffb0e7 '
    secret = 'xzYSvcKvfP8Nx1uS+FxK7yWtoSfJplenN0vv9zGywfQcjTqEfqTmvGWsGixSQHCtkh9JdNoncEU1rEL1MXDWkA=='
    passphrase = 'si3b5hm7609'
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
    strategy = MA30N5Strategy()
    feeder = GDAXFeeder()
    trader = RealTimeTrader(client, product=product, size=0.01)
    feeder.subscribe(strategy)
    strategy.subscribe(trader)
    
    # Backtest.
    feeder.start()
    print('Connected and waiting for data')
    
    
    
    
