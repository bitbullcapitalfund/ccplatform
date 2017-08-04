# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:12:38 2017

@author: Paúl Herrera
"""

import pymongo


class MongoClient():
    def __init__(self, db_name, collection_name, host='localhost', port=27017, *args, **kwargs):
        self._c = pymongo.MongoClient(host, port)
        self.set_database(db_name)
        self.set_collection(collection_name)
        
    def receive(self, msg):
        self.collection.insert_one(msg)
        print(msg)
        
    def set_collection(self, collection_name):
        self.collection = self.database[collection_name]
        
    def set_database(self, db_name):
        self.database = self._c[db_name]
