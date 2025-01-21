import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db  # Ensure db is imported
from api.jwt_authorize import token_required
from model.post import Post
from model.rate import Rate

# Define the Blueprint for the Rate API
rate_api = Blueprint('rate_api', __name__, url_prefix='/api')

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

# Add resource to the API
api.add_resource(RateAPI._CRUD, "/rate")