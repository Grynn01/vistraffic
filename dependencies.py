from injector import singleton
from traffic.app_logic.interfaces.traffic_application_interface import (
    TrafficApplicationInterface,
)
from traffic.app_logic.traffic_application import TrafficApplication
from traffic.repository.interfaces.traffic_repository_interface import (
    TrafficRepositoryInterface,
)
from traffic.repository.traffic_repository import TrafficRepository
from traffic.infra.interfaces.mongo_client_interface import MongoClientInterface
from traffic.infra.mongo_client import MongoConnection
from traffic.infra.interfaces.cluster_interface import ClusterInterface
from traffic.infra.cluster import Cluster


def configure(binder):
    binder.bind(TrafficApplicationInterface, to=TrafficApplication, scope=singleton)
    binder.bind(TrafficRepositoryInterface, to=TrafficRepository, scope=singleton)
    binder.bind(MongoClientInterface, to=MongoConnection, scope=singleton)
    binder.bind(ClusterInterface, to=Cluster, scope=singleton)
