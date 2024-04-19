from flask import request, jsonify, Blueprint
from app.models import HostAddress  # Import the User model

host_address_bp = Blueprint('host_address_bp', __name__)

@host_address_bp.route('/host-address', methods=['POST'])
def create_host():
    data = request.json
    user = HostAddress(**data)
    user_id = user.save()
    return jsonify({"message": "Hosr created successfully", "host": user_id}), 201

# Existing route to get all users
@host_address_bp.route('/host-address', methods=['GET'])
def get_all_hosts():
    users = HostAddress.get_all_addresses()
    return jsonify(users)

