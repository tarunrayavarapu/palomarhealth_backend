from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

kiruthic_api = Blueprint('kiruthic_api', __name__, url_prefix='/api')
api = Api(kiruthic_api)

class KiruthicAPI:
    class _A_Person(Resource):
        def get(self):
            return jsonify({
                "name": "Kiruthic Selvakumar",
                "age": 16,
                "classes": ["AP CSP", "AP Chemistry", "Honors Humanities", "AP Calculus AB", "AP World History"],
                "favorite": {
                    "food": "Pizza",
                    "color": "Blue",
                }
            })
    

api.add_resource(KiruthicAPI._A_Person, "/kiruthic")
