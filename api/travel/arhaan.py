from flask import Blueprint, jsonify
from flask_restful import Api, Resource


student_api = Blueprint('student_api', __name__, url_prefix='/api')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(student_api)


class StudentAPI:
   @staticmethod
   def get_student(name):
       students = {
           "Arhaan": {
               "name": "Arhaan",
               "age": 21,
               "major": "Computer Science",
               "university": "Harvard University"
           },
       }
       return students.get(name)


   class _Arhaan(Resource):
       def get(self):
           # Use the helper method to get John's details
           arhaan_details = StudentAPI.get_student("Arhaan")
           return jsonify(arhaan_details)


   class _Bulk(Resource):
       def get(self):
           # Use the helper method to get both John's and Jeff's details
           arhaan_details = StudentAPI.get_student("Arhaan")
           return jsonify({"students": [arhaan_details]})


   # Building REST API endpoints
   api.add_resource(_John, '/student/john')


# Instantiate the StudentAPI to register the endpoints
student_api_instance = StudentAPI()