from flask import Blueprint, jsonify
from flask_restful import Api, Resource


student_api = Blueprint('student_api', __name__, url_prefix='/api')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(student_api)


class StudentAPI:
   @staticmethod
   def get_student(name):
       students = {
           "Rohan": {
               "name": "Rohan",
               "age": 15,
               "major": "CS",
               "university": "Del Norte High School"
           }
       }
       return students.get(name)


   class _Rohan(Resource):
       def get(self):
           # Use the helper method to get John's details
           rohan_details = StudentAPI.get_student("Rohan")
           return jsonify(rohan_details)