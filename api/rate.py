import jwt
from flask import Flask, Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from __init__ import app, db  # Ensure db is imported
from api.jwt_authorize import token_required
from model.post import Post
from model.rate import Rate
from flask_cors import cross_origin  # Importing cross_origin
from model.user import User


# Define the Blueprint for the Rate API
rate_api = Blueprint('rate_api', __name__, url_prefix='/api')
#CORS(rate_api, supports_credentials=True)
CORS(rate_api, supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'])

# Connect the Api object to the Blueprint
api = Api(rate_api)

class RateAPI:
    """
    Define the API CRUD endpoints for the Rate model.
    There are operations for creating and retrieving ratings for a post.
    """

    class _CRUD(Resource):
        @token_required()
        @cross_origin(supports_credentials=True)  # Add this decorator to handle CORS for PUT requests
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            post_id = data.get('post_id')
            rating_value = data.get('rating')

            if post_id is None or rating_value is None:
                return jsonify({"message": "post_id and rating are required"}), 400

            try:
                rating_value = int(rating_value)
            except ValueError:
                return jsonify({"message": "Rating must be an integer"}), 400

            if not (1 <= rating_value <= 10):
                return jsonify({"message": "Rating must be between 1 and 10"}), 400

            # Create a new rating entry
            rating = Rate(user_id=current_user.id, post_id=post_id, value=rating_value)
            db.session.add(rating)
            db.session.commit()

            return jsonify({"message": "Rating submitted successfully"})

        @token_required()
        def get(self):
            """
            Retrieve ratings for a post.
            """
            post_id = request.args.get('post_id')
            if not post_id:
                return jsonify({"message": "post_id is required"}), 400

            ratings = db.session.query(Rate, User).join(User, Rate.user_id == User.id).filter(Rate.post_id == post_id).all()
            ratings_list = [{"rating_id": r.Rate.id, "username": r.User._name, "rating": r.Rate.value} for r in ratings]

            return jsonify(ratings_list)

        
        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            rating_id = data.get('rating_id')
            new_rating_value = data.get('rating')

            if rating_id is None or new_rating_value is None:
                return jsonify({"message": "rating_id and new rating value are required"}), 400

            try:
                new_rating_value = int(new_rating_value)
            except ValueError:
                return jsonify({"message": "Rating must be an integer"}), 400

            if not (1 <= new_rating_value <= 10):
                return jsonify({"message": "Rating must be between 1 and 10"}), 400

            # Find the rating by ID and ensure it belongs to the current user
            rating = Rate.query.filter_by(id=rating_id, user_id=current_user.id).first()

            if not rating:
                return jsonify({"message": "Rating not found or not authorized"}), 404

            # Update the rating value
            rating.value = new_rating_value
            db.session.commit()

            return jsonify({"message": "Rating updated successfully"})
        
        @token_required()
        def delete(self):
            """
            Delete a rating for a post by the current user.
            """
            current_user = g.current_user
            data = request.get_json()
            rating_id = data.get('rating_id')

            if rating_id is None:
                return jsonify({"message": "rating_id is required"}), 400

            rating = Rate.query.filter_by(user_id=current_user.id, id=rating_id).first()
            if rating:
                db.session.delete(rating)
                db.session.commit()
                return jsonify({"message": "Rating deleted successfully"})
            else:
                return jsonify({"message": "Rating not found"}), 404


# Add resource to the API
api.add_resource(RateAPI._CRUD, "/rate")