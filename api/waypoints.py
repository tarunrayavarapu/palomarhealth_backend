import json
import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.waypoints import Waypoints
from model.waypointsuser import WaypointsUser

"""
This Blueprint object is used to define APIs for the Waypoint model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
waypoints_api = Blueprint('waypoints_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(waypoints_api)

class WaypointAPI:
    """
    Define the API CRUD endpoints for the Waypoint model.
    There are four operations that correspond to common HTTP methods:
    - waypoint: create a new waypoint
    - get: read waypoints
    - put: update a waypoint
    - delete: delete a waypoint
    """
    class _GETWaypoints(Resource):
        @token_required()
        def get(self):
            """
            Retrieve a single waypoint by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None or 'id' not in data:
                waypoints = Waypoints.query.all()
                json_waypoints = [waypoint.to_dict() for waypoint in waypoints]
                return jsonify(json_waypoints)

            waypoints = Waypoints.query.get(data['id'])
            if waypoints is None:
                return {'message': 'Waypoint not found'}, 404
            # Convert Python object to JSON format 
            json_ready = waypoints.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)                

    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new waypointuser.
            """
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'injury' not in data:
                return {'message': 'Waypoint title is required'}, 400
            if 'location' not in data:
                return {'message': 'Waypoint comment is required'}, 400
            if 'address' not in data:
                data['address'] = {}
            if 'rating' not in data:
                data['rating'] = 5

            current_user = g.current_user
            # Create a new waypoint object using the data from the request
            waypointsuser = WaypointsUser(data['injury'], data['location'], data['address'], data['rating'], current_user.id)
            # Save the waypoint object using the Object Relational Mapper (ORM) method defined in the model
            waypointsuser.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(waypointsuser.read())

        @token_required()
        def get(self):
            """
            Retrieve a single waypoint by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            current_user = g.current_user
            waypointsuser = WaypointsUser.query.filter_by(_user_id=current_user.id)
            if waypointsuser is None:
                return {'message': 'Waypoint not found'}, 404
            # Convert Python object to JSON format 
            waypointsusers = waypointsuser.all()
            json_waypointsuser = [waypointsuser.to_dict() for waypointsuser in waypointsusers]
            return jsonify(json_waypointsuser)

            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a waypoint.
            """
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current waypoint from the database table(s)
            waypointsuser = WaypointsUser.query.get(data['waypoint_id'])
            if waypointsuser is None:
                return {'message': 'WaypointUser not found'}, 404
            # Update the waypoint
            waypointsuser._rating = data['rating']
            # Save the waypoint
            waypointsuser.update()
            # Return response
            return jsonify(waypointsuser.read())

        @token_required()
        def delete(self):
            """
            Delete a waypoint.
            """
            waypoint_id = request.args.get('waypoint_id')
            # Find the current waypoint from the database table(s)
            waypointsuser = WaypointsUser.query.filter_by(id=waypoint_id).first()
            if waypointsuser is None:
                return {'message': 'Waypoint not found'}, 404
            # Delete the waypoint using the ORM method defined in the model
            waypointsuser.delete()
            # Return response
            return jsonify({"message": "Waypoint deleted"})

    class _GetRating(Resource):
        @token_required()
        def get(self):
            """
            Get the last rating for a specific address.
            This endpoint doesn't require authentication.
            """
            try:
                address = request.args.get('address')
                if not address:
                    return {'message': 'Address parameter is required'}, 400
                    
                rating_info = WaypointsUser.get_last_rating(address)
                if rating_info is None:
                    return {'message': 'No ratings found'}, 404
                    
                return jsonify(rating_info)
                
            except Exception as e:
                return {'message': str(e)}, 500

    api.add_resource(_CRUD, '/waypoints')
    api.add_resource(_GetRating, '/waypoints/rating')