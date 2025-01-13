from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

# Initialize Blueprint and API for waypoints
waypoints_api = Blueprint('waypoints_api', __name__, url_prefix='/api')
api = Api(waypoints_api)

# Simulated database
groups = [
    {"id": 1, "name": "Fractures"},
    {"id": 2, "name": "Burns"},
    {"id": 3, "name": "Allergic Reactions"},
    {"id": 4, "name": "Head Injuries"},
    {"id": 5, "name": "Muscle Strains"}
]

channels = {
    "Fractures": [
        {"id": 1, "name": "Saint Louis Hospital"},
        {"id": 2, "name": "Central Clinic"},
        {"id": 3, "name": "Necker Hospital"}
    ],
    "Burns": [
        {"id": 4, "name": "Georges Pompidou Hospital"},
        {"id": 5, "name": "Pitié-Salpêtrière Hospital"}
    ]
}

posts = []  # List to store user posts


class WaypointsAPI:
    """
    Class encapsulating Waypoints API resources.
    """
    
    # Utility function to find channel name by ID
    @staticmethod
    def get_channel_name_by_id(channel_id):
        for group_channels in channels.values():
            for channel in group_channels:
                if channel["id"] == channel_id:
                    return channel["name"]
        return None

    class Groups(Resource):
        """
        Resource for fetching groups.
        """
        def post(self):
            section_name = request.json.get('section_name', '')
            if section_name == "Wellness Waypoints":
                return jsonify(groups)
            return jsonify({"message": "Section not found"}), 404

    class Channels(Resource):
        """
        Resource for fetching channels by group name.
        """
        def post(self):
            group_name = request.json.get('group_name', '')
            if group_name in channels:
                return jsonify(channels[group_name])
            return jsonify({"message": "Group not found"}), 404

    class Posts(Resource):
        """
        Resource for adding a new post.
        """
        def post(self):
            post_data = request.json
            title = post_data.get('title')
            comment = post_data.get('comment')
            channel_id = post_data.get('channel_id')

            if title and comment and channel_id:
                channel_name = WaypointsAPI.get_channel_name_by_id(channel_id)
                if not channel_name:
                    return jsonify({"success": False, "message": "Channel not found."}), 404

                new_post = {
                    "id": len(posts) + 1,
                    "title": title,
                    "comment": comment,
                    "channel_name": channel_name,
                    "user_name": "Anonymous"
                }
                posts.append(new_post)
                return jsonify({"success": True, "message": "Post added successfully."}), 201
            return jsonify({"success": False, "message": "Invalid data provided."}), 400

    class FilterPosts(Resource):
        """
        Resource for fetching posts by channel.
        """
        def post(self):
            channel_id = request.json.get('channel_id')
            if not channel_id:
                return jsonify({"success": False, "message": "Channel ID is required."}), 400

            channel_name = WaypointsAPI.get_channel_name_by_id(channel_id)
            if not channel_name:
                return jsonify({"success": False, "message": "Channel not found."}), 404

            filtered_posts = [post for post in posts if post["channel_name"] == channel_name]
            return jsonify(filtered_posts)


# Add Resources to API
api.add_resource(WaypointsAPI.Groups, '/groups/filter')
api.add_resource(WaypointsAPI.Channels, '/channels/filter')
api.add_resource(WaypointsAPI.Posts, '/post')
api.add_resource(WaypointsAPI.FilterPosts, '/posts/filter')
