# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 12:27:21 2017

@author: Paúl Herrera
"""
import sys


class Subscriber:
    def __init__(self, name=None):
        if not name:
            self.name = str(self.__class__).split(' ')[1].split("'")[1]
        else:
            self.name = name

    def update(self, message):
        # start new Thread in here to handle any task
        print('\n\n {} got message "{}"'.format(self.name, message))


class Publisher:
    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = {event: dict()
                       for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def get_events(self):
        return self.events

    def register(self, event, subscriber):
        self.get_subscribers(event)[subscriber] = subscriber.update

    def set_event(self, event):
        self.events[event] = dict()

    def unregister(self, event, subscriber):
        del self.get_subscribers(event)[subscriber]

    def dispatch(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


class PubSubPattern():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribers = []

    def publish(self, message):
        for s in self.subscribers:
            s.receive(message)

    def receive(self, message):
        raise NotImplementedError

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)


def get_arg(index, default=None):
    """
    Grabs a value from the command line or returns the default one.
    """
    try:
        return sys.argv[index]
    except IndexError:
        return default
