from flask import make_response, request
from flask_restful import Resource
from injector import inject
from traffic.app_logic.interfaces.traffic_application_interface import (
    TrafficApplicationInterface,
)
from traffic.app_logic.exceptions import TrafficApplicationException
from traffic.entities.traffic_query import TrafficQuery


class TrafficResource(Resource):
    @inject
    def __init__(self, traffic_app: TrafficApplicationInterface):
        self.traffic_app = traffic_app

    def post(self):
        query_data = request.form.to_dict()
        if not query_data:
            return {
                "error_type": "MISSING_PARAMETERS",
                "error_message": "La consulta no contiene todos los parametros requeridos",
            }
        try:
            query_data_dto = TrafficQuery(**query_data)
            query_data_dto.format()
            response_data = self.traffic_app.get_jams(query_data_dto)
        except TrafficApplicationException as e:
            return {
                "error_type": str(e.error_type),
                "error_message": str(e.message),
            }, 500

        if not response_data:
            return {
                "error_type": "QUERY_ERROR",
                "error_message": "No se pudo realizar la consulta sobre nuestra base de datos",
            }, 500

        response = make_response(response_data)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = True

        return response
