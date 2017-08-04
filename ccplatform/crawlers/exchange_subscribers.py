import websocket
from websocket import create_connection


def pull_poloniex_data(currency_pair, key='', secret=''):
    ws = create_connection("wss://api.poloniex.com")
    ws.send('ticker')
    


def pull_bitfinex_data(currency_pair, key='', secret=''):
    pass

def pull_bitstamp_data(currency_pair, key='', secret=''):
    pass
def pull_okcoin_data(currency_pair, key='', secret=''):
    pass
def pull_huobi_data(currency_pair, key='', secret=''):
    pass

def pull_bittrex_data(currency_pair, key='', secret=''):
    pass

def pull_coinigy_data(currency_pair, key='', secret=''):
    pass
