import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.user import User

# Create a Blueprint for the user API
user_api = Blueprint('user_api', __name__, url_prefix='/api')

# Create an Api object and associate it with the Blueprint
# API docs: https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:
    """
    Define the API endpoints for the User model.
    """
    class _BULK_CRUD(Resource):
        """
        Users API operation for bulk Create and Read.
        """

        def post(self):
            """
            Handle bulk user creation by sending POST requests to the single user endpoint.
            """
            users = request.get_json()

            if not isinstance(users, list):
                return {'message': 'Expected a list of user data'}, 400

            results = {'errors': [], 'success_count': 0, 'error_count': 0}

            with current_app.test_client() as client:
                for user in users:
                    # Set a default password as we don't have it for bulk creation
                    user["password"] = app.config['DEFAULT_PASSWORD']

                    # Simulate a POST request to the single user creation endpoint
                    response = client.post('/api/user', json=user)

                    if response.status_code == 200:
                        results['success_count'] += 1
                    else:
                        results['errors'].append(response.get_json())
                        results['error_count'] += 1

            return jsonify(results)
        
        @token_required()
        def get(self):
            """
            Retrieve all users.
            """
            current_user = g.current_user
            users = User.query.all()  # extract all users from the database

            # Prepare a JSON list of user dictionaries
            json_ready = []
            for user in users:
                user_data = user.read()
                if current_user.role == 'Admin' or current_user.id == user.id:
                    user_data['access'] = ['rw']  # read-write access control
                else:
                    user_data['access'] = ['ro']  # read-only access control
                json_ready.append(user_data)

            return jsonify(json_ready)

    class _CRUD(Resource):
        """
        Users API operation for Create, Read, Update, Delete.
        """

        def post(self):
            """
            Create a new user.
            """
            body = request.get_json()

            # Validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': 'Name is missing, or is less than 2 characters'}, 400

            # Validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': 'User ID is missing, or is less than 2 characters'}, 400

            # Setup minimal USER OBJECT
            user_obj = User(name=name, uid=uid)

            # Add user to database
            user = user_obj.create(body)  # pass the body elements to be saved in the database
            if not user:  # failure returns error message
                return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

            return jsonify(user.read())
        
        @token_required()
        def get(self):
            """
            Return the current user and return as a JSON object.
            """
            user = g.current_user
            user_data = user.read()
            return jsonify(user_data)

        @token_required()
        def put(self):
            """
            Update a user.
            """
            current_user = g.current_user
            body = request.get_json()

            # Admin-specific update handling
            if current_user.role == 'Admin':
                uid = body.get('uid')
                if uid is None or uid == current_user.uid:
                    user = current_user  # Admin is updating themselves
                else:
                    user = User.query.filter_by(_uid=uid).first()
                    if user is None:
                        return {'message': f'User {uid} not found'}, 404
            else:
                user = current_user  # Non-admin can only update themselves

            # Update the user object with the new data
            user.update(body)

            return jsonify(user.read())

        @token_required("Admin")
        def delete(self):
            """
            Delete a user.
            """
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 404
            json = user.read()
            user.delete()
            return f"Deleted user: {json}", 204  # use 200 to test with Postman

    class _Security(Resource):
        """
        Security-related API operations.
        """

        def post(self):
            """
            Authenticate a user and generate a JWT token.
            """
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400

                # Get Data
                uid = body.get('uid')
                if uid is None:
                    return {'message': 'User ID is missing'}, 401
                password = body.get('password')
                if not password:
                    return {'message': 'Password is missing'}, 401

                # Find user
                user = User.query.filter_by(_uid=uid).first()

                if user is None or not user.is_password(password):
                    return {'message': "Invalid user id or password"}, 401

                # Generate token
                token = jwt.encode(
                    {"_uid": user._uid},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                resp = Response(f"Authentication for {user._uid} successful")
                resp.set_cookie(
                    current_app.config["JWT_TOKEN_NAME"],
                    token,
                    max_age=3600,
                    secure=True,
                    httponly=True,
                    path='/',
                    samesite='None'  # This is the key part for cross-site requests
                )
                return resp
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500

        @token_required()
        def delete(self):
            """
            Invalidate the current user's token by setting its expiry to 0.
            """
            current_user = g.current_user
            try:
                # Generate a token with practically 0 age
                token = jwt.encode(
                    {"_uid": current_user._uid, "exp": datetime.utcnow()},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )

                # Prepare a response indicating the token has been invalidated
                resp = Response("Token invalidated successfully")
                resp.set_cookie(
                    current_app.config["JWT_TOKEN_NAME"],
                    token,
                    max_age=0,  # Immediately expire the cookie
                    secure=True,
                    httponly=True,
                    path='/',
                    samesite='None'
                )
                return resp
            except Exception as e:
                return {
                    "message": "Failed to invalidate token",
                    "error": str(e)
                }, 500
    
    class _ID(Resource):  # Individual identification API operation
        @token_required()
        def get(self):
            ''' Retrieve the current user from the token_required authentication check '''
            current_user = g.current_user
            ''' Return the current user as a json object '''
            return jsonify(current_user.read())
            
    class _GradeData(Resource):
        """
        Grade data API operations
        """
        
        @token_required()
        def get(self):
            """
            Get the grade data for a user.
            """
            current_user = g.current_user
            
            # If request includes a UID parameter and user is admin, get that user's grade data
            uid = request.args.get('uid')
            if current_user.role == 'Admin' and uid:
                user = User.query.filter_by(_uid=uid).first()
                if not user:
                    return {'message': f'User {uid} not found'}, 404
            else:
                user = current_user  # Get the current user's grade data
                
            return jsonify({'uid': user.uid, 'grade_data': user.grade_data})
        
        @token_required()
        def post(self):
            """
            Add or update grade data for a user.
            """
            current_user = g.current_user
            body = request.get_json()
            
            # Determine which user's grade data to update
            uid = body.get('uid')
            if current_user.role == 'Admin' and uid:
                user = User.query.filter_by(_uid=uid).first()
                if not user:
                    return {'message': f'User {uid} not found'}, 404
            else:
                # Non-admins can only update their own grade data
                if uid and uid != current_user.uid and current_user.role != 'Admin':
                    return {'message': 'Permission denied: You can only update your own grade data'}, 403
                user = current_user
            
            # Get the grade data from the request
            grade_data = body.get('grade_data')
            if not grade_data:
                return {'message': 'Grade data is missing'}, 400
                
            # Update the user's grade data
            user.update({'grade_data': grade_data})
            
            return jsonify({'message': 'Grade data updated successfully', 'uid': user.uid, 'grade_data': user.grade_data})

    class _APExam(Resource):
        """
        AP exam data API operations
        """
        
        @token_required()
        def get(self):
            """
            Get the AP exam data for a user.
            """
            current_user = g.current_user
            
            # If request includes a UID parameter and user is admin, get that user's AP exam data
            uid = request.args.get('uid')
            if current_user.role == 'Admin' and uid:
                user = User.query.filter_by(_uid=uid).first()
                if not user:
                    return {'message': f'User {uid} not found'}, 404
            else:
                user = current_user  # Get the current user's AP exam data
                
            return jsonify({'uid': user.uid, 'ap_exam': user.ap_exam})
        
        @token_required()
        def post(self):
            """
            Add or update AP exam data for a user.
            """
            current_user = g.current_user
            body = request.get_json()
            
            # Determine which user's AP exam data to update
            uid = body.get('uid')
            if current_user.role == 'Admin' and uid:
                user = User.query.filter_by(_uid=uid).first()
                if not user:
                    return {'message': f'User {uid} not found'}, 404
            else:
                # Non-admins can only update their own AP exam data
                if uid and uid != current_user.uid and current_user.role != 'Admin':
                    return {'message': 'Permission denied: You can only update your own AP exam data'}, 403
                user = current_user
            
            # Get the AP exam data from the request
            ap_exam = body.get('ap_exam')
            if not ap_exam:
                return {'message': 'AP exam data is missing'}, 400
                
            # Update the user's AP exam data
            user.update({'ap_exam': ap_exam})
            
            return jsonify({'message': 'AP exam data updated successfully', 'uid': user.uid, 'ap_exam': user.ap_exam})

# Register the API resources with the Blueprint
api.add_resource(UserAPI._ID, '/id')
api.add_resource(UserAPI._BULK_CRUD, '/users')
api.add_resource(UserAPI._CRUD, '/user')
api.add_resource(UserAPI._Security, '/authenticate')
api.add_resource(UserAPI._GradeData, '/grade_data')
api.add_resource(UserAPI._APExam, '/apexam')