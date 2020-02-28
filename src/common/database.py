import pymongo


class Database(object):
    # we want to use the same URI and database
    # so we define them outside of init function
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    # has to be static method if self is not in the parameter
    # this method can only be applied to Database class as a whole
    # and never to an instance of Database
    @staticmethod
    def initialize():
        # notice the param has to be Database.URI instead of just URI,
        # unless URI is defined inside of the method
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['zinan_test']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)