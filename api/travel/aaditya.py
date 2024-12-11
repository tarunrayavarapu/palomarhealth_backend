from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

aaditya_api = Blueprint('aaditya_api', __name__, url_prefix='/api')
api = Api(aaditya_api)

class AadityaAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Aaditya Taleppady",
                "age": 15,
                "favorite_vacations": ["India", "Colorado", "Mammoth", "Hawaii"],
                "favorite_sports_teams": ["49ers", "Warriors", "Padres"]
            })
    

api.add_resource(AadityaAPI._A_Person, "/aaditya")