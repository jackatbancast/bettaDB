import eventedpy as e
from bettadb.db import DataStore

class Client:
    def __init__(self, datastore=None, filename=None, debug=True):
        self.evt_loop = e.EventLoop()
        self.datastore = datastore or DataStore(filename, self.evt_loop, debug)
        self.evt_loop.start()
        self.evt_loop.event('log debug', "DEBUG :: Client started")

    def insert(self, collection, document, callback=None):
        self.evt_loop.event('insert', collection, document, callback)

    def delete(self, collection, query, callback=None):
        self.evt_loop.event('delete', collection, query, callback)

    def find(self, collection, query, callback):
        self.evt_loop.event('find', collection, query, callback)

    def find_one(self, collection, query, callback):
        self.evt_loop.event('find_one', collection, query, callback)
