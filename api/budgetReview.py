import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.budgetReview import BudgetReview
from model.channel import Channel

"""
Define the API CRUD endpoints
"""
budget_review_api = Blueprint('budget_review_api', __name__, url_prefix='/api')

api = Api(budget_review_api)

class BudgetReviewAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new budget review.
            """
            current_user = g.current_user
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Budget review title is required'}, 400
            if 'comment' not in data:
                return {'message': 'Budget review comment is required'}, 400
            if 'channel_id' not in data:
                return {'message': 'Channel ID is required'}, 400
            if 'rating' not in data:
                return {'message': 'Budget review rating is required'}, 400
            if 'hashtag' not in data:
                data['hashtag'] = None  # Optional field, default to None
            if 'date' not in data:
                data['date'] = datetime.utcnow().isoformat()  # Optional field, default to current time

            # Create the BudgetReview object with the provided data
            budget_review = BudgetReview(
                data['title'], 
                data['comment'], 
                data['rating'], 
                data['hashtag'], 
                data['date'], 
                current_user.id, 
                data['channel_id']
            )
            # Save the BudgetReview object
            budget_review.create()
            return jsonify(budget_review.read())

        @token_required()
        def get(self):
            """
            Retrieve a single budget review by ID.
            """
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Budget review ID not found'}, 400
            budget_review = BudgetReview.query.get(data['id'])
            if not budget_review:
                return {'message': 'Budget review not found'}, 404
            return jsonify(budget_review.read())

        @token_required()
        def put(self):
            """
            Update a budget review.
            """
            current_user = g.current_user
            data = request.get_json()

            # Find the current budget review
            budget_review = BudgetReview.query.get(data['id'])
            if not budget_review:
                return {'message': 'Budget review not found'}, 404

            # Update fields with the new data
            budget_review._title = data['title']
            budget_review._comment = data['comment']
            budget_review._rating = data['rating']
            budget_review._hashtag = data.get('hashtag', budget_review._hashtag)  # optional, defaults to previous value
            budget_review._date = data.get('date', budget_review._date)  # optional, defaults to previous value
            budget_review._channel_id = data['channel_id']

            # Save the updated BudgetReview object
            budget_review.update()
            return jsonify(budget_review.read())

        @token_required()
        def delete(self):
            """
            Delete a budget review.
            """
            current_user = g.current_user
            data = request.get_json()

            # Find the budget review by ID
            budget_review = BudgetReview.query.get(data['id'])
            if not budget_review:
                return {'message': 'Budget review not found'}, 404

            # Delete the review
            budget_review.delete()
            return jsonify({"message": "Budget review deleted"})

    class _USER(Resource):
        @token_required()
        def get(self):
            """
            Retrieve all budget reviews by the current user.
            """
            current_user = g.current_user
            budget_reviews = BudgetReview.query.filter(BudgetReview._user_id == current_user.id).all()
            json_ready = [budget_review.read() for budget_review in budget_reviews]
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Bulk create budget reviews.
            """
            budget_reviews = request.get_json()

            if not isinstance(budget_reviews, list):
                return {'message': 'Expected a list of budget review data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for budget_review in budget_reviews:
                    response = client.post('/api/budget_review', json=budget_review)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            return jsonify(results)

        def get(self):
            """
            Retrieve all budget reviews.
            """
            budget_reviews = BudgetReview.query.all()
            json_ready = [budget_review.read() for budget_review in budget_reviews]
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve budget reviews by channel ID and user ID.
            """
            data = request.get_json()
            if 'channel_id' not in data:
                return {'message': 'Channel ID not found'}, 400

            budget_reviews = BudgetReview.query.filter_by(_channel_id=data['channel_id']).all()
            json_ready = [budget_review.read() for budget_review in budget_reviews]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/budget_review')
    api.add_resource(_USER, '/budget_review/user')
    api.add_resource(_BULK_CRUD, '/budget_reviews')
    api.add_resource(_FILTER, '/budget_reviews/filter')
