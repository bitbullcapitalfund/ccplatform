import ccxt
import sys

listOfTradingPairs = {'BTC-USDT':'USDT/BTC','ETH-BTC':'BTC/ETH','ETH-USDT':'USDT/ETH','DGB-BTC':'BTC/DGB','LTC-BTC':'BTC/LTC','BTS-BTC':'BTC/BTS','XRP-BTC':'BTC/XRP','STRAT-BTC':'BTC/STRAT','SC-BTC':'BTC/SC','DASH-BTC':'BTC/DASH','LTC-USDT':'USDT/LTC','STR-BTC':'BTC/STR','ETC-BTC':'BTC/ETC','XRP-USDT':'USDT/XRP','DASH-USDT':'USDT/DASH','FCT-BTC':'BTC/FCT','POT-BTC':'BTC/POT','LSK-BTC':'BTC/LSK','LBC-BTC':'BTC/LBC','XEM-BTC':'BTC/XEM','NXT-USDT':'USDT/NXT','STR-USDT':'USDT/STR','XMR-BTC':'BTC/XMR','NXT-BTC':'BTC/NXT','ETC-USDT':'USDT/ETC','ZEC-BTC':'BTC/ZEC','GNT-BTC':'BTC/GNT','ZEC-USDT':'USDT/ZEC','STEEM-BTC':'BTC/STEEM','REP-BTC':'BTC/REP','XMR-USDT':'USDT/XMR','DOGE-BTC':'BTC/DOGE','LSK-ETH':'ETH/LSK','ARDR-BTC':'BTC/ARDR','DCR-BTC':'BTC/DCR','SYS-BTC':'BTC/SYS','GAME-BTC':'BTC/GAME','ZEC-ETH':'ETH/ZEC','MAID-BTC':'BTC/MAID','GNT-ETH':'ETH/GNT','ETC-ETH':'ETH/ETC','BCN-BTC':'BTC/BCN','AMP-BTC':'BTC/AMP','REP-USDT':'USDT/REP','GNO-BTC':'BTC/GNO','BURST-BTC':'BTC/BURST','EMC2-BTC':'BTC/EMC2','SJCX-BTC':'BTC/SJCX','VIA-BTC':'BTC/VIA','VTC-BTC':'BTC/VTC','REP-ETH':'ETH/REP','GNO-ETH':'ETH/GNO','BTM-BTC':'BTC/BTM','RADS-BTC':'BTC/RADS','EXP-BTC':'BTC/EXP','BLK-BTC':'BTC/BLK','CLAM-BTC':'BTC/CLAM','XCP-BTC':'BTC/XCP','FLDC-BTC':'BTC/FLDC','OMNI-BTC':'BTC/OMNI','STEEM-ETH':'ETH/STEEM','SBD-BTC':'BTC/SBD','NEOS-BTC':'BTC/NEOS','PASC-BTC':'BTC/PASC','VRC-BTC':'BTC/VRC','XBC-BTC':'BTC/XBC','BELA-BTC':'BTC/BELA','FLO-BTC':'BTC/FLO','NAV-BTC':'BTC/NAV','PPC-BTC':'BTC/PPC','HUC-BTC':'BTC/HUC','NAUT-BTC':'BTC/NAUT','NOTE-BTC':'BTC/NOTE','NMC-BTC':'BTC/NMC','BCY-BTC':'BTC/BCY','BTCD-BTC':'BTC/BTCD','NXC-BTC':'BTC/NXC','PINK-BTC':'BTC/PINK','LTC-XMR':'XMR/LTC','DASH-XMR':'XMR/DASH','XPM-BTC':'BTC/XPM','GRC-BTC':'BTC/GRC','RIC-BTC':'BTC/RIC','XVC-BTC':'BTC/XVC','ZEC-XMR':'XMR/ZEC','NXT-XMR':'XMR/NXT','BTCD-XMR':'XMR/BTCD','BLK-XMR':'XMR/BLK','MAID-XMR':'XMR/MAID','BCN-XMR':'XMR/BCN'}

def live_ticker(tradepair):
	global listOfTradingPairs
	print ("Ticker of Currency Pair",tradepair)
	if tradepair in listOfTradingPairs.keys():
		poloniex  = ccxt.poloniex ()
		poloniex.load_products ()
		tradepair = listOfTradingPairs.get(tradepair)
		temp = poloniex.fetch_ticker (tradepair)
		while True:
			if(poloniex.fetch_ticker (tradepair) == temp):
				pass
			else:
				temp = poloniex.fetch_ticker (tradepair)
				print (temp)
	else:
		print ("Currency Pair is not from the below list \n",listOfTradingPairs.keys())
		
live_ticker('BTC-USDT')