from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime
from model.palomar import Palomar  # Your model
from __init__ import app

# Define Blueprint for Palomar Health API
palomar_api = Blueprint('palomar_api', __name__, url_prefix='/api')
api = Api(palomar_api)

class PalomarAPI:
    """
    API for managing Palomar Health Posts.
    Includes create, read, update, delete, and analytics.
    """

    class _CRUD(Resource):
        def post(self):
            """
            Create a new PalomarHealth post
            """
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
            result = post.create()
            if result:
                return jsonify(post.read()), 201
            return {'message': 'Failed to create post'}, 500

        def put(self):
            """
            Update an existing PalomarHealth post
            """
            data = request.get_json()
            post_id = data.get('id')
            if not post_id:
                return {'message': 'Post ID is required for update'}, 400

            post = Palomar.query.get(post_id)
            if not post:
                return {'message': 'Post not found'}, 404

            post.update(data)
            return jsonify(post.read()), 200

        def delete(self):
            """
            Delete a PalomarHealth post
            """
            data = request.get_json()
            post_id = data.get('id')
            if not post_id:
                return {'message': 'Post ID is required'}, 400

            post = Palomar.query.get(post_id)
            if not post:
                return {'message': 'Post not found'}, 404

            post.delete()
            return jsonify({"message": "Post deleted successfully"}), 200

        def get(self):
            """
            Get all PalomarHealth posts
            """
            posts = Palomar.query.all()
            return jsonify([post.read() for post in posts]), 200

    class _ANALYTICS(Resource):
        def get(self):
            """
            Get dummy analytics for testing — real data to be added later.
            """
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
            return jsonify(analytics_data), 200

    # Register endpoints
    api.add_resource(_CRUD, '/palomar')
    api.add_resource(_ANALYTICS, '/palomar/analytics')
