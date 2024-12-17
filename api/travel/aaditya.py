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
                "classes": ["AP CSP", "AP Chemistry", "World History 1", "AP Calculus AB", "Offroll P5"],
                "favorite": {
                    "color": "Blue",
                    "food": "Pasta"
                }
            })
    

api.add_resource(AadityaAPI._A_Person, "/people/aaditya")