from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

tarun_api = Blueprint('_api', __name__, url_prefix='/api')
api = Api(tarun_api)

class TarunAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Tarun Rayavarapu",
                "age": 16,
                "classes": ["AP CSP", "AP Chemistry", "World History", "AP Calculus AB", "English"],
                "favorite": "Pizza, Pasta, Curry",
                "sports": "Soccer, Basketball",
                "Origin": "India"
            })
    

api.add_resource(TarunAPI._A_Person, "/tarun")
