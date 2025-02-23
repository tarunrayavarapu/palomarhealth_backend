from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import db
from model.hotel import Hotel
from model.user import User
from api.jwt_authorize import token_required
from flask_cors import cross_origin  # Importing cross_origin

hotel_api = Blueprint('hotel_api', __name__, url_prefix='/api')
CORS(hotel_api, supports_credentials=True)
api = Api(hotel_api)

class HotelAPI:

    class _CRUD(Resource):
        
        @token_required()
        @cross_origin(supports_credentials=True)  # Add this decorator to handle CORS for PUT requests
        def post(self):

            current_user = g.current_user
            data = request.get_json()

            if not data or 'hotel' not in data or 'city' not in data or 'country' not in data or 'rating' not in data:
                return {'message': 'Hotel, location, and rating are required'}, 400

            hotel = Hotel(
                user_id=current_user.id,
                hotel=data.get('hotel'),
                city=data.get('city'),
                country=data.get('country'),
                rating=data.get('rating'),
                note=data.get('note')
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
                    return {'message': 'Hotel not found'}, 404
                return jsonify(hotel.read())

            # all_hotels = Hotel.query.all()
            # return jsonify([hotel.read() for hotel in all_hotels])
        
            hotels = db.session.query(Hotel, User).join(User, Hotel.user_id == User.id).all()
            hotel_list = [{"id": h.Hotel.id, "user_id": h.User._name, "hotel": h.Hotel.hotel, "city": h.Hotel.city, "country": h.Hotel.country, "rating": h.Hotel.rating, "note": h.Hotel.note} for h in hotels]
            
            return jsonify(hotel_list)


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
