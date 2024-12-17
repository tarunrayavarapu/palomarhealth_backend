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
                "sports": ["Basketball", "Badminton", "Taekwondo"]
            })
    

api.add_resource(RohanAPI._BojjaAPI, "/people/rohan")