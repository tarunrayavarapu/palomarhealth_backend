from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import db
from model.budgeting import Budgeting  # Assuming your Budgeting model is in the 'budgeting' module

budgeting_api = Blueprint('budgeting_api', __name__, url_prefix='/api')

api = Api(budgeting_api)

class BudgetingAPI:

    class _CRUD(Resource):
        def post(self):
            """
            Create a new budgeting entry.
            """
            data = request.get_json()

            # Validate the input data
            if not data or 'expense' not in data or 'cost' not in data or 'category' not in data or 'user_id' not in data:
                return {'message': 'Expense, cost, category, and user_id are required'}, 400

            # Create a new budgeting entry
            budgeting = Budgeting(
                expense=data.get('expense'),
                cost=data.get('cost'),
                category=data.get('category'),
                user_id=data.get('user_id')
            )

            try:
                budgeting.create()
                return jsonify(budgeting.read())
            except Exception as e:
                return {'message': f'Error saving budgeting entry: {e}'}, 500

        def get(self):
            """
            Retrieve budgeting entries.
            """
            budgeting_id = request.args.get('id')

            if budgeting_id:
                # Get a specific budgeting entry by ID
                budgeting = Budgeting.query.get(budgeting_id)
                if not budgeting:
                    return {'message': 'Budgeting entry not found'}, 404
                return jsonify(budgeting.read())

            # Get all budgeting entries
            all_budgeting = Budgeting.query.all()
            return jsonify([budgeting.read() for budgeting in all_budgeting])

        def put(self):
            """
            Update a budgeting entry.
            """
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a budgeting entry'}, 400

            # Find the budgeting entry by ID
            budgeting = Budgeting.query.get(data['id'])
            if not budgeting:
                return {'message': 'Budgeting entry not found'}, 404

            # Update the entry with new data
            try:
                budgeting.update(data)
                return jsonify(budgeting.read())
            except Exception as e:
                return {'message': f'Error updating budgeting entry: {e}'}, 500

        def delete(self):
            """
            Delete a budgeting entry.
            """
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for deleting a budgeting entry'}, 400

            # Find the budgeting entry by ID
            budgeting = Budgeting.query.get(data['id'])
            if not budgeting:
                return {'message': 'Budgeting entry not found'}, 404

            # Delete the budgeting entry
            try:
                budgeting.delete()
                return {'message': 'Budgeting entry deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting budgeting entry: {e}'}, 500

    api.add_resource(_CRUD, '/budgeting')