from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource

derek_api = Blueprint('derek_api', __name__, url_prefix='/api')
api = Api(derek_api)

class DerekAPI:
    class Student(Resource):
        def get(self):
            return jsonify({
                "name": "Derek Kang",
                "age": 15,
                "classes": ["AP CSP", "AP Physics Mechanics", "Ap Seminar", "AP Calculus AB", "AP World History"],
                "favorite": {
                    "color": "Blue",
                    "food": "Pasta"
                }
            })
    

api.add_resource(DerekAPI.Student, "/people/derek")