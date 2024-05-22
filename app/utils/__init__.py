import os

from ...scripts.sharepoint import upload_file_to_sharepoint, upload_folder_to_sharepoint, create_folder_in_sharepoint, get_access_token
from ...scripts.delete_folder import delete_file_or_folder

def upload_to_share_porint(pdf_folder_path, cohort):
    # Move to .env file

    # ##################################
    # # ㊙️ Upload to SharePoint
    # ##################################
    # Credentials and SharePoint information
    client_id = '6ab526e0-c314-4736-bb76-536dc241fe5e'
    client_secret = '0ZF8Q~afzsm0T4LQ9jEGJT6s26XZZlp1CKA1idzA'
    tenant_id = '825c9d58-d758-4658-a35a-49b607ca99a5'
    site_id = 'f9ac8ea8-56b1-4bdb-99d6-64efa51997df'

    # Folder in SharePoint where the new folder will be created
    base_folder_path = 'Documents/AI projects'

    # Get the access token
    access_token = get_access_token(client_id, client_secret, tenant_id)

    # Local folder path and name
    local_folder_path = pdf_folder_path  # This is the local folder path where your PDFs are located
    folder_name_to_create = os.path.basename(local_folder_path)

    # The full folder path on SharePoint where you want the new folder to be created
    folder_path = os.path.join(base_folder_path, cohort, folder_name_to_create).replace('\\', '/')

    # Create the folder and upload files to SharePoint
    if access_token:
        try:
            upload_folder_to_sharepoint(access_token, site_id, folder_path, local_folder_path)
            print(f'All files from {local_folder_path} have been uploaded to {folder_path} on SharePoint.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Could not get access token')


def delete_folder_and_files_from_local_storage(file_name):
    ##################################
    # ㊙️ Delete Files
    ##################################
    # Delete the folders and all their contents recursively
    delete_path = os.path.join('uploads', file_name)
    delete_file_or_folder(delete_path)

    delete_path = os.path.join('content', file_name)
    delete_file_or_folder(delete_path)

    # delete_file_or_folder(local_folder_path)

    print("Folders and all their contents have been deleted successfully.")