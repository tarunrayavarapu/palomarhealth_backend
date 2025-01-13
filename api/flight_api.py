from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json


flight_api = Blueprint('flight_api', __name__, url_prefix='/api')
api = Api(flight_api)


base_flight_api_url = 'https://api.aviationstack.com/v1/flights'

api_key = 'e57e129b3e76d1dc706a05dc1e776b40'
class FlightAPI:
    
    class _Flight(Resource):
        
        def get(self):
            
            origin = request.args.get('origin', 'JFK')
            destination = request.args.get('destination', 'LAX')
            flight_data = get_flight_data(origin, destination, api_key)

            if flight_data:
                return jsonify(flight_data)
            else:
                return jsonify({"error": "Failed to get flight data"}), 500

    
    api.add_resource(_Flight, '/flight')


def get_flight_data(origin, destination, api_key):
    

    api_url = base_flight_api_url.format(origin, destination, api_key)
    response = requests.get(api_url)
    
    if response.status_code == requests.codes.ok:
        return response.json
    else:
        print("Error:", response.status_code, response.text)
        return None