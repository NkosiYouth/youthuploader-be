from flask import request, jsonify, Blueprint
from app.models import Supervisor  # Import the User model

supervisor_bp = Blueprint('supervisor', __name__)

@supervisor_bp.route('/supervisors', methods=['POST'])
def create_host():
    data = request.json
    user = Supervisor(**data)
    user_id = user.save()
    return jsonify({"message": "Supervisor created successfully", "supervisor_id": user_id}), 201

# Existing route to get all users
@supervisor_bp.route('/supervisors', methods=['GET'])
def get_all_supervisors():
    supervisors = Supervisor.get_all_supervisors()
    return jsonify(supervisors)
