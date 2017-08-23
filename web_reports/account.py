# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:33:14 2017

@author: paulj
"""

import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pandas as pd
from os import environ


class CoinigyAccount:
    def __init__(self, key, secret, *args, **kwargs):
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': key,
            'X-API-SECRET': secret,
        }

        self.calls = {
            'activity': 'https://api.coinigy.com/api/v1/activity',
            'accounts': 'https://api.coinigy.com/api/v1/accounts',
            'balances': 'https://api.coinigy.com/api/v1/balances',
            'balanceHistory': 'https://api.coinigy.com/api/v1/balanceHistory',
            'ticker': 'https://api.coinigy.com/api/v1/ticker',
        }

        self.auth_ids = {}

    def call(self, name, data=None):
        if data:
            return requests.post(self.calls[name],
                                 headers=self.headers,
                                 data=data)
        else:
            return requests.post(self.calls[name], headers=self.headers)

    def get_bitcoin_price(self):
        data = """
            {
            "exchange_code": "GDAX",
            "exchange_market": "BTC/USD"
            }
        """
        r = self.call('ticker', data)
        r = json.loads(r.text)
        price = r['data'][0]['last_trade']
        return float(price)

    def get_altcoins_balance(self, date=None, avoid=[]):
        """
        Returns as DataFrame with the balance in USD
        for each altcoin.
        """
        if date:
            btc_price = self.get_bitcoin_price()
            data = '{"date": "' + date + '"}'
            r = self.call('balanceHistory', data)
            r = json.loads(r.text)
            r = r['data']['balance_history']
            balances = {}
            # Sums the balance for each account in a dictionary.
            for i in r:
                if i['auth_id'] not in avoid:
                    try:
                        balances[i['balance_curr_code']] += float(i['btc_value']) * btc_price
                    except KeyError:
                        balances[i['balance_curr_code']] = float(i['btc_value']) * btc_price
            return pd.DataFrame(balances, index=[date])
        # If a date is not included, it returns the complete historical data.
        else:
            today = dt.date.today()
            balances = self.get_altcoins_balance(date=today.isoformat())
            print('Getting data for: {}'.format(today.isoformat()))
            counter = 1
            self.dates = []
            # Loop to get each one of the days.
            while True:
                date = (today - dt.timedelta(days=counter)).isoformat()
                print('Getting data for: {}'.format(date))
                b = self.get_altcoins_balance(date=date)
                # Continues looping only if a balance greater than 0
                # is returned.
                if len(b.columns) > 0:
                    balances = pd.concat([b, balances])
                    counter += 1
                else:
                    return balances

    def get_total_balance(self, date=None):
        """
        Returns a float or a list of floats with the account balance
        """
        if date:
            btc_price = self.get_bitcoin_price()
            data = '{"date": "' + date + '"}'
            r = self.call('balanceHistory', data)
            r = json.loads(r.text)
            r = r['data']['balance_history']
            balances = [float(x['btc_value']) * btc_price for x in r]
            return sum(balances)
        # If a date is not included, it returns the complete historical data.
        else:
            counter = 0
            today = dt.date.today()
            balance = []
            self.dates = []
            # Loop to get each one of the days.
            while True:
                date = (today - dt.timedelta(days=counter)).isoformat()
                print('Getting data for: {}'.format(date))
                b = self.get_total_balance(date=date)
                # Continues looping only if a balance greater than 0
                # is returned.
                if b > 0:
                    self.dates.append(date)
                    balance.append(b)
                    counter += 1
                else:
                    self.dates.reverse()
                    balance.reverse()
                    return balance


class CoinigyAccountPlotter:
    def __init__(self, key, secret):
        self.account = CoinigyAccount(key, secret)

    def plot_altcoins_balance(self, avoid=[]):
        balance = self.account.get_altcoins_balance(avoid=avoid)
        sns.set_style('white')
        balance.plot(figsize=(15, 12), title='Fund balance per altcoin', fontsize=16, linewidth=3)

    def plot_fund_balance(self):
        balance = self.account.get_total_balance()
        sns.set(rc={'axes.facecolor': '#A5CADD'})
        # fig = plt.figure(figsize=(15, 12))
        plt.plot(balance, linewidth=5, color='#961313')
        x = range(len(self.account.dates))
        plt.xticks(x, self.account.dates, fontsize=17, color='#C1726D')
        plt.yticks(fontsize=17, color='#C1726D')
        plt.title('Historical Fund Balance in USD \n', fontsize=22, color='#961313')
        plt.show()


if __name__ == "__main__":
    # Varaibles.
    key = environ['LANDON-BITTREX-KEY']
    secret = environ['LANDON-BITTREX-SECRET']

    # Initializations.
    plotter = CoinigyAccountPlotter(key, secret)
    plotter.plot_altcoins_balance(avoid=['55245', ])
    plotter.plot_fund_balance()

    # Plotting.
