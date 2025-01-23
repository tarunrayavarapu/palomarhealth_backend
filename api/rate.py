import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from datetime import datetime
from __init__ import app, db  # Ensure db is imported
from api.jwt_authorize import token_required
from model.post import Post
from model.rate import Rate

# Define the Blueprint for the Rate API
rate_api = Blueprint('rate_api', __name__, url_prefix='/api')
CORS(rate_api, supports_credentials=True)
# Connect the Api object to the Blueprint
api = Api(rate_api)

class RateAPI:
    """
    Define the API CRUD endpoints for the Rate model.
    There are operations for creating and retrieving ratings for a post.
    """

    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create or update a rating (1-10 scale) for a post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()
            post_id = data.get('post_id')
            rating_value = data.get('rating')

             # Validate post_id and rating_value
            if post_id is None or rating_value is None:
                return jsonify({"message": "post_id and rating are required"}), 400

            try:
                rating_value = int(rating_value)
            except ValueError:
                return jsonify({"message": "Rating must be an integer"}), 400


            # Validate rating value
            if not (1 <= rating_value <= 10):
                return jsonify({"message": "Rating must be between 1 and 10"}), 400

            # Create or update the rating
            rating = Rate.query.filter_by(user_id=current_user.id, post_id=post_id).first()
            if rating:
                rating.value = rating_value
                rating.updated_at = datetime.utcnow()
            else:
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
            ratings = Rate.query.filter_by(post_id=post_id).all()
            ratings_list = [{"user_id": r.user_id, "rating": r.value} for r in ratings]
            return jsonify(ratings_list)
        
        @token_required()
        def put(self):
            """
            Update a rating (1-10 scale) for a post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()
            post_id = data.get('post_id')
            rating_value = data.get('rating')

            # Validate post_id and rating_value
            if post_id is None or rating_value is None:
                return jsonify({"message": "post_id and rating are required"}), 400

            try:
                rating_value = int(rating_value)
            except ValueError:
                return jsonify({"message": "Rating must be an integer"}), 400

            if not (1 <= rating_value <= 10):
                return jsonify({"message": "Rating must be between 1 and 10"}), 400

            # Find the rating
            rating = Rate.query.filter_by(user_id=current_user.id, post_id=post_id).first()
            if rating:
                rating.value = rating_value
                rating.updated_at = datetime.utcnow()
                db.session.commit()
                return jsonify({"message": "Rating updated successfully"})
            else:
                return jsonify({"message": "Rating not found"}), 404

        
        @token_required()
        def delete(self):
            """
            Delete a rating for a post by the current user.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()
            post_id = data.get('post_id')

            # Validate post_id
            if post_id is None:
                return jsonify({"message": "post_id is required"}), 400

            # Find the rating
            rating = Rate.query.filter_by(user_id=current_user.id, post_id=post_id).first()
            if rating:
                db.session.delete(rating)
                db.session.commit()
                return jsonify({"message": "Rating deleted successfully"})
            else:
                return jsonify({"message": "Rating not found"}), 404


# Add resource to the API
api.add_resource(RateAPI._CRUD, "/rate")