import eventedpy as e
from bettadb.db import DataStore

evt_loop = e.EventLoop()
datastore = DataStore(evt_loop=evt_loop)

class Client:
    def __init__(self, filename=None, debug=True):
        self.datastore = datastore
        self.datastore.debug = debug
        self.datastore.filename=filename
        self.evt_loop = evt_loop
        self.evt_loop.start()
        self.evt_loop.add(e.Event('log debug', message="DEBUG :: Client started"))

    def insert(self, collection, document, callback=None):
        self.evt_loop.add(e.Event('insert', collection, document, callback))

    def delete(self, collection, query, callback=None):
        self.evt_loop.add(e.Event('delete', collection, query, callback))

    def find(self, collection, query, callback):
        self.evt_loop.add(e.Event('find', collection, query, callback))

    def find_one(self, collection, query, callback):
        self.evt_loop.add(e.Event('find_one', collection, query, callback))
