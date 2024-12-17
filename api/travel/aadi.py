from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

aadi_api = Blueprint('aadi_api', __name__, url_prefix='/api')
api = Api(aadi_api)

class AadiAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Aadi Bhat",
                "age": 15,
                "classes": ["AP CSP", "AP Chemistry", "AP Seminar", "AP Calculus AB", "World History", "Honors PoE"],
                "favorite": {
                    "color": "Red",
                    "food": "Noodles"
                }
            })
    

api.add_resource(AadiAPI._A_Person, "/people/aadi")