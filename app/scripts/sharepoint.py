import requests
import os

# Function to upload file to SharePoint
def upload_file_to_sharepoint(access_token, site_id, folder_path, file_name, file_data):
    folder_path_encoded = requests.utils.quote(folder_path.strip('/'))
    file_name_encoded = requests.utils.quote(file_name)
    endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path_encoded}/{file_name_encoded}:/content'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/octet-stream'
    }

    response = requests.put(endpoint, headers=headers, data=file_data)

    # Check for successful response
    if response.status_code in (201, 200):
        location = response.headers.get('Location')
        if not location:
            location = response.json().get('webUrl')
        return location
    else:
        raise Exception(f"Failed to upload file: {response.json()}")


# Function to create a folder in SharePoint
def create_folder_in_sharepoint(access_token, site_id, folder_path):
    endpoint = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{folder_path}:/children'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    body = {
        "name": os.path.basename(folder_path),
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }

    response = requests.post(endpoint, headers=headers, json=body)

    if response.status_code in (201, 200):
        print(f"Folder '{os.path.basename(folder_path)}' created in SharePoint.")
        return response.json()
    else:
        raise Exception(f"Failed to create folder: {response.json()}")


# Function to upload all files in a given local folder to a SharePoint folder
def upload_folder_to_sharepoint(access_token, site_id, folder_path, local_folder_path):
    # Iterate over each file in the local folder and upload
    for file_name in os.listdir(local_folder_path):
        # Make sure it's a file and not a directory
        if os.path.isfile(os.path.join(local_folder_path, file_name)):
            file_path = os.path.join(local_folder_path, file_name)
            with open(file_path, 'rb') as file_data:
                # Upload the file directly to the folder_path, without appending additional path components
                try:
                    file_location = upload_file_to_sharepoint(access_token, site_id, folder_path, file_name, file_data.read())
                    print(f'File {file_name} uploaded to SharePoint at {file_location}')
                except Exception as e:
                    print(f'An error occurred while uploading {file_name}: {e}')


# Define the function to get an access token for SharePoint
def get_access_token(client_id, client_secret, tenant_id):
    # Endpoint for obtaining the access token from Microsoft
    token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    # Prepare the data for the token request
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }

    # Headers for the token request
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the token request
    response = requests.post(token_endpoint, data=token_data, headers=token_headers)

    # Check for a successful request
    response.raise_for_status()

    # Return the access token
    return response.json().get("access_token")



