from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

arhaan_api = Blueprint('arhaan_api', __name__, url_prefix='/api')
api = Api(arhaan_api)

class ArhaanAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Arhaan Memon",
                "age": 15,
                "classes": ["AP CSP", "AP Seminar", "AP BIO", "History", "Math 3b"],
                "Favorite Sport": {"Basketball": "Football"},
                "Favorite Countries": {"India", "France", "Switcherland"}
            })
    

api.add_resource(ArhaanAPI._A_Person, "/arhaan")