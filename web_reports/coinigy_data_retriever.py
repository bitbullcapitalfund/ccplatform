#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 07:38:26 2017

@author: paulj
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime as dt
import json
import requests
from pprint import pprint
from time import sleep

from ccplatform.common import get_arg
from ccplatform.mongo_handler import MyMongoClient
from account import CoinigyAccount


def get_balances():
    return json.loads(account.call('balances').text)


if __name__ == "__main__":
    # Variables.
    db_name = 'cc_data'
    trader = get_arg(1, 'LANDON') #'LANDON', 'CHRISTIAN' OR 'VIVEK.
    time_between_calls = dt.timedelta(seconds=get_arg(2, 300))
    key = os.environ['{}-BITTREX-KEY'.format(trader)]
    secret = os.environ['{}-BITTREX-SECRET'.format(trader)]
    collection = '{}_coinigy_account'.format(trader)
    try:
        db_user = 'Writeuser'
        db_password = os.environ['MONGO-WRITE-PASSWORD']
        host = 'mongodb://{}:{}@127.0.0.1'.format(db_user, db_password)
    except KeyError:
        host = 'localhost'
    
    # Component initialization.
    account = CoinigyAccount(key, secret)
    db = MyMongoClient(db_name, collection_name=collection,
                       host=host)
    
    # Time setting.
    next_call = dt.datetime.now()
    
    # Main loop.
    while True:
        now = dt.datetime.now()
        if now >= next_call:
            try:
                data = get_balances()
            except KeyError:
                print(data)
            except requests.exceptions.SSLError:
                continue
            except json.JSONDecodeError:
                continue
            except ConnectionError:
                sleep(600)
                continue
            data = data['data']
            # Inserts each coin as a document in the DB.    
            for d in data:
                d['time'] = now
                db.insert_one(d)
            next_call = now + time_between_calls
        
    
    