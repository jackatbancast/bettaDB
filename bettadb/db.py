import json

class NoEventLoop(NameError):
    pass

class DataStore:
    def __init__(self, filename=None, evt_loop=None, debug=False):
        if not evt_loop:
            raise NoEventLoop
        self.namespace = {}
        self.debug = debug
        self.evt_loop = evt_loop
        self.filename = filename
        if self.filename:
            self.import_file()
        
        if self.debug:
            self.evt_loop.on('.+', lambda *args, **kwargs: print("Args: %s\nKwargs:%s" % (args, kwargs)))
            self.evt_loop.on('log debug$', lambda message: print(message))
        self.evt_loop.on('insert$', self.insert)
        self.evt_loop.on('delete$', self.delete)
        self.evt_loop.on('find$', self.find)
        self.evt_loop.on('find\_one$', self.find_one)

    def commit(self, filename=None):
        out_filename = filename or self.filename
        if out_filename:
            try:
                with open(out_filename, 'wb') as f:
                    f.write(self.__toJSON(self.namespace))
            except:
                pass

    def import_file(self, filename=None):
        in_filename = filename or self.filename
        if in_filename:
            try:
                with open(in_filename, 'rb') as f:
                    self.namespace = self.__fromJSON(f.read())
            except:
                pass
           
    def __toJSON(self, code):
        #TODO: implement better conversion
        return json.dumps(code)

    def __fromJSON(self, code):
        #TODO: implement better conversion
        return json.loads(code)

    def insert(self, collection, document, callback=None, *args, **kwargs):
        if collection and document:
            if collection in self.namespace.keys():
                self.namespace[collection].append(document)
            else:
                self.namespace[collection] = [document]
            if callback:
                callback(None, document, *args, **kwargs)
        elif callback:
            callback(True, None, *args, **kwargs)
        
    def delete(self, collection, query, callback=None, *args, **kwargs):
        if collection in self.namespace.keys():
            doccount = 0
            for doc in self.namespace[collection]:
                match = True
                for key in query.keys():
                    if key in doc.keys() and query.get(key) == doc.get(key):
                        continue
                    else:
                        match = False
                        break
                if match:
                    self.namespace[collection].pop(self.namespace[collection].index(doc))
                    doccount += 1
            if callback:
                callback(None, doccount, *args, **kwargs)#(err, doccount)
            else:
                pass
        elif callback:
            callback(True, None, *args, **kwargs)

    def find(self, collection, query, callback, *args, **kwargs):
        if collection in self.namespace.keys():
            retval = []
            for doc in self.namespace[collection]:
                match=True
                for key in query.keys():
                    if key in doc.keys() and query.get(key) == doc.get(key):
                        continue
                    else:
                        match = False
                        break
                if match:
                    retval.append(doc)
            callback(None, retval, *args, **kwargs)
        else:
            callback(True, None, *args, **kwargs)

    def find_one(self, collection, query, callback, *args, **kwargs):
        if collection in self.namespace.keys():
            d = None
            for doc in self.namespace[collection]:
                match = True
                for key in query.keys():
                    if key in doc.keys() and query.get(key) == doc.get(key):
                        continue
                    else:
                        match = False
                        break
                if match:
                    d = doc
                    break
            callback(None, d, *args, **kwargs)
        else:
            callback(True, None, *args, **kwargs)
