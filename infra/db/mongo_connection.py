import pymongo
import os


# write singleton mongodb connection class
class MongoConnection:
    __instance = None
    __client = None
    __db = None

    @staticmethod
    def getInstance():
        if MongoConnection.__instance == None:
            MongoConnection()
        return MongoConnection.__instance

    def __init__(self):
        if MongoConnection.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoConnection.__instance = self
            MongoConnection.__client = pymongo.MongoClient(os.getenv("MONGODB_URL"))
            MongoConnection.__db = MongoConnection.__client[os.getenv("MONGODB_NAME")]

    def get_db(self):
        return MongoConnection.__db
