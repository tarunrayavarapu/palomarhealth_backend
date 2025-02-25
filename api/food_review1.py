from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import db
from model.food_review1 import FoodReview1
from model.user import User
from api.jwt_authorize import token_required
from flask_cors import cross_origin  # Importing cross_origin

food_review_1_api = Blueprint('food_review_1_api', __name__, url_prefix='/api')
api = Api(food_review_1_api)

CORS(food_review_1_api, supports_credentials=True, methods=['GET', 'POST', 'PUT', 'DELETE'])

class FoodReviewAPI:
    class _CRUD(Resource):

        @token_required()
        @cross_origin(supports_credentials=True)  # Add this decorator to handle CORS for POST requests
        def post(self):
            current_user = g.current_user
            data = request.get_json()

            if not data or 'food' not in data or 'review' not in data or 'rating' not in data:
                return {'message': 'Invalid, data required'}, 400

            food_review = FoodReview1(
                food=data.get('food'),
                review=data.get('review'),
                rating=data.get('rating'),
                user_id=current_user.id
            )

            try:
                food_review.create()
                return jsonify(food_review.read())
            except Exception as e:
                return {'message': f'Error saving review: {e}'}, 500

        def get(self):
            review_id = request.args.get('id')

            if review_id:
                review = FoodReview1.query.get(review_id)
                if not review:
                    return {'message': 'Review not found'}, 404
                return jsonify(review.read())

            reviews = db.session.query(FoodReview1, User).join(User, FoodReview1.user_id == User.id).all()
            review_list = [{"id": r.FoodReview1.id, "user_id": r.User._name, "food": r.FoodReview1.food, "review": r.FoodReview1.review, "rating": r.FoodReview1.rating} for r in reviews]
            
            return jsonify(review_list)

        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a review'}, 400

            review = FoodReview1.query.get(data['id'])
            if not review:
                return {'message': 'Review not found'}, 404

            try:
                review.update(data)
                return jsonify(review.read())
            except Exception as e:
                return {'message': f'Error updating review: {e}'}, 500

        def delete(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a review'}, 400

            review = FoodReview1.query.get(data['id'])
            if not review:
                return {'message': 'Review not found'}, 404

            try:
                review.delete()
                return {'message': 'Review deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting review: {e}'}, 500

    api.add_resource(_CRUD, '/food_review_1_api')
