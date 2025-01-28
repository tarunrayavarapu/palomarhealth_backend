from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
from model.flight_api_post import Flight

app = Flask(__name__)

# Blueprint for the flight API
flight_api = Blueprint('flight_api', __name__, url_prefix='/api')
from flask_cors import CORS
CORS(flight_api, supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'])

api = Api(flight_api)

# AviationStack API details
base_flight_api_url = 'https://api.aviationstack.com/v1/flights'
access_key = '3a3f41a8aec9903733ea4ce65d4b8adb'


class FlightAPI:
    class _Flight(Resource):
        def get(self):
            origin = request.args.get('origin', '')
            destination = request.args.get('destination', '')

            flight_data = get_flight_data(origin, destination, access_key)
            if flight_data:
                return jsonify(flight_data)
            else:
                return jsonify({"error": "Failed to get flight data"}), 500

        def post(self):
            # If you want POST to do something (like store or process data), add it here
            return jsonify({"message": "POST method is not supported for /flight-api endpoint"})


    api.add_resource(_Flight, '/flight-api')


def get_flight_data(origin, destination, access_key):
    api_url = f"{base_flight_api_url}?access_key={access_key}&dep_iata={origin}&arr_iata={destination}"
    response = requests.get(api_url)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None
    



# CRUD operations endpoint
class _CRUD(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'origin' not in data or 'destination' not in data or 'note' not in data:
            return {'message': 'Origin, destination, and note are required'}, 400

        flight = Flight(
            origin=data.get('origin'),
            destination=data.get('destination'),
            note=data.get('note')
        )

        try:
            flight.create()
            return jsonify(flight.read())
        except Exception as e:
            return {'message': f'Error saving flight: {e}'}, 500

    def get(self):
        flight_id = request.args.get('id')

        if flight_id:
            flight = Flight.query.get(flight_id)
            if not flight:
                return {'message': 'Flight not found'}, 404
            return jsonify(flight.read())

        all_flights = Flight.query.all()
        return jsonify([flight.read() for flight in all_flights])

    def put(self):
        data = request.get_json()

        if not data or 'id' not in data:
            return {'message': 'ID is required for updating a flight'}, 400

        flight = Flight.query.get(data['id'])
        if not flight:
            return {'message': 'Flight not found'}, 404

        try:
            flight.update(data)
            return jsonify(flight.read())
        except Exception as e:
            return {'message': f'Error updating flight: {e}'}, 500

    def delete(self):
        data = request.get_json()

        if not data or 'id' not in data:
            return {'message': 'ID is required for deleting a flight'}, 400

        flight = Flight.query.get(data['id'])
        if not flight:
            return {'message': 'Flight not found'}, 404

        try:
            flight.delete()
            return {'message': 'Flight deleted successfully'}, 200
        except Exception as e:
            return {'message': f'Error deleting flight: {e}'}, 500


# Register the CRUD resource
api.add_resource(_CRUD, '/flight')


# if __name__ == '__main__':
#     app.run(port=8887)