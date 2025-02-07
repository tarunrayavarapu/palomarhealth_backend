from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.food_review123 import FoodReview123

food_review123_api = Blueprint('food_review123_api', __name__, url_prefix='/api')

api = Api(food_review123_api, supports_credentials=True)

class FoodAPI:
    class _CRUD(Resource):
        def post(self):

            data = request.get_json()

            if not data or 'food' not in data or 'review' not in data or 'rating' not in data:
                return {'message': 'Invalid, data required'}, 400

            food_review123_api = FoodReview123(
                food=data.get('food'),
                review=data.get('review'),
                rating=data.get('rating'),
                # _hashtag=data.get('_hashtag'),
                # _user_id=data.get('_user_id'),
                # _group_id=data.get('_group_id')
            )

            try:
                food_review123_api.create()
                return jsonify(food_review123_api.read())
            except Exception as e:
                return {'message': f'Error saving review: {e}'}, 500

        def get(self):

            review_id = request.args.get('id')

            if review_id:

                review = FoodReview123.query.get(review_id)
                if not review:
                    return {'message': 'Review not found'}, 404
                return jsonify(review.read())

            all_reviews = FoodReview123.query.all()
            return jsonify([review.read() for review in all_reviews])

        def put(self):

            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a review'}, 400

            review = FoodReview123.query.get(data['id'])
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

            review = FoodReview123.query.get(data['id'])
            if not review:
                return {'message': 'Review not found'}, 404

            try:
                review.delete()
                return {'message': 'Review deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting review: {e}'}, 500

    api.add_resource(_CRUD, '/food_review123_api')