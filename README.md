bettaDB
=======

A better embedded Database, modelled on MongoDB

The database is event-driven, and based on top of [eventedpy](https://github.com/jackatbancast/eventedpy)

Usage
-----

Currently supported methods are insert, delete, find and find_one

    from bettadb.client import Client

    c = Client()

    c.insert(
        'test', #Collection
        {'hello': 'world'}, #Document
        lambda err, doc: print(doc) #Callback
    )
    #Prints {'hello': 'world'}

    print(c.datastore.namespace)
    #prints {'test': [{'hello': 'world'}]}
