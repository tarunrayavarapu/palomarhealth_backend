from flask import Blueprint, jsonify
from flask_restful import Api, Resource

# Create a Blueprint for the student API
tarun_api = Blueprint('tarun_api', __name__, url_prefix='/api')

# Initialize the API using Flask-RESTful
api = Api(tarun_api)

class TarunAPI:
    @staticmethod
    def get_student():
        # Static details for Tarun
        return {
            "name": "Tarun",
            "age": 24,
            "major": "Data Science",
            "university": "PQR University"
        }

    class _Tarun(Resource):
        def get(self):
            # Use the helper method to get Tarun's details
            tarun_details = TarunAPI.get_student()
            return jsonify(tarun_details)

    # Building REST API endpoint
    api.add_resource(_Tarun, '/student/tarun')

# Instantiate the TarunAPI to register the endpoint
tarun_api_instance = TarunAPI()
