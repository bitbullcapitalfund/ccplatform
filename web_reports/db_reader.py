# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 08:33:47 2017

@author: paulj
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import datetime as dt
import pandas as pd
import seaborn as sns
import json
from pprint import pprint

from ccplatform.common import get_arg
from ccplatform.mongo_handler import MyMongoClient
from account import CoinigyAccount


class CoinigyDB(MyMongoClient):
    def __init__(self, db_name='cc_data', collection_name='coinigy_account',
                 host='localhost', port=27017, *args, **kwargs):
        super().__init__(db_name, collection_name, host, port, *args, **kwargs)
        self._account = CoinigyAccount(key, secret)
        self.altcoins = db.collection.find().distinct("balance_curr_code")

    def get_altcoin_hist(self, currency='USD',
                         granularity=3600):
        btc_price = self._account.get_bitcoin_price()
        # Querying.
        query = self.collection.find({'balance_curr_code': currency}).sort('_id', -1)
        balance = pd.DataFrame()
        # Populating dataframe.
        for q in query:
            b = pd.DataFrame(q, index=[q['time']])
            balance = pd.concat([b, balance])
        balance.drop(['time', '_id'], axis=1, inplace=True)
        # Resampling dataframe.
        balance = balance.resample('{}S'.format(granularity)).last().ffill()
        balance['pct_change'] = balance.btc_balance.astype(float).pct_change()
        balance['usd_balance'] = balance.btc_balance.astype(float) * btc_price

        return balance[['balance_curr_code', 'balance_amount_total',
                        'usd_balance', 'btc_balance', 'pct_change']]

    def get_altcoins_balance(self, pct_time=60):
        balances = pd.DataFrame()
        for a in self.altcoins:
            print('Getting {} data.'.format(a))
            b = db.get_altcoin_hist(a, pct_time * 60)
            balances = pd.concat([balances, b.iloc[-1, :].to_frame().transpose()],
                                 axis=0)
        return balances.reset_index(drop=True)


if __name__ == "__main__":
    # Varaibles.
    key = os.environ['CHRISTIAN-BITTREX-KEY']
    secret = os.environ['CHRISTIAN-BITTREX-SECRET']

    # Initializations.
    db = CoinigyDB(key, secret)
    balance = db.get_altcoins_balance()
    balance_hist = db.get_altcoin_hist()
    print(balance)

    # Plotting
    sns.set_style('whitegrid')
    fig = sns.plt.figure(figsize=(15, 12))
    sns.barplot(x=balance.balance_curr_code, y=balance['pct_change'])
    sns.plt.title('Percentage change')
    sns.plt.show()
