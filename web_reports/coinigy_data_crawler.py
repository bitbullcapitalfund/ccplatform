# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:02:00 2017

@author: paulj
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ccplatform.mongo_handler import MyMongoClient
from ccplatform.coinigy.coinigy_data_feeder import CoinigyWebsocket
from ccplatform.coinigy.websocket_thread import ConnectThread


def get_arg(index, default):
    try:
        return sys.argv[index]
    except IndexError:
        return default


if __name__ == "__main__":
	# Variables.
    key = "1a0ffafcbaff2886c8212180bedcd49b"
    secret = "700320ef659ac9bf39e89202fce9ad12"
    channel = get_arg(1, '4AE7D052-0F85-C19E-09E1-4190EF8775CC')

    # Initializing websocket.
    ws = CoinigyWebsocket(key, secret, channels=[channel], reconnect=False)
    connnectThread = ConnectThread(ws)
    # connnectThread.setDaemon(True)

    # Setting database and subscriptions.
    db = MyMongoClient(db_name='coinigy_account_data', collection_name=channel)
    ws.pub.register(channel, db)
        
    # Start connection.
    connnectThread.start()
    print('\nWaiting for connection')