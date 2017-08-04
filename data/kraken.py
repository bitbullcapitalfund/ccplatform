import ccxt
import sys

listOfTradingPairs = {'BTC-EUR':'BTC/EUR','ETH-USD':'ETH/USD','BTC-USD':'BTC/USD','ETH-EUR':'ETH/EUR','ETH-BTC':'ETH/BTC','LTC-EUR':'LTC/EUR','LTC-USD':'LTC/USD','ICN-BTC':'ICN/BTC','XRP-EUR':'XRP/EUR','LTC-BTC':'LTC/BTC','XRP-USD':'XRP/USD','ETC-EUR':'ETC/EUR','ICN-ETH':'ICN/ETH','DASH-USD':'DASH/USD','DASH-BTC':'DASH/BTC','DASH-EUR':'DASH/EUR','EOS-EUR':'EOS/EUR','ETC-USD':'ETC/USD','USDT-USD':'USDT/USD','XRP-BTC':'XRP/BTC','ETC-BTC':'ETC/BTC','ZEC-EUR':'ZEC/EUR','EOS-USD':'EOS/USD','XMR-EUR':'XMR/EUR','EOS-BTC':'EOS/BTC','XLM-EUR':'XLM/EUR','EOS-ETH':'EOS/ETH','XMR-BTC':'XMR/BTC','BTC-GBP':'BTC/GBP','XLM-BTC':'XLM/BTC','ETC-ETH':'ETC/ETH','ZEC-BTC':'ZEC/BTC','BTC-JPY':'BTC/JPY','XMR-USD':'XMR/USD','ZEC-USD':'ZEC/USD','REP-EUR':'REP/EUR','BTC-CAD':'BTC/CAD','REP-BTC':'REP/BTC','ETH-GBP':'ETH/GBP','ETH-JPY':'ETH/JPY','XLM-USD':'XLM/USD','ETH-CAD':'ETH/CAD','MLN-ETH':'MLN/ETH','REP-ETH':'REP/ETH','GNO-BTC':'GNO/BTC','REP-USD':'REP/USD','XRP-JPY':'XRP/JPY','GNO-EUR':'GNO/EUR','GNO-ETH':'GNO/ETH','GNO-USD':'GNO/USD','MLN-BTC':'MLN/BTC','XRP-CAD':'XRP/CAD'}

def live_ticker(tradepair):
	global listOfTradingPairs
	print ("Ticker of Currency Pair",tradepair)
	if tradepair in listOfTradingPairs.keys():
		kraken  = ccxt.kraken ()
		kraken.load_products ()
		tradepair = listOfTradingPairs.get(tradepair)
		temp = kraken.fetch_ticker (tradepair)
		while True:
			if(kraken.fetch_ticker (tradepair) == temp):
				pass
			else:
				temp = kraken.fetch_ticker (tradepair)
				print (temp)
	else:
		print ("Currency Pair is not from the below list \n",listOfTradingPairs)
		

		
live_ticker('BTC-USD')
