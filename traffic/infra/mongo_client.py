from injector import inject
from pymongo import MongoClient
from traffic.infra.interfaces.mongo_client_interface import MongoClientInterface


class MongoConnection(MongoClientInterface):
    @inject
    def __init__(self):
        self.client = MongoClient(
            "mongodb://superusertmr:timer123@ec2-3-21-134-158.us-east-2.compute.amazonaws.com:27017/?authSource=admin"
        )

    def get_traffic_collection(self, collection: str):
        return self.client["traffic_db"][collection]
