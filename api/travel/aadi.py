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
                "hobbies": ["Lego", "Mario", "Computer stuff"],
                "favorite_foods": ["Maggi", "Naan", "Pizza"]
            })
    

api.add_resource(AadiAPI._A_Person, "/people/aadi")