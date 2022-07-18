from flask import Flask
from flask_injector import FlaskInjector
from flask_restful import Api
from injector import inject
from traffic.app_logic.interfaces.traffic_application_interface import (
    TrafficApplicationInterface,
)
from dependencies import configure
from traffic.resources.traffic_resource import TrafficResource


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(TrafficResource, "/traffic/")
    FlaskInjector(app=app, modules=[configure])
    return app
