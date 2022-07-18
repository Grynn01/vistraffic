from abc import ABC, abstractmethod


class TrafficApplicationInterface(ABC):
    @abstractmethod
    def get_jams(self, query_data: dict):
        pass
