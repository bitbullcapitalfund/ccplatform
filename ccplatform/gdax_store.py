# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 16:24:22 2017

@author: Paúl Herrera
"""

import sys
import os

from data_feeder import GDAXFeeder
from mongo_handler import MyMongoClient


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
    collection_name = 'gdax_' + product

    # Initializing objects.
    # client = gdax.AuthenticatedClient(key, secret, passphrase)
    feeder = GDAXFeeder()
    try:
        db_user = 'Writeuser'
        db_password = os.environ['MONGO-WRITE-PASSWORD']
        host = 'mongodb://{}:{}@127.0.0.1'.format(db_user, db_password)
    except KeyError:
        host = 'localhost'
    db = MyMongoClient('cc_data', collection_name, host=host)
    feeder.pub.register('gdax_data', db)

    # Trade.
    feeder.start()
    print('Connected and waiting for data')
