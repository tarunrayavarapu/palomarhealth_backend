# palomar_api.py
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from __init__ import db
from model.palomar import Palomar
from api.jwt_authorize import token_required

palomar_api = Blueprint('palomar_api', __name__, url_prefix='/api')
CORS(palomar_api, supports_credentials=True)
api = Api(palomar_api)

class PalomarAPI:

    class _CRUD(Resource):
        
        @token_required()
        @cross_origin(supports_credentials=True)
        def post(self):
            data = request.get_json()
            required_fields = ['caption', 'platform', 'post_type', 'content']
            if not all(field in data for field in required_fields):
                return {'message': 'All fields (caption, platform, post_type, content) are required'}, 400

            post = Palomar(
                caption=data['caption'],
                platform=data['platform'],
                post_type=data['post_type'],
                content=data['content']
            )

            try:
                post.create()
                return jsonify(post.read())
            except Exception as e:
                return {'message': f'Error saving post: {e}'}, 500

        @token_required()
        @cross_origin(supports_credentials=True)
        def get(self):
            post_id = request.args.get('id')
            if post_id:
                post = Palomar.query.get(post_id)
                if not post:
                    return {'message': 'Post not found'}, 404
                return jsonify(post.read())
            posts = Palomar.query.all()
            return jsonify([post.read() for post in posts])

        @token_required()
        @cross_origin(supports_credentials=True)
        def put(self):
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Post ID is required for update'}, 400

            post = Palomar.query.get(data['id'])
            if not post:
                return {'message': 'Post not found'}, 404

            try:
                post.update(data)
                return jsonify(post.read())
            except Exception as e:
                return {'message': f'Error updating post: {e}'}, 500

        @token_required()
        @cross_origin(supports_credentials=True)
        def delete(self):
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Post ID is required'}, 400

            post = Palomar.query.get(data['id'])
            if not post:
                return {'message': 'Post not found'}, 404

            try:
                post.delete()
                return {'message': 'Post deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting post: {e}'}, 500

    class _ANALYTICS(Resource):
        def get(self):
            analytics_data = {
                "note": "This is tester data. Real analytics will be displayed here later.",
                "engagement": {
                    "likes": 42,
                    "comments": 17,
                    "shares": 9,
                    "clicks": 120,
                },
                "trending_score": 78.9
            }
            return jsonify(analytics_data)

    # Register endpoints
    api.add_resource(_CRUD, '/palomar')
    api.add_resource(_ANALYTICS, '/palomar/analytics')
