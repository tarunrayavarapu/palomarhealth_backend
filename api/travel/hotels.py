from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json

# blueprint for the hotel api
hotel_api = Blueprint('hotel_api', __name__, url_prefix='/api')
api = Api(hotel_api)

# base url for the hotel api
base_hotel_api_url = 'https://nominatim.openstreetmap.org/search'

class HotelAPI:
    class _Hotel(Resource):
        def get(self):
            hotel = request.args.get('hotel', 'Hilton') 
            place = request.args.get('place', 'Paris') 
            hotel_data = get_hotel_data(hotel, place)
            if hotel_data:
                return jsonify(hotel_data)
            else:
                return jsonify({"error": "Failed to get hotel data"}), 500
        def post(self):
            hotel = request.args.get('hotel', ' ') 
            place = request.args.get('place', ' ') 
            hotel_data = get_hotel_data(hotel, place)
            if hotel_data:
                return jsonify(hotel_data)
            else:
                return jsonify({"error": "Failed to post hotel data"}), 500

    api.add_resource(_Hotel, '/aadi/hotel')

def get_hotel_data(hotel, place):

    api_url = f"{base_hotel_api_url}?q={hotel},{place}&format=json&addressdetails=1"
    response = requests.get(api_url, headers={"User-Agent": "MyHotelApp/1.0 (contact@example.com)"})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None