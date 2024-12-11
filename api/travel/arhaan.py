from flask import Blueprint, jsonify
from flask_restful import Api, Resource


arhaan_api = Blueprint('arhaan_api', __name__, url_prefix='/api')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(arhaan_api)


class StudentAPI:
   def get_student(name):
       students = {
           "Arhaan": {
               "name": "Arhaan Memon",
               "age": 15,
               "classes": ("AP CSP", "AP BIO", "AP SEM, History, Math 3b"),
               "sports": ("Basketball", "Football"),
               "Food": ("Pizza", "Pasta", "Apple Pie")
           },
       }
       return students.get(name)


   class _Arhaan(Resource):
       def get(self):
           # Use the helper method to get Arhaan's details
           arhaan_details = StudentAPI.get_student("Arhaan")
           return jsonify(arhaan_details)


   # Building REST API endpoints
   api.add_resource(_Arhaan, '/student/arhaan')


# Instantiate the StudentAPI to register the endpoints
student_api_instance = StudentAPI()