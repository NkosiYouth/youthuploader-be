from flask import request, jsonify, Blueprint
from app.models.User import User  # Import the User model
from app.utils import upload_folder_to_sharepoint, delete_file_or_folder, get_access_token
import os
from dotenv import load_dotenv

load_dotenv()


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
    try:
        data = request.json
        data['isValidated'] = True
        result = User.update_user(user_id, data)

        if result:

            data = User.find_by_id(user_id)

            client_id =  os.getenv('CLIENT_ID')
            client_secret =  os.getenv('CLIENT_SECRET')
            tenant_id =  os.getenv('TENAT_ID')
            site_id =  os.getenv('SITE_ID')

            access_token = get_access_token(client_id, client_secret, tenant_id)

            if access_token:
                base_folder_path = 'Documents/AI projects'
                # local_folder_path = pdf_folder_path  # This is the local folder path where your PDFs are located
                local_folder_path = os.path.join(data['files'][0].replace(".pdf", ""))
                folder_name_to_create = os.path.basename(local_folder_path)
                 # The full folder path on SharePoint where you want the new folder to be created
                folder_path = os.path.join(base_folder_path, data['cohort'], folder_name_to_create).replace('\\', '/')

                upload_folder_to_sharepoint(access_token, site_id, folder_path, local_folder_path)
                print(f'All files from {local_folder_path} have been uploaded to {folder_path} on SharePoint.')

            else:
                    print('Could not get access token')
                    delete_file_or_folder(data['files'][0])

            return jsonify({"message": "User updated successfully"}), 200

        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(f'An error occurred: {e}')
        return jsonify({"message": "Bad Request"}), 400

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
