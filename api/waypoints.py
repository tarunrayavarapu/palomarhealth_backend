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

waypoints = []  # List to store user waypoints


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

    class Waypoints(Resource):
        """
        Resource for adding a new waypoint.
        """
        def post(self):
            waypoints_data = request.json
            title = waypoints_data.get('title')
            comment = waypoints_data.get('comment')
            channel_id = waypoints_data.get('channel_id')

            if title and comment and channel_id:
                channel_name = WaypointsAPI.get_channel_name_by_id(channel_id)
                if not channel_name:
                    return jsonify({"success": False, "message": "Channel not found."}), 404

                new_waypoint = {
                    "id": len(waypoints) + 1,
                    "title": title,
                    "comment": comment,
                    "channel_name": channel_name,
                    "user_name": "Anonymous"
                }
                waypoints.append(new_waypoint)
                return jsonify({"success": True, "message": "Waypoints added successfully."}), 201
            return jsonify({"success": False, "message": "Invalid data provided."}), 400

    class FilterWaypoints(Resource):
        """
        Resource for fetching waypoints by channel.
        """
        def waypoint(self):
            channel_id = request.json.get('channel_id')
            if not channel_id:
                return jsonify({"success": False, "message": "Channel ID is required."}), 400

            channel_name = WaypointsAPI.get_channel_name_by_id(channel_id)
            if not channel_name:
                return jsonify({"success": False, "message": "Channel not found."}), 404

            filtered_waypoints = [waypoint for waypoint in waypoints if waypoint["channel_name"] == channel_name]
            return jsonify(filtered_waypoints)


# Add Resources to API
api.add_resource(WaypointsAPI.Groups, '/groups/filter')
api.add_resource(WaypointsAPI.Channels, '/channels/filter')
api.add_resource(WaypointsAPI.Waypoints, '/waypoints')
api.add_resource(WaypointsAPI.FilterWaypoints, '/waypoints/filter')

