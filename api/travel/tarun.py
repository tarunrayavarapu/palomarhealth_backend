from flask import Blueprint, jsonify
from flask_restful import Api, Resource

tarun_api = Blueprint('tarun_api', __name__, url_prefix='/api')

api = Api(tarun_api)

class TarunAPI:
    @staticmethod
    def get_student():
        return {
            "name": "Tarun",
            "age": 24,
            "favorite_sport": "Basketball/Soccer",
            "origin": "India",
            "classes": "AP Chem, AP CSP, AP Calc AB, World History, English",
            "favorite food": "Pizza, Pasta, Curry"
            }

    class _Tarun(Resource):
        def get(self):
            tarun_details = TarunAPI.get_student()
            return jsonify(tarun_details)

    api.add_resource(_Tarun, '/student/tarun')

tarun_api_instance = TarunAPI()
