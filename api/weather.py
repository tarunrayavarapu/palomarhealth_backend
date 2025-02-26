import jwt
import requests
import json
import logging
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from model.weather import Weather
from datetime import datetime
from __init__ import app, db 
from api.jwt_authorize import token_required
from model.post import Post
from flask_cors import cross_origin 
from model.user import User


# blueprint for the weather api
weather_api = Blueprint('weather_api', __name__, url_prefix='/api')
CORS(weather_api, supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'])
api = Api(weather_api)

# api key and api url for the weather api
api_key = 'MQI4P3He9SrgKNuM2Jlxpw==0jgKA84fv3L0yojr'
weather_api_url = 'https://api.api-ninjas.com/v1/weather?lat={}&lon={}'


class WeatherAPI:
    
    class _Weather(Resource):
        
        def get(self):
            
            # retrieve the weather data for the latitude and longitude of a city
            
            lat = request.args.get('lat', '')  # get the latitude of the city from the query parameters
            lon = request.args.get('lon', '')  # get the longitude of the city from the query parameters
            weather_data = get_weather_data(lat, lon)

            if weather_data:
                return jsonify(weather_data)
            else:
                return jsonify({"error": "Failed to get weather data"}), 500

    # add the resource for /weather
    
    api.add_resource(_Weather, '/weather')


    class _CRUD(Resource):
        @token_required()
        @cross_origin(supports_credentials=True)
        def get(self):
            
            weather_id = request.args.get('id')

            if weather_id:
                weather = Weather.query.get(weather_id)
                
                if not weather:
                    return {'message': 'Weather not found'}, 404
                return jsonify(weather)
            
            current_user = g.current_user
            is_admin = current_user.role == 'Admin'
            
            all_items = db.session.query(Weather, User).join(User, Weather.user_id == User.id).all()
            item_list = [{"id": item.Weather.id, "user_id": item.User._name, "current_user": current_user._name, "is_admin": is_admin, "item": item.Weather.item} for item in all_items]
            
            
            return jsonify(item_list)
            
        @token_required()
        @cross_origin(supports_credentials=True)
        def post(self):

            current_user = g.current_user
            data = request.get_json()
            item = data.get('item')
            
            if not data or 'item' not in data:
                return {'message': 'Required information not entered'}, 400

            current_user = g.current_user

            weather = Weather(
                item=data.get('item'), 
                user_id=current_user.id
            )
            
            db.session.add(weather)
            db.session.commit()
            return jsonify(weather.read())

        #@token_required()
        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating information'}, 400

            weather = Weather.query.get(data['id'])
            if not weather:
                return {'message': 'Information not found'}, 404

            try:
                weather.update(data)
                return jsonify(weather.read())
            except Exception as e:
                return {'message': f'Error updating information: {e}'}, 500

        #@token_required()
        def delete(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting information'}, 400

            weather = Weather.query.get(data['id'])
            if not weather:
                return {'message': 'Information not found'}, 404

            try:
                weather.delete()
                return {'message': 'Information deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting information: {e}'}, 500

    api.add_resource(_CRUD, '/packing_checklists')

def get_weather_data(lat, lon):
    
    # get the weather data for the latitude and longitude of a city

    api_url = weather_api_url.format(lat, lon)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None