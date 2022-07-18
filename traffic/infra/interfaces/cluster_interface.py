from abc import ABC, abstractmethod


class ClusterInterface(ABC):
    @abstractmethod
    def clusterize(self, points_info_dict, points_to_cluster, top_jams):
        pass
