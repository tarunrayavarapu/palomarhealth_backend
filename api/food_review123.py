from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.food_review123 import FoodReview123


# Define the Blueprint for the FoodReview123 API
food_review123_api = Blueprint('food_review123_api', __name__, url_prefix='/api')
api = Api(food_review123_api)



# Define the API resources
class FoodReview123API:
    class _ReviewList(Resource):
        def get(self):
            """
            Retrieve all food reviews.
            """
            with db.session.no_autoflush:
                reviews = FoodReview123.query.all()
                return jsonify([review.read() for review in reviews])

        def post(self):
            """
            Add a new food review.
            Request JSON should include:
              - 'food': The name of the food item
              - 'review': The review text
              - 'rating': The star rating (1 to 5)
            """
            try:
                data = request.get_json()

                # Validate input data
                food = data.get("food")
                review = data.get("review")
                rating = data.get("rating")

                if not all([food, review, rating]):
                    return {"message": "Missing 'food', 'review', or 'rating'."}, 400
                if not (isinstance(rating, (int, float)) and 1 <= rating <= 5):
                    return {"message": "Rating must be a number between 1 and 5."}, 400

                # Create and save a new review
                new_review = FoodReview123(food=food, review=review, rating=rating)
                new_review.create()
                return {"message": "Review added successfully.", "review": new_review.read()}, 201
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    class _AverageRating(Resource):
        def get(self):
            """
            Calculate the average rating for all reviews.
            """
            with db.session.no_autoflush:
                reviews = FoodReview123.query.all()
                if not reviews:
                    return {"message": "No reviews available."}, 200

                average_rating = sum(review.rating for review in reviews) / len(reviews)
                return {
                    "average_rating": round(average_rating, 2),
                    "total_reviews": len(reviews)
                }

# Add resource routes
api.add_resource(FoodReview123API._ReviewList, "/foodreviews123")
api.add_resource(FoodReview123API._AverageRating, "/foodreviews123/average")