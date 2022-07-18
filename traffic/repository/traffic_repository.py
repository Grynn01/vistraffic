from dataclasses import make_dataclass

from injector import inject
from traffic.repository.interfaces.traffic_repository_interface import (
    TrafficRepositoryInterface,
)
from traffic.infra.interfaces.mongo_client_interface import MongoClientInterface


class TrafficRepository(TrafficRepositoryInterface):
    @inject
    def __init__(self, mongo_client: MongoClientInterface) -> None:
        self.mongo_client = mongo_client

    def query_jams_by_date(self, start_date, finish_date, commune, length, delay):
        pipeline = [
            {"$unwind": {"path": "$incidents"}},
            {
                "$match": {
                    "incidents.properties.iconCategory": 6,
                    "incidents.properties.comuna": commune,
                    "incidents.properties.length": {"$gte": length},
                    "incidents.properties.delay": {"$gte": delay},
                    "date": {"$gte": start_date, "$lt": finish_date},
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "date": {"$first": "$date"},
                    "incidents": {"$push": "$incidents"},
                }
            },
        ]

        return self._query_db(pipeline)

    def query_jams_by_date_no_commune(self, start_date, finish_date, length, delay):
        pipeline = [
            {"$unwind": {"path": "$incidents"}},
            {
                "$match": {
                    "incidents.properties.iconCategory": 6,
                    "incidents.properties.length": {"$gte": length},
                    "incidents.properties.delay": {"$gte": delay},
                    "date": {"$gte": start_date, "$lt": finish_date},
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "date": {"$first": "$date"},
                    "incidents": {"$push": "$incidents"},
                }
            },
        ]

        return self._query_db(pipeline)

    def query_jams_by_date_and_range_time(
        self, start_date, finish_date, commune, length, delay, init_time, finish_time
    ):
        pipeline = [
            {"$unwind": {"path": "$incidents"}},
            {
                "$match": {
                    "incidents.properties.iconCategory": 6,
                    "incidents.properties.comuna": commune,
                    "incidents.properties.length": {"$gte": length},
                    "incidents.properties.delay": {"$gte": delay},
                    "date": {"$gte": start_date, "$lt": finish_date},
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "date": {"$first": "$date"},
                    "incidents": {"$push": "$incidents"},
                }
            },
            {
                "$redact": {
                    "$cond": {
                        "if": {
                            "$and": [
                                {"$gte": [{"$hour": "$date"}, init_time]},
                                {"$lt": [{"$hour": "$date"}, finish_time]},
                            ]
                        },
                        "then": "$$KEEP",
                        "else": "$$PRUNE",
                    }
                }
            },
        ]

        return self._query_db(pipeline)

    def query_jams_by_date_and_range_time_no_commune(
        self, start_date, finish_date, length, delay, init_time, finish_time
    ):
        pipeline = [
            {"$unwind": {"path": "$incidents"}},
            {
                "$match": {
                    "incidents.properties.iconCategory": 6,
                    "incidents.properties.length": {"$gte": length},
                    "incidents.properties.delay": {"$gte": delay},
                    "date": {"$gte": start_date, "$lt": finish_date},
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "date": {"$first": "$date"},
                    "incidents": {"$push": "$incidents"},
                }
            },
            {
                "$redact": {
                    "$cond": {
                        "if": {
                            "$and": [
                                {"$gte": [{"$hour": "$date"}, init_time]},
                                {"$lt": [{"$hour": "$date"}, finish_time]},
                            ]
                        },
                        "then": "$$KEEP",
                        "else": "$$PRUNE",
                    }
                }
            },
        ]

        return self._query_db(pipeline)

    def _query_db(self, pipeline):
        points_to_cluster = []
        points_incident_length = []
        points_incident_delay = []
        points_incident_datetime = []
        Point = make_dataclass("Point", [("x", float), ("y", float)])
        snaps = self.mongo_client.get_traffic_collection("traffic").aggregate(
            pipeline, allowDiskUse=True
        )
        for snap in snaps:
            incidents = snap.get("incidents")
            incidents_datetime = snap.get("date")
            for incident in incidents:
                point_list = incident.get("geometry").get("coordinates")
                incident_length = incident.get("properties").get("length")
                incident_delay = incident.get("properties").get("delay")
                for point in point_list:
                    points_to_cluster.append(Point(point[0], point[1]))
                    points_incident_length.append(incident_length)
                    points_incident_delay.append(incident_delay)
                    points_incident_datetime.append(incidents_datetime)

        return (
            points_to_cluster,
            points_incident_length,
            points_incident_delay,
            points_incident_datetime,
        )
