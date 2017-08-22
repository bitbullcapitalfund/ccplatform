# -*- coding: utf-8 -*-

import ccxt
import logging
import json
from pub_sub import Publisher, Subscriber
from websocket_thread import ConnectThread

class BittrexWebsocket():
    """
    Main class. Has all the websocket implementations.
    """
    listOfTradingPairs = {'BTC-USDT':'BTC/USDT','ETH-BTC':'ETH/BTC','ANS-BTC':'ANS/BTC','DGB-BTC':'DGB/BTC','STRAT-BTC':'STRAT/BTC','ETH-USDT':'ETH/USDT','LTC-BTC':'LTC/BTC','OMG-BTC':'OMG/BTC','SC-BTC':'SC/BTC','WAVES-BTC':'WAVES/BTC','DASH-BTC':'DASH/BTC','XRP-BTC':'XRP/BTC','CVC-BTC':'CVC/BTC','ANS-ETH':'ANS/ETH','SNT-BTC':'SNT/BTC','LBC-BTC':'LBC/BTC','PAY-BTC':'PAY/BTC','EMC2-BTC':'EMC2/BTC','LSK-BTC':'LSK/BTC','ETC-BTC':'ETC/BTC','BTS-BTC':'BTS/BTC','MTL-BTC':'MTL/BTC','XMR-BTC':'XMR/BTC','BAT-BTC':'BAT/BTC','XVG-BTC':'XVG/BTC','NXT-BTC':'NXT/BTC','XEM-BTC':'XEM/BTC','FCT-BTC':'FCT/BTC','QTUM-BTC':'QTUM/BTC','ZEC-BTC':'ZEC/BTC','GNT-BTC':'GNT/BTC','PIVX-BTC':'PIVX/BTC','ANT-BTC':'ANT/BTC','FUN-BTC':'FUN/BTC','LTC-USDT':'LTC/USDT','STEEM-BTC':'STEEM/BTC','NMR-BTC':'NMR/BTC','SNT-ETH':'SNT/ETH','LGD-BTC':'LGD/BTC','SNRG-BTC':'SNRG/BTC','ARDR-BTC':'ARDR/BTC','PAY-ETH':'PAY/ETH','XEL-BTC':'XEL/BTC','DOGE-BTC':'DOGE/BTC','GBYTE-BTC':'GBYTE/BTC','DGD-BTC':'DGD/BTC','LTC-ETH':'LTC/ETH','UBQ-BTC':'UBQ/BTC','DCR-BTC':'DCR/BTC','VOX-BTC':'VOX/BTC','KMD-BTC':'KMD/BTC','SWT-BTC':'SWT/BTC','GAME-BTC':'GAME/BTC','PART-BTC':'PART/BTC','ION-BTC':'ION/BTC','BLOCK-BTC':'BLOCK/BTC','OMG-ETH':'OMG/ETH','RDD-BTC':'RDD/BTC','EDG-BTC':'EDG/BTC','1ST-BTC':'1ST/BTC','SYS-BTC':'SYS/BTC','XRP-USDT':'XRP/USDT','PTOY-BTC':'PTOY/BTC','VTC-BTC':'VTC/BTC','XLM-BTC':'XLM/BTC','2GIVE-BTC':'2GIVE/BTC','CFI-BTC':'CFI/BTC','WINGS-BTC':'WINGS/BTC','CVC-ETH':'CVC/ETH','ARK-BTC':'ARK/BTC','DYN-BTC':'DYN/BTC','UNB-BTC':'UNB/BTC','BNT-BTC':'BNT/BTC','POT-BTC':'POT/BTC','HMQ-BTC':'HMQ/BTC','REP-BTC':'REP/BTC','DASH-USDT':'DASH/USDT','EBST-BTC':'EBST/BTC','ZEC-USDT':'ZEC/USDT','PDC-BTC':'PDC/BTC','RISE-BTC':'RISE/BTC','GBG-BTC':'GBG/BTC','RLC-BTC':'RLC/BTC','VIA-BTC':'VIA/BTC','SYNX-BTC':'SYNX/BTC','COVAL-BTC':'COVAL/BTC','AMP-BTC':'AMP/BTC','CLOAK-BTC':'CLOAK/BTC','DCT-BTC':'DCT/BTC','SNGLS-BTC':'SNGLS/BTC','QRL-BTC':'QRL/BTC','QTUM-ETH':'QTUM/ETH','SHIFT-BTC':'SHIFT/BTC','NXS-BTC':'NXS/BTC','ETC-USDT':'ETC/USDT','RADS-BTC':'RADS/BTC','GNT-ETH':'GNT/ETH','BNT-ETH':'BNT/ETH','DASH-ETH':'DASH/ETH','FUN-ETH':'FUN/ETH','XRP-ETH':'XRP/ETH','ETC-ETH':'ETC/ETH','XMR-USDT':'XMR/USDT','XZC-BTC':'XZC/BTC','STORJ-BTC':'STORJ/BTC','MCO-BTC':'MCO/BTC','MAID-BTC':'MAID/BTC','ABY-BTC':'ABY/BTC','ANT-ETH':'ANT/ETH','EXCL-BTC':'EXCL/BTC','FTC-BTC':'FTC/BTC','UNO-BTC':'UNO/BTC','DOPE-BTC':'DOPE/BTC','SPHR-BTC':'SPHR/BTC','NLG-BTC':'NLG/BTC','CRW-BTC':'CRW/BTC','TRST-BTC':'TRST/BTC','ZEN-BTC':'ZEN/BTC','SC-ETH':'SC/ETH','BLK-BTC':'BLK/BTC','BAT-ETH':'BAT/ETH','XAUR-BTC':'XAUR/BTC','MUE-BTC':'MUE/BTC','EXP-BTC':'EXP/BTC','GNO-BTC':'GNO/BTC','DTB-BTC':'DTB/BTC','MYST-BTC':'MYST/BTC','SBD-BTC':'SBD/BTC','THC-BTC':'THC/BTC','ZCL-BTC':'ZCL/BTC','PINK-BTC':'PINK/BTC','TX-BTC':'TX/BTC','ADX-BTC':'ADX/BTC','SWIFT-BTC':'SWIFT/BTC','BITB-BTC':'BITB/BTC','NEOS-BTC':'NEOS/BTC','BAY-BTC':'BAY/BTC','XDN-BTC':'XDN/BTC','MTL-ETH':'MTL/ETH','SPR-BTC':'SPR/BTC','MUSIC-BTC':'MUSIC/BTC','BSD-BTC':'BSD/BTC','BURST-BTC':'BURST/BTC','ADT-BTC':'ADT/BTC','DMD-BTC':'DMD/BTC','SIB-BTC':'SIB/BTC','NMR-ETH':'NMR/ETH','GRS-BTC':'GRS/BTC','ADX-ETH':'ADX/ETH','MONA-BTC':'MONA/BTC','XST-BTC':'XST/BTC','LUN-BTC':'LUN/BTC','XCP-BTC':'XCP/BTC','FLDC-BTC':'FLDC/BTC','VRC-BTC':'VRC/BTC','FLO-BTC':'FLO/BTC','GOLOS-BTC':'GOLOS/BTC','NAV-BTC':'NAV/BTC','GUP-BTC':'GUP/BTC','GAM-BTC':'GAM/BTC','OK-BTC':'OK/BTC','MLN-BTC':'MLN/BTC','ZEC-ETH':'ZEC/ETH','OMNI-BTC':'OMNI/BTC','TIME-BTC':'TIME/BTC','TKN-BTC':'TKN/BTC','APX-BTC':'APX/BTC','CFI-ETH':'CFI/ETH','EGC-BTC':'EGC/BTC','KORE-BTC':'KORE/BTC','FAIR-BTC':'FAIR/BTC','BCY-BTC':'BCY/BTC','BTCD-BTC':'BTCD/BTC','BTA-BTC':'BTA/BTC','MCO-ETH':'MCO/ETH','CPC-BTC':'CPC/BTC','QWARK-BTC':'QWARK/BTC','NAUT-BTC':'NAUT/BTC','NXC-BTC':'NXC/BTC','PPC-BTC':'PPC/BTC','INFX-BTC':'INFX/BTC','CANN-BTC':'CANN/BTC','TRUST-BTC':'TRUST/BTC','START-BTC':'START/BTC','VRM-BTC':'VRM/BTC','XEM-ETH':'XEM/ETH','PTOY-ETH':'PTOY/ETH','HMQ-ETH':'HMQ/ETH','CLUB-BTC':'CLUB/BTC','MYST-ETH':'MYST/ETH','AGRS-BTC':'AGRS/BTC','QRL-ETH':'QRL/ETH','RBY-BTC':'RBY/BTC','AUR-BTC':'AUR/BTC','1ST-ETH':'1ST/ETH','ENRG-BTC':'ENRG/BTC','DRACO-BTC':'DRACO/BTC','SNGLS-ETH':'SNGLS/ETH','ADT-ETH':'ADT/ETH','BRK-BTC':'BRK/BTC','SEQ-BTC':'SEQ/BTC','GEO-BTC':'GEO/BTC','XMR-ETH':'XMR/ETH','WINGS-ETH':'WINGS/ETH','IOC-BTC':'IOC/BTC','GRC-BTC':'GRC/BTC','STORJ-ETH':'STORJ/ETH','TRIG-BTC':'TRIG/BTC','CRB-BTC':'CRB/BTC','LMC-BTC':'LMC/BTC','LGD-ETH':'LGD/ETH','AEON-BTC':'AEON/BTC' ,'XMG-BTC':'XMG/BTC','CLAM-BTC':'CLAM/BTC','GLD-BTC':'GLD/BTC','TKS-BTC':'TKS/BTC','BYC-BTC':'BYC/BTC','DGD-ETH':'DGD/ETH','CURE-BTC':'CURE/BTC','HKG-BTC':'HKG/BTC','BRX-BTC':'BRX/BTC','XVC-BTC':'XVC/BTC','EMC-BTC':'EMC/BTC','GCR-BTC':'GCR/BTC','XWC-BTC':'XWC/BTC','PKB-BTC':'PKB/BTC','DAR-BTC':'DAR/BTC','LUN-ETH':'LUN/ETH','BLITZ-BTC':'BLITZ/BTC','EFL-BTC':'EFL/BTC','TKN-ETH':'TKN/ETH','IOP-BTC':'IOP/BTC','PTC-BTC':'PTC/BTC','XBB-BTC':'XBB/BTC','INCNT-BTC':'INCNT/BTC','VTR-BTC':'VTR/BTC','REP-ETH':'REP/ETH','RLC-ETH':'RLC/ETH','GNO-ETH':'GNO/ETH','SLS-BTC':'SLS/BTC','SLR-BTC':'SLR/BTC','BTC-BITCNY':'BTC/BITCNY','ERC-BTC':'ERC/BTC','TIME-ETH':'TIME/ETH','TRST-ETH':'TRST/ETH','GUP-ETH':'GUP/ETH','XLM-ETH':'XLM/ETH','CRB-ETH':'CRB/ETH'}
	
    def __init__(self, channels=[]):
        
        self.channels=channels
        self.check_tradepair()
		# Disabbling logging.
        logger = logging.getLogger()
        logger.disabled = True
        self.bittrex=ccxt.bittrex()
        self.bittrex.load_products()
        self.pub = Publisher(channels)
        
	#checking whether the requested tradepair is in Bittrex list	
    def check_tradepair(self):
        for c in self.channels:
            if c in BittrexWebsocket.listOfTradingPairs.keys():
                pass
            else:
                self.channels.remove(c)
                print("{} is not Bittrex TradePair List".format(c))
        
    def connect(self):
        while True:
            for c in channels:
                channel = Subscriber(c)
                self.pub.register(c, channel)
                tradepair = BittrexWebsocket.listOfTradingPairs.get(c)
                temp=self.bittrex.fetch_ticker(tradepair)
                if(self.bittrex.fetch_ticker(tradepair) == temp):
                    pass
                else:
                    temp = self.bittrex.fetch_ticker(tradepair)
                    channel.update(temp)
   


    
if __name__ == "__main__":
    # Variables.
    channels=['BTC-USDT','LTC-CNY']
    ws = BittrexWebsocket(channels=channels)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x=input("Press any key to exit")
    