from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json


# blueprint for the weather api
weather_api = Blueprint('weather_api', __name__, url_prefix='/api')
api = Api(weather_api)

# api key and api url for the weather api
api_key = 'MQI4P3He9SrgKNuM2Jlxpw==0jgKA84fv3L0yojr'
weather_api_url = 'https://api.api-ninjas.com/v1/weather?lat={}&lon={}'


class WeatherAPI:
    
    # define the api crud endpoints for the weather api
    
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


def get_weather_data(lat, long):
    
    # get the weather data for the latitude and longitude of a city

    api_url = weather_api_url.format(lat, long)
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
