from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

tarun_api = Blueprint('tarun_api', __name__, url_prefix='/api')
api = Api(tarun_api)

class TarunAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Tarun Rayavarapu",
                "age": 16,
                "classes": ["AP CSP", "AP Chemistry", "World History", "AP Calculus AB", "English"],
                "favorite": {
                    "color": "Black",
                    "food": "Pizza, Pasta, Curry"
                }
            })
    

api.add_resource(TarunAPI._A_Person, "/people/tarun")
