# from flask import Blueprint, request, jsonify
# from flask_restful import Api, Resource
# import requests

# flight_api = Blueprint('flight_api', __name__, url_prefix='/api')
# api = Api(flight_api)

# base_flight_api_url = 'https://api.aviationstack.com/v1/flights'
# access_key = 'e57e129b3e76d1dc706a05dc1e776b40'

# class FlightAPI:
#     class _Flight(Resource):
        # def get(self):
        #     origin = request.args.get('dep_iata', '')
        #     destination = request.args.get('arr_iata', '')
        #     flight_data = get_flight_data(origin, destination, access_key)

        #     if flight_data:
        #         return jsonify(flight_data)
        #     else:
        #         return jsonify({"error": "Failed to get flight data"}), 500

#     api.add_resource(_Flight, '/flight')

# def get_flight_data(origin, destination, access_key):
#     api_url = f"{base_flight_api_url}?access_key={access_key}&dep_iata={origin}&arr_iata={destination}"
#     response = requests.get(api_url)
    
#     if response.status_code == requests.codes.ok:
#         return response.json()
#     else:
#         print("Error:", response.status_code, response.text)
#         return None

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.flight_api_post import Flight
import requests

flight_api = Blueprint('flight_api', __name__, url_prefix='/api')
api = Api(flight_api)

base_flight_api_url = 'https://api.aviationstack.com/v1/flights'
access_key = 'e57e129b3e76d1dc706a05dc1e776b40'


def get_flight_data(origin, destination, access_key):
    api_url = f"{base_flight_api_url}?access_key={access_key}&dep_iata={origin}&arr_iata={destination}"
    response = requests.get(api_url)
    
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None
    
    
class FlightAPI:

    class _CRUD(Resource):
        def post(self):

            data = request.get_json()

            if not data or 'dep_iata' not in data or 'arr_iata' not in data:
                return {'message': 'Required information not entered'}, 400

            flight = Flight(
                departure_iata = data.get('dep_iata'),
                arrival_iata = data.get('arr_iata')
            )

            try:
                flight.create()
                return jsonify(flight.read())
            except Exception as e:
                return {'message': f'Error saving information: {e}'}, 500

        def get(self):
            origin = request.args.get('dep_iata', '')
            destination = request.args.get('arr_iata', '')
            flight_data = get_flight_data(origin, destination, access_key)

            if flight_data:
                return jsonify(flight_data)
            else:
                return jsonify({"error": "Failed to get flight data"}), 500

        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating information'}, 400

            flight = Flight.query.get(data['id'])
            if not flight:
                return {'message': 'Information not found'}, 404

            try:
                flight.update(data)
                return jsonify(flight.read())
            except Exception as e:
                return {'message': f'Error updating information: {e}'}, 500

        def delete(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting information'}, 400

            flight = Flight.query.get(data['id'])
            if not flight:
                return {'message': 'Information not found'}, 404

            try:
                flight.delete()
                return {'message': 'Information deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting information: {e}'}, 500

    api.add_resource(_CRUD, '/flight')