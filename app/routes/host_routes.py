from flask import request, jsonify, Blueprint
from app.models import Host  # Import the User model

host_bp = Blueprint('host', __name__)

@host_bp.route('/hosts', methods=['POST'])
def create_host():
    data = request.json
    user = Host(**data)
    user_id = user.save()
    return jsonify({"message": "Hosr created successfully", "user_id": user_id}), 201

# Existing route to get all users
@host_bp.route('/hosts', methods=['GET'])
def get_all_hosts():
    users = Host.get_all_hosts()
    return jsonify(users)

