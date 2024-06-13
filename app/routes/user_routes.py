from flask import request, jsonify, Blueprint
from app.models.User import User  # Import the User model
from app.utils import upload_file_to_sharepoint, delete_file_or_folder

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    user_id = user.save()
    return jsonify({"message": "User created successfully", "user_id": user_id}), 201

# Route to verify and update user by id
@user_bp.route('/users/verify/<user_id>', methods=['PUT'], endpoint='verify_user')
def verify_and_update_user(user_id):
    data = request.json
    data['isValidated'] = True
    print(data)
    print(user_id)
    result = User.update_user(user_id, data)
    if result:
        upload_file_to_sharepoint(data['files'][0])
        delete_file_or_folder(data['files'][0])
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Route to update user by id
@user_bp.route('/users/<user_id>', methods=['PUT'], endpoint='update_user')
def update_user(user_id):
    data = request.json
    print(data)
    print(user_id)
    result = User.update_user(user_id, data)
    if result:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Route to get all users
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    query_params = request.args.to_dict()
    users = User.get_all_users(query_params)
    return jsonify(users)

# Route to get a user by ID
@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.find_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 404
