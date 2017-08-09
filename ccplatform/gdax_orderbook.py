# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:23:10 2017

@author: Paúl Herrera
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import gdax

from core.data_feeder import HistoricalDataFeeder, RealTimeFeeder
from core.strategy import DeviationStrategy
from core.trader import PaperTrader, RealTimeTrader
from core.order_book import Level3OrderBook, CumulativeOrderBook


def animate(i):
    global order_book
    plot_flag = True
    
    # Plotting.
    ask = float(order_book.current_ask)
    bid = float(order_book.current_bid)
    yAsk = [float(i) for i in order_book.current_data.keys() if float(i) >= ask]
    yBid = [float(i) for i in order_book.current_data.keys() if float(i) <= bid]
    xAsk = [v for k,v in order_book.current_data.items() if float(k) >= ask]
    xBid = [v for k,v in order_book.current_data.items() if float(k) <= bid]
    try:
        miny = int(np.percentile(yBid, 10))
        maxy = int(np.percentile(yAsk, 90))
        minx = 0
        maxx = int(np.percentile(xBid + xAsk , 90))
    # Avoids raising plotting errors before any data 
    # has been saved in the order book.
    except IndexError:
        plot_flag = False

    if plot_flag:
        ax1.clear()
        plt.ylim([miny, maxy])
        plt.xlim([minx, maxx])
        plt.title('GDAX exchange order book')
        plt.ylabel('Price')
        plt.xlabel('Volume')
        plt.barh(yAsk, xAsk, height=0.02, color='green')
        plt.barh(yBid, xBid, height=0.02, color='red')


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
    startDate = '2017-06-19'
    endDate = '2017-06-26'
    period = int(get_arg(2, 10))
    entry_std = float(get_arg(3, 0.5))
    exit_std = float(get_arg(4, 0.5))
    size = float(get_arg(5, 0.01))
  
    # Setting client and data.
    
    # Initializing objects.
    client = gdax.AuthenticatedClient(key, secret, passphrase)
    feeder = RealTimeFeeder()
    order_book = CumulativeOrderBook()
    strategy = DeviationStrategy(period=period, entry_std=entry_std, exit_std=exit_std)
    trader = RealTimeTrader(client, size=0.01)
    feeder.subscribe(order_book)
    order_book.subscribe(strategy)
    strategy.subscribe(trader)
    
    
    # Trade.
    feeder.start()
    print('Connected and waiting for data')
    
    # Figure
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    
    # Updating plot.
    ani = animation.FuncAnimation(fig, animate, interval=300)
    plt.show()
    
    
    
    
