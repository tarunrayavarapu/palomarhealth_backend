from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

# Blueprint for the food review API
food_review_api = Blueprint('food_review_api', __name__, url_prefix='/api')
api = Api(food_review_api)

# In-memory storage for reviews
reviews = ["hi"]

class FoodReviewAPI:
    class _ReviewList(Resource):
        def get(self):
            """
            Retrieve all food reviews.
            """
            return jsonify(reviews)

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
                food = data.get("food")
                review = data.get("review")
                rating = data.get("rating")

                if not (food and review and isinstance(rating, (int, float)) and 1 <= rating <= 5):
                    return {"message": "Invalid data. Ensure 'food', 'review', and 'rating' (1-5) are provided."}, 400
                
                new_review = {
                    "food": food,
                    "review": review,
                    "rating": rating
                }
                reviews.append(new_review)
                return {"message": "Review added successfully.", "review": new_review}, 201
            except Exception as e:
                return {"message": f"An error occurred: {str(e)}"}, 500

    class _AverageRating(Resource):
        def get(self):
            """
            Calculate the average rating for all reviews.
            """
            if not reviews:
                return {"message": "No reviews available."}, 200
            
            average_rating = sum(review['rating'] for review in reviews) / len(reviews)
            return {"average_rating": round(average_rating, 2), "total_reviews": len(reviews)}

# Add resource routes
api.add_resource(FoodReviewAPI._ReviewList, "/reviews")
api.add_resource(FoodReviewAPI._AverageRating, "/reviews/average")
