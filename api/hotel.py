from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.hotel import Hotel

hotel_api = Blueprint('hotel_api', __name__, url_prefix='/api')

api = Api(hotel_api)

class HotelAPI:

    class _CRUD(Resource):
        def post(self):

            data = request.get_json()

            if not data or 'hotel' not in data or 'location' not in data or 'rating' not in data:
                return {'message': 'Hotel, location, and rating are required'}, 400

            hotel = Hotel(
                hotel=data.get('hotel'),
                location=data.get('location'),
                rating=data.get('rating')
            )

            try:
                hotel.create()
                return jsonify(hotel.read())
            except Exception as e:
                return {'message': f'Error saving hotel: {e}'}, 500

        def get(self):

            hotel_id = request.args.get('id')

            if hotel_id:

                hotel = Hotel.query.get(hotel_id)
                if not hotel:
                    return {'message': 'Hote not found'}, 404
                return jsonify(hotel.read())

            all_hotels = Hotel.query.all()
            return jsonify([hotel.read() for hotel in all_hotels])

        def put(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a hotel'}, 400

            hotel = Hotel.query.get(data['id'])
            if not hotel:
                return {'message': 'Hotel not found'}, 404

            try:
                hotel.update(data)
                return jsonify(hotel.read())
            except Exception as e:
                return {'message': f'Error updating hotel: {e}'}, 500

        def delete(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a hotel'}, 400

            hotel = Hotel.query.get(data['id'])
            if not hotel:
                return {'message': 'Hotel not found'}, 404

            try:
                hotel.delete()
                return {'message': 'Hotel deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting hotel: {e}'}, 500

    api.add_resource(_CRUD, '/hotel')