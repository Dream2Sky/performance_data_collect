import threading
import configparser

import pymongo as mongo

from environment import environment
from utils import singleton

@singleton
class MongoDBClient(object):

    def __init__(self):
        self.mongo_config = environment.mongo_config
        self.connection_string = self.mongo_config.get_config("basic_db", "uri")
        self.mongo_client = mongo.MongoClient(self.connection_string)

    def init_db(self, db_config_name):
        db_name = self.mongo_config.get_config(db_config_name, "name")
        return self.mongo_client[db_name]


db_client = MongoDBClient()
fps_mongo_db = db_client.init_db("fps_mongo_db")
collect_mongo_db = db_client.init_db("collect_mongo_db")
