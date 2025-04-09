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

            if not data or 'caption' not in data or 'platform' not in data or 'post_type' not in data or 'content' not in data:
                return {'message': 'Caption, platform, post_type, and content are required'}, 400

            post = Palomar(
                caption=data.get('caption'),
                platform=data.get('platform'),
                post_type=data.get('post_type'),
                content=data.get('content')
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
            post_list = [p.read() for p in posts]

            return jsonify(post_list)

        @token_required()
        @cross_origin(supports_credentials=True)
        def put(self):
            data = request.get_json()

            if not data or 'id' not in data:
                return {'message': 'ID is required for updating a post'}, 400

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
                return {'message': 'ID is required for deleting a post'}, 400

            post = Palomar.query.get(data['id'])
            if not post:
                return {'message': 'Post not found'}, 404

            try:
                post.delete()
                return {'message': 'Post deleted successfully'}, 200
            except Exception as e:
                return {'message': f'Error deleting post: {e}'}, 500

    api.add_resource(_CRUD, '/palomar')
