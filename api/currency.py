from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

# blueprint for the currency conversion api
currency_api = Blueprint('currency_api', __name__, url_prefix='/api')
api = Api(currency_api)

# API key and API URL for the currency conversion API
api_key = 'whtBMWOKRMxDm+KkxJidew==WPks2hKmgV3Lqogd'
currency_api_url = 'https://api.api-ninjas.com/v1/convertcurrency?have={}&want={}&amount={}'

class CurrencyAPI:
    
    # Define the API CRUD endpoints for currency conversion
    
    class _CurrencyConversion(Resource):
        
        def get(self):
            # Retrieve the currency data for the conversion request
            
            have = request.args.get('have', '')  # Get the currency to convert from
            want = request.args.get('want', '')  # Get the currency to convert to
            amount = request.args.get('amount', '')  # Get the amount to convert
            
            if not have or not want or not amount:
                return jsonify({"error": "Missing required parameters (have, want, amount)"}), 400
            
            # Get the conversion result from the external API
            conversion_data = get_conversion_data(have, want, amount)
            
            if conversion_data:
                return jsonify(conversion_data)
            else:
                return jsonify({"error": "Failed to get currency conversion data"}), 500
    
    # Add the resource for /currency_conversion
    api.add_resource(_CurrencyConversion, '/convertcurrency')

# Function to fetch conversion data from the API
def get_conversion_data(have, want, amount):
    # Construct the URL for the API request
    api_url = currency_api_url.format(have, want, amount)
    
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None
