import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from datetime import datetime
from __init__ import app, db  # Ensure db is imported
from api.jwt_authorize import token_required
from model.budgeting import Budgeting  # Assuming your Budgeting model is in the 'budgeting' module
from model.user import User

budgeting_api = Blueprint('budgeting_api', __name__, url_prefix='/api')
CORS(budgeting_api, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])
api = Api(budgeting_api)

class BudgetingAPI:
    """
    Define the API CRUD endpoints for the Budgeting model.
    Operations include creating, retrieving, updating, and deleting budgeting entries.
    """
    
    class _CRUD(Resource):
        @token_required()
        @cross_origin(supports_credentials=True)
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            
            if not data or 'expense' not in data or 'cost' not in data or 'category' not in data:
                return jsonify({"message": "Expense, cost, and category are required"}), 400
            
            budgeting = Budgeting(
                expense=data.get('expense'),
                cost=data.get('cost'),
                category=data.get('category'),
                user_id=current_user.id
            )
            
            db.session.add(budgeting)
            db.session.commit()
            
            return jsonify({"message": "Budgeting entry created successfully"})
        
        @token_required()
        def get(self):
            current_user = g.current_user
            budgeting_entries = Budgeting.query.filter_by(user_id=current_user.id).all()
            return jsonify([entry.read() for entry in budgeting_entries])
        
        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            budgeting_id = data.get('id')
            
            if not budgeting_id:
                return jsonify({"message": "ID is required for updating a budgeting entry"}), 400
            
            budgeting = Budgeting.query.filter_by(id=budgeting_id, user_id=current_user.id).first()
            if not budgeting:
                return jsonify({"message": "Budgeting entry not found"}), 404
            
            budgeting.expense = data.get('expense', budgeting.expense)
            budgeting.cost = data.get('cost', budgeting.cost)
            budgeting.category = data.get('category', budgeting.category)
            
            db.session.commit()
            return jsonify({"message": "Budgeting entry updated successfully"})
        
        @token_required()
        def delete(self):
            current_user = g.current_user
            data = request.get_json()
            budgeting_id = data.get('id')
            
            if not budgeting_id:
                return jsonify({"message": "ID is required for deleting a budgeting entry"}), 400
            
            budgeting = Budgeting.query.filter_by(id=budgeting_id, user_id=current_user.id).first()
            if not budgeting:
                return jsonify({"message": "Budgeting entry not found"}), 404
            
            db.session.delete(budgeting)
            db.session.commit()
            return jsonify({"message": "Budgeting entry deleted successfully"})

api.add_resource(BudgetingAPI._CRUD, '/budgeting')