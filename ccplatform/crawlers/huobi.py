import ccxt
import sys

listOfTradingPairs = {'BTC-CNY':'BTC/CNY','LTC-CNY':'LTC/CNY'}
def live_ticker(tradepair):
	global listOfTradingPairs
	print ("Ticker of Currency Pair",tradepair)
	if tradepair in listOfTradingPairs.keys():
		huobi  = ccxt.huobi ()
		huobi.load_products ()
		tradepair = listOfTradingPairs.get(tradepair)
		temp = huobi.fetch_ticker (tradepair)
		while True:
			if(huobi.fetch_ticker (tradepair) == temp):
				pass
			else:
				temp = huobi.fetch_ticker (tradepair)
				print (temp)
	else:
		print ("Currency Pair is not from the below list \n",listOfTradingPairs.keys())
		

live_ticker('BTC-CNY')