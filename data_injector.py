#!/usr/bin/python3

from pymongo import MongoClient
from shapely.geometry import Point, shape
import requests
import datetime
import json


class TomTomIncidentRequest:
    def __init__(self, api_key):
        self.city_coordenates = "-70.805086,-33.538223,-70.525680,-33.364616"
        self.api_key = api_key
        self.url = "https://api.tomtom.com/traffic/services/5/incidentDetails"
        with open("/home/ubuntu/cron/comunasChile.geojson") as f:
            self.geojson = json.load(f)

    def call_api(self):
        payload = {
            "bbox": self.city_coordenates,
            "language": "es-ES",
            "fields": "{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,events{description,code,iconCategory},startTime,endTime,from,to,length,delay,roadNumbers,timeValidity}}}",
            "key": self.api_key,
        }
        req = requests.get(self.url, params=payload)
        return req

    def get_comuna(self, raw_point):
        point = Point(raw_point)
        for feature in self.geojson["features"]:
            polygon = shape(feature["geometry"])
            if polygon.contains(point):
                return feature["properties"]["COMUNA"]

    def complete_comunas(self, incidents):
        for incident in incidents:
            incident["properties"]["comuna"] = self.get_comuna(
                incident["geometry"]["coordinates"][0]
            )
        return incidents


class ConnectMongo(object):
    @staticmethod
    def get_connection():
        return MongoClient("mongodb://")


class DataInjector:
    def __init__(self, api_key):
        self.db_connection = ConnectMongo.get_connection()
        self.api_connection = TomTomIncidentRequest(api_key)

    def inject(self):
        db = self.db_connection.traffic_db
        traffic = db.traffic
        raw_incidents = self.api_connection.call_api()
        incidents = self.api_connection.complete_comunas(
            raw_incidents.json().get("incidents")
        )
        new_traffic_document = {
            "date": datetime.datetime.utcnow(),
            "incidents": incidents,
        }
        traffic.insert_one(new_traffic_document)


if __name__ == "__main__":
    inyector = DataInjector("<key>")
    inyector.inject()
