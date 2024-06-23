from pymongo import MongoClient
from bson import ObjectId, json_util
import json

class Product:
    def __init__(self, db):
        self.collection = db['products']

    def get_all(self):
        return list(json.loads(json_util.dumps(self.collection.find())))
    
    def get_by_id(self, id):
        product = self.collection.find_one({"_id":ObjectId(id)})
        return json.loads(json_util.dumps(product))
    
    def add(self, data):
        return self.collection.insert_one(data).inserted_id