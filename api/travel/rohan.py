from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

rohan_api = Blueprint('rohan_api', __name__, url_prefix='/api')
api = Api(rohan_api)

class RohanAPI:
    class _BojjaAPI(Resource):
        def get(self):
            return jsonify({
                "name": "Rohan Bojja",
                "age": 15,
                "classes": ["AP CSP", "AP Chemistry", "AP World History", "AP Calculus AB", "AP Seminar"],
                "favorite": {
                    "color": "Burgundy",
                    "food": "Chicken Tikka Masala"
                }
            })
    

api.add_resource(RohanAPI._BojjaAPI, "/people/rohan")