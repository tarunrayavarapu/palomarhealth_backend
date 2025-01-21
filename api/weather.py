from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json
from model.weather import Weather


# blueprint for the weather api
weather_api = Blueprint('weather_api', __name__, url_prefix='/api')
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
        def get(self):
            
            # retrieve the weather data for the latitude and longitude of a city
            
            weather_id = request.args.get('id')
            # weather_data = get_weather_data(lat, lon)

            if weather_id:
                weather = Weather.query.get(weather_id)
                
                if not weather:
                    return {'message': 'Weather not found'}, 404
                return jsonify(weather)
            # else:
            #     return jsonify({"error": "Failed to get weather data"}), 500
        def post(self):

            data = request.get_json()
            
            if not data or 'item' not in data:
                return {'message': 'Required information not entered'}, 400

            packing_checklists = Weather(
                user = data.get('user'),
                item = data.get('item')
            )

            try:
                packing_checklists.create()
                return jsonify(packing_checklists.read())
            except Exception as e:
                return {'message': f'Error saving information: {e}'}, 500

        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating information'}, 400

            packing_checklists = Weather.query.get(data['id'])
            if not packing_checklists:
                return {'message': 'Information not found'}, 404

            try:
                packing_checklists.update(data)
                return jsonify(packing_checklists.read())
            except Exception as e:
                return {'message': f'Error updating information: {e}'}, 500

        def delete(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting information'}, 400

            packing_checklists = Weather.query.get(data['id'])
            if not packing_checklists:
                return {'message': 'Information not found'}, 404

            try:
                packing_checklists.delete()
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