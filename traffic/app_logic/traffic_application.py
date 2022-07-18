from injector import inject
from traffic.app_logic.interfaces.traffic_application_interface import (
    TrafficApplicationInterface,
)
from traffic.repository.interfaces.traffic_repository_interface import (
    TrafficRepositoryInterface,
)
from traffic.infra.interfaces.cluster_interface import ClusterInterface
import json
from map_config import map_for_comune
from traffic.entities.traffic_query import TrafficQuery


class TrafficApplication(TrafficApplicationInterface):
    @inject
    def __init__(
        self, traffic_repo: TrafficRepositoryInterface, cluster_client: ClusterInterface
    ):
        self.traffic_repo = traffic_repo
        self.cluster_client = cluster_client

    def get_jams(self, query_data: TrafficQuery):
        if query_data.start_time != None and query_data.finish_time != None:
            if query_data.commune == "ALL":
                (
                    points_to_cluster,
                    points_incident_length,
                    points_incident_delay,
                    points_incident_datetime,
                ) = self.traffic_repo.query_jams_by_date_and_range_time_no_commune(
                    query_data.start_date,
                    query_data.finish_date,
                    query_data.length,
                    query_data.delay,
                    query_data.start_time,
                    query_data.finish_time,
                )
            else:
                (
                    points_to_cluster,
                    points_incident_length,
                    points_incident_delay,
                    points_incident_datetime,
                ) = self.traffic_repo.query_jams_by_date_and_range_time(
                    query_data.start_date,
                    query_data.finish_date,
                    query_data.commune,
                    query_data.length,
                    query_data.delay,
                    query_data.start_time,
                    query_data.finish_time,
                )
        else:
            if query_data.commune == "ALL":
                (
                    points_to_cluster,
                    points_incident_length,
                    points_incident_delay,
                    points_incident_datetime,
                ) = self.traffic_repo.query_jams_by_date_no_commune(
                    query_data.start_date,
                    query_data.finish_date,
                    query_data.length,
                    query_data.delay,
                )
            else:
                (
                    points_to_cluster,
                    points_incident_length,
                    points_incident_delay,
                    points_incident_datetime,
                ) = self.traffic_repo.query_jams_by_date(
                    query_data.start_date,
                    query_data.finish_date,
                    query_data.commune,
                    query_data.length,
                    query_data.delay,
                )
        points_info_dict = {
            "point_incident_length": points_incident_length,
            "point_incident_delay": points_incident_delay,
            "points_incident_datetime": points_incident_datetime,
        }
        top_clusters_df = self.cluster_client.clusterize(
            points_info_dict, points_to_cluster, query_data.top_jams
        )
        response_data = json.loads(top_clusters_df.to_json())
        response_data.update({"map_config": map_for_comune[query_data.commune]})
        return response_data
