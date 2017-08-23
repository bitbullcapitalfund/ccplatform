# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 20:54:30 2017

@author: Paúl Herrera
"""

import sys

from mongo_handler import MyMongoClient
from coinigy.coinigy_data_feeder import CoinigyWebsocket
from coinigy.websocket_thread import ConnectThread


def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == "__main__":
    # Variables.
    key = "67a4cf6b2800fb2a177693a61bff2b1a"
    secret = "8f756b95e898a8e42bbed7b0abb858d5"
    channel = get_arg(1, 'TRADE-GDAX--BTC--USD')
    db_name = 'cc_data'

    # Initializing websocket.
    ws = CoinigyWebsocket(key, secret, channels=[channel], reconnect=False)
    connnectThread = ConnectThread(ws)
    # connnectThread.setDaemon(True)

    # Setting database and subscriptions.
    db = MyMongoClient(db_name, collection_name=channel)
    ws.pub.register(channel, db)

    # Start connection.
    connnectThread.start()
    print('\nWaiting for connection')
