from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json

# Blueprint for the flights API
flights_api = Blueprint('flights_api', __name__, url_prefix='/api')
api = Api(flights_api)

# Base URL for the flights API (replace with an actual API endpoint)
base_flight_api_url = 'https://api.aviationstack.com/v1/flights'

class FlightsAPI:
    class _Flights(Resource):
        def get(self):
            origin = request.args.get('origin', 'LAX')  # Default to LAX
            destination = request.args.get('destination', 'JFK')  # Default to JFK

            flight_data = get_flight_data(origin, destination)
            if flight_data:
                return jsonify(flight_data)
            else:
                return jsonify({"error": "Failed to get flight data"}), 500

    # Add resource for flights API endpoint
    api.add_resource(_Flights, '/rohan/flights')

def get_flight_data(origin, destination, date=None):
    # Build the API URL with query parameters
    api_url = f"{base_flight_api_url}?origin={origin}&destination={destination}"

    # Make the GET request
    response = requests.get(api_url, headers={"User-Agent": "MyFlightApp/1.0 (contact@example.com)"})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None