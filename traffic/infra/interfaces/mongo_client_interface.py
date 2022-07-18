from abc import ABC, abstractmethod


class MongoClientInterface(ABC):
    @abstractmethod
    def get_traffic_collection(self, collection: str):
        pass
