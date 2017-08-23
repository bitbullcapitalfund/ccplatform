# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 20:54:30 2017

@author: Paúl Herrera
"""

import os
import sys
import logging
import json

from socketclusterclient import Socketcluster
from ccplatform.coinigy.pub_sub import Publisher, Subscriber
from ccplatform.coinigy.websocket_thread import ConnectThread

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


class CoinigyWebsocket():
    """
    Main class. Has all the websocket implementations.
    """

    def __init__(self, key, secret, channels=[], reconnect=True):
        # Disabbling logging.
        logger = logging.getLogger()
        logger.disabled = True

        # API credentials.
        self.api_credentials = json.loads('{}')
        self.api_credentials["apiKey"] = key
        self.api_credentials["apiSecret"] = secret

        # Socket parameters.
        self.socket = Socketcluster.socket("wss://sc-02.coinigy.com/socketcluster/")
        self.socket.setreconnection(reconnect)

        self.pub = Publisher(channels)
        # Populates the channels dictionary with all the different channels instances as values.
        for c in channels:
            channel = Subscriber(c)
            self.pub.register(c, channel)
            self.socket.onchannel(c, self.onChannelMessage)

        # Connecting to socket.
        self.socket.setBasicListener(self.onconnect, self.ondisconnect,
                                     self.onConnectError)
        self.socket.setAuthenticationListener(self.onSetAuthentication,
                                              self.onAuthentication)

    def getChannels(self):
        channels = []
        for subscriber, callback in self.pub.get_subscribers().items():
            channels.append[subscriber]
        return channels

    def unSubscribe(self, event, channel):
        self.socket.unsubscribe(event)
        self.pub.unregister(event, channel)

    def subscribe(self, event, channel):
        self.socket.subscribe(event)
        self.pub.register(event, channel)
        self.socket.onchannel(event, self.onChannelMessage)

    def connect(self):
        self.socket.connect()

    def onconnect(self, socket):
        print('Connecting to websocket')

    def ondisconnect(self, socket):
        pass

    def onConnectError(self, socket, error):
        logging.info("On connect error got called")

    def onSetAuthentication(self, socket, token):
        logging.info("Token received " + token)
        socket.setAuthtoken(token)

    def onAuthentication(self, socket, isauthenticated):
        print('Authenticating user')
        logging.info("Authenticated is " + str(isauthenticated))
        socket.emitack("auth", self.api_credentials, self.ack)

    def ack(self, eventname, error, data):
        if not error:
            print('User succesfully autenticated')
        else:
            print('Error in authentication')
        # Subscribing for the exchanges channels.
        for channelName, channel in self.pub.get_events().items():
            print("Subscribing to channel: {}".format(channelName))
            self.socket.subscribeack(channelName, self.subscribedack)

    def subscribedack(self, eventname, error, data):
        if not error:
            print('Succesfully subscribed to channel {}'.format(eventname))

    def onChannelMessage(self, event, message):
        self.pub.dispatch(event, message)

    def print_message(self, key, error, message):
        print(message)


if __name__ == "__main__":
    # Variables.
    key = "7f30437f1a03e032b6d6b606db087024"
    secret = "8a412962096a60e2685e5058ebe76e4a"
    channels = [
        # 'TRADE-BTCE--BTC--USD',
        # 'TRADE-OK--BTC--CNY',
        # 'TRADE-BITF--BTC--USD',
        'TRADE-GDAX--BTC--USD',
        # 'TRADE-PLNX--USDT--BTC',
        # 'TRADE-BTRX--BTC--USDT',
        # 'TRADE-HUOB--BTC--CNY',
    ]

    # Connecting to websocket.
    ws = CoinigyWebsocket(key, secret, channels=channels, reconnect=True)
    connnectThread = ConnectThread(ws)
    connnectThread.setDaemon(True)
    connnectThread.start()
    x = input("Press any key to exit")
