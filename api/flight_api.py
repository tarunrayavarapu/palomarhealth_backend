from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

app = Flask(__name__)

flight_api = Blueprint('flight_api', __name__, url_prefix='/api')
api = Api(flight_api)

base_flight_api_url = 'https://api.aviationstack.com/v1/flights'
access_key = '49dedef46036ca89f373e18c5615ff38'

class FlightAPI:
    class _Flight(Resource):
        def get(self):
            origin = request.args.get('origin', 'JFK')
            destination = request.args.get('destination', 'LAX')
            flight_data = get_flight_data(origin, destination, access_key)

            if flight_data:
                return jsonify(flight_data)
            else:
                return jsonify({"error": "Failed to get flight data"}), 500

    api.add_resource(_Flight, '/flight')

def get_flight_data(origin, destination, access_key):
    api_url = f"{base_flight_api_url}?access_key={access_key}&dep_iata={origin}&arr_iata={destination}"
    response = requests.get(api_url)
    
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

app.register_blueprint(flight_api)

if __name__ == '__main__':
    app.run(port=8887)