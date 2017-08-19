# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:12:38 2017

@author: Paúl Herrera
"""

import pymongo
import threading
from common import Subscriber

class MyMongoClient(Subscriber):
    def __init__(self, db_name, collection_name, host='localhost', port=27017, *args, **kwargs):
        super().__init__(name=db_name, *args, **kwargs)
        self._c = pymongo.MongoClient(host, port)
        self.set_database(db_name)
        self.set_collection(collection_name)
        
    def insert_one(self, data):
        self.collection.insert_one(data)
        print('Inserted: \n{}'.format(data))
        
    def update(self, msg):
        t = threading.Thread(target=self.insert_one, args=(msg,))
        t.start()
        
    def set_collection(self, collection_name):
        self.collection = self.database[collection_name]
        
    def set_database(self, db_name):
        self.database = self._c[db_name]
