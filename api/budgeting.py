import logging
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource  # used for REST API building
from __init__ import app
from api.jwt_authorize import token_required
from model.budgeting import Budgeting  # Updated to import the new Budgeting model

"""
Define the API CRUD endpoints
"""
budgeting_api = Blueprint('budgeting_api', __name__, url_prefix='/api')

api = Api(budgeting_api)

class BudgetingAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new budgeting entry.
            """
            current_user = g.current_user
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'total_budget' not in data:
                return {'message': 'Total budget is required'}, 400
            if 'percent_hotels' not in data:
                return {'message': 'Percent for hotels is required'}, 400
            if 'percent_transport' not in data:
                return {'message': 'Percent for transport is required'}, 400
            if 'overbudget' not in data:
                return {'message': 'Overbudget boolean is required'}, 400

            # Create the Budgeting object with the provided data
            budgeting = Budgeting(
                data['total_budget'],
                data['percent_hotels'],
                data['percent_transport'],
                data['overbudget']
            )
            # Save the Budgeting object
            budgeting.create()
            return jsonify(budgeting.read())

        @token_required()
        def get(self):
            """
            Retrieve a single budgeting entry by ID.
            """
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Budgeting entry ID not found'}, 400
            budgeting = Budgeting.query.get(data['id'])
            if not budgeting:
                return {'message': 'Budgeting entry not found'}, 404
            return jsonify(budgeting.read())

        @token_required()
        def put(self):
            """
            Update a budgeting entry.
            """
            current_user = g.current_user
            data = request.get_json()

            # Find the current budgeting entry
            budgeting = Budgeting.query.get(data['id'])
            if not budgeting:
                return {'message': 'Budgeting entry not found'}, 404

            # Update fields with the new data
            budgeting.total_budget = data['total_budget']
            budgeting.percent_hotels = data['percent_hotels']
            budgeting.percent_transport = data['percent_transport']
            budgeting.overbudget = data['overbudget']

            # Save the updated Budgeting object
            budgeting.update(data)
            return jsonify(budgeting.read())

        @token_required()
        def delete(self):
            """
            Delete a budgeting entry.
            """
            current_user = g.current_user
            data = request.get_json()

            # Find the budgeting entry by ID
            budgeting = Budgeting.query.get(data['id'])
            if not budgeting:
                return {'message': 'Budgeting entry not found'}, 404

            # Delete the budgeting entry
            budgeting.delete()
            return jsonify({"message": "Budgeting entry deleted"})

    class _USER(Resource):
        @token_required()
        def get(self):
            """
            Retrieve all budgeting entries by the current user.
            """
            current_user = g.current_user
            budgeting_entries = Budgeting.query.filter(Budgeting._user_id == current_user.id).all()
            json_ready = [budgeting.read() for budgeting in budgeting_entries]
            return jsonify(json_ready)

    class _BULK_CRUD(Resource):
        def post(self):
            """
            Bulk create budgeting entries.
            """
            budgeting_entries = request.get_json()

            if not isinstance(budgeting_entries, list):
                return {'message': 'Expected a list of budgeting entry data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for budgeting in budgeting_entries:
                    response = client.post('/api/budgeting', json=budgeting)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            return jsonify(results)

        def get(self):
            """
            Retrieve all budgeting entries.
            """
            budgeting_entries = Budgeting.query.all()
            json_ready = [budgeting.read() for budgeting in budgeting_entries]
            return jsonify(json_ready)

    class _FILTER(Resource):
        @token_required()
        def post(self):
            """
            Retrieve budgeting entries by group ID.
            """
            data = request.get_json()
            if 'group_id' not in data:  
                return {'message': 'Group ID not found'}, 400

            budgeting_entries = Budgeting.query.filter_by(_group_id=data['group_id']).all()  
            json_ready = [budgeting.read() for budgeting in budgeting_entries]
            return jsonify(json_ready)

    api.add_resource(_CRUD, '/budgeting')
    api.add_resource(_USER, '/budgeting/user')
    api.add_resource(_BULK_CRUD, '/budgetings')
    api.add_resource(_FILTER, '/budgetings/filter')
