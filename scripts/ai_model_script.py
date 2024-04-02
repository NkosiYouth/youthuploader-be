from PyPDF2 import PdfReader, PdfWriter
import io
import json

from .pdf_image import convert_pdf_to_images, save_images_to_files

from .image_text_model import image_text_model
from .identify_document_and_type import identify_document_and_type
from .consolidate_data import consolidate_data
from .verify_non_digital_documents import process_non_digital_responses
from .update_image_texts_from_non_digital_documents import update_ocr_responses
from .combine_all_orc import consolidate_ocr_results_based_on_digitization

from .inspect_eaa1_document import get_ocr_text_for_eaa1_document

from .payroll_document import get_ocr_text_for_pay_roll
from .employment_contract_data import get_ocr_text_for_employment_contract

def ai_model(file_path, file_name, cohort):
    ##################################
    # ㊙️ PDF To Image with PyMuPDF
    ##################################
    # Replace 'path_to_your_pdf_file.pdf' with the actual path to the PDF file

    storage_path = f'content/{file_name}'
    pdf_path = f"/uploads/{file_name}"
    pdf_path = file_path

    # Step 2: Convert each PDF page to an image
    images = convert_pdf_to_images(pdf_path)  # Updated function call
    # Step 3: Save each image to a file and get the file paths
    image_file_paths = save_images_to_files(images, storage_path)  # Updated function call

    # Output the results
    print(image_file_paths)

    ##################################
    # ⭐ Image Text Model
    ##################################
    results_list = image_text_model(image_file_paths)

    ##################################
    # 〽️ Identify Document and Type
    ##################################
    image_classification = identify_document_and_type(results_list)


    ##################################
    # ㊙️ Consolidate Data
    ##################################
    consolidated_data = consolidate_data(image_file_paths, results_list, image_classification)

    ##################################
    # ❇️ Verify Non-Digital Documents
    ##################################
    # Then, you would call this function as before and pass its output to `update_ocr_responses`:
    processed_responses = process_non_digital_responses(consolidated_data)
    print(processed_responses)

    ##################################
    # 🧊 Update Image Texts From Non-Digital Documents
    ##################################
    # Usage of the function goes here
    # Assuming consolidated_data and processed_responses are already defined and populated
    updated_data = update_ocr_responses(consolidated_data, processed_responses)
    print(updated_data)

    ##################################
    # ✏️ Combine All ORC
    ##################################
    consolidated_text = consolidate_ocr_results_based_on_digitization(updated_data)
    print(consolidated_text)

    ##################################
    # ❄️ Inspect EAA1 Document
    ##################################
    # Example usage:
    # Assuming updated_data is a list of entries where each entry is a list or tuple as expected
    document_name_to_search = "EEA1"
    ee_ocr_text = get_ocr_text_for_eaa1_document(updated_data, document_name_to_search)
    print(ee_ocr_text)
    API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/b4c504c2-24f0-423a-8884-dc88ea143607"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    # Assuming ee_ocr_text is obtained from get_ocr_text_for_document function
    if ee_ocr_text is not None:
        payload = {
            "question": ee_ocr_text,
        }
        output = query(payload)
        race_and_gender = output['text']
        print(race_and_gender)
    else:
        race_and_gender = None

    # Example usage of the function:
    race_and_gender_text = json_to_text(race_and_gender)
    print(race_and_gender_text)

    ##################################
    # ⭐ Payroll Document
    ##################################
    # Example usage:
    # Assuming updated_data is a list of entries where each entry is a list or tuple as expected
    document_name_to_search = "Payroll"
    payroll_ocr_text = get_ocr_text_for_pay_roll(updated_data, document_name_to_search)

    # Print the combined OCR text for the document name
    print(payroll_ocr_text)
    API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/3b379972-f629-40c3-a70f-fc7899d3a0db"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    # Assuming ee_ocr_text is obtained from get_ocr_text_for_document function
    if ee_ocr_text is not None:
        payload = {
            "question": payroll_ocr_text,
        }
        output = query(payload)
        payroll_data = output['text']
        print(payroll_data)
    else:
        payroll_data = None

    def json_to_text(payroll_data):
        if payroll_data is None:
            return 'None'
        # Assuming json_data is a string representation of a JSON object.
        try:
            # Convert string to a dictionary
            data_dict = json.loads(payroll_data)
            # Join the key-value pairs into a string
            return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
        except (json.JSONDecodeError, TypeError):
            return 'Invalid JSON or input type'

    # Example usage of the function:
    payroll_data_text = json_to_text(payroll_data)
    print(payroll_data_text)

    ##################################
    # ㊙️ Employment Contract Data
    ##################################
    # Example usage:
    # Assuming updated_data is a list of entries where each entry is a list or tuple as expected
    document_name_to_search = "Employment Contract"
    ep_contract_ocr_text = get_ocr_text_for_employment_contract(updated_data, document_name_to_search)

    # Print the combined OCR text for the document name
    print(ep_contract_ocr_text)

    API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/a6fb0bf0-0612-4236-8fd6-a4bb5d2085ce"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    # Assuming ee_ocr_text is obtained from get_ocr_text_for_document function
    if ee_ocr_text is not None:
        payload = {
            "question": ep_contract_ocr_text,
        }
        output = query(payload)
        contract_data = output['text']
        print(contract_data)
    else:
        contract_data = None

        def json_to_text(contract_data):
            if contract_data is None:
                return 'None'
            # Assuming json_data is a string representation of a JSON object.
            try:
                # Convert string to a dictionary
                data_dict = json.loads(payroll_data)
                # Join the key-value pairs into a string
                return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
            except (json.JSONDecodeError, TypeError):
                return 'Invalid JSON or input type'

    # Example usage of the function:
    contract_data_text = json_to_text(contract_data)
    print(contract_data_text)


    ##################################
    # ㊙️ Merge texts all texts
    ##################################
    def merge_texts(consolidated_text, race_and_gender_text, payroll_data_text, contract_data_text):
        # Initialize a list to hold all text parts
        texts = []

        # Check each text and add it to the list if it exists, otherwise add "N/A"
        texts.append(consolidated_text if consolidated_text is not None else "Consolidated Text: N/A")
        texts.append(race_and_gender_text if race_and_gender_text is not None else "Race and Gender Text: N/A")
        texts.append(payroll_data_text if payroll_data_text is not None else "Payroll Data Text: N/A")
        texts.append(contract_data_text if contract_data_text is not None else "Contract Data Text: N/A")

        # Now, concatenate all parts with a space in between
        merged_text = ' '.join(texts)
        return merged_text

    # Merge the texts
    merged_text = merge_texts(consolidated_text, race_and_gender_text, payroll_data_text, contract_data_text)
    print(merged_text)

     ##################################
    # ㊙️ Get User Data
    ##################################

    API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/ce5137d2-eb6e-497f-82d5-1ad3cfd7b3d4"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    output = query({
        "question": merged_text,
    })
    print(output)

    user_data = output['text']
    user_data_json = json.loads(output['text'])
    print(user_data_json)

     ##################################
    # ㊙️ Compile PDF/s
    ##################################

    def extract_page_names(consolidated_data):
        page_names = []
        for data in consolidated_data:
            image_file_path, ocr_results, image_classification = data

            # Check if image_classification is already a dict
            if isinstance(image_classification, dict):
                classification_dict = image_classification
            else:
                # If it's a string, then load it as JSON
                classification_dict = json.loads(image_classification)

            document_name = classification_dict.get('document_name', 'Unknown')
            page_names.append(document_name)

        return page_names

    # Usage:
    # Assuming consolidated_data is already defined and contains your tuples
    page_names = extract_page_names(consolidated_data)
    print(page_names)

    def update_page_names_with_user(page_names, user_data):
        # Parse the JSON string into a dictionary
        user_data = json.loads(user_data)

        # Extract first name, last name, and RSA ID number from the user_data dictionary
        first_name = user_data.get('first_name', '').strip()  # Ensure the keys match those in your JSON
        last_name = user_data.get('last_name', '').strip()    # Ensure the keys match those in your JSON
        rsa_id_number = user_data.get('rsa_id_number', '').strip()  # Ensure the keys match those in your JSON

        # Update page_names with the user's information
        updated_page_names = [f"{name} - {first_name} {last_name} - {rsa_id_number}" for name in page_names]

        return updated_page_names

    updated_page_names = update_page_names_with_user(page_names, user_data)
    print(updated_page_names)

    def split_pdf_into_pages(pdf_data):
        reader = PdfReader(pdf_data)
        page_files = []

        for i in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            page_io = io.BytesIO()
            writer.write(page_io)
            page_io.seek(0)
            page_files.append(page_io)

        return page_files

    def merge_pages_by_name(updated_page_names, page_files):
        pages_by_name = {}

        for name, page_file in zip(updated_page_names, page_files):
            if name not in pages_by_name:
                pages_by_name[name] = [page_file]
            else:
                pages_by_name[name].append(page_file)

        for name, pages in pages_by_name.items():
            writer = PdfWriter()

            for page in pages:
                page.seek(0)
                reader = PdfReader(page)
                writer.add_page(reader.pages[0])

            # Use the name directly without replacing spaces with underscores
            output_filename = f"{name}.pdf"
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)
                print(f"Saved PDF file: {output_filename}")

        return list(pages_by_name.keys())

    def merge_pages_by_name(updated_page_names, page_files, user_data):
        # Parse the JSON string into a dictionary to extract user info
        user_data = json.loads(user_data)
        first_name = user_data.get('first_name', '').strip()
        last_name = user_data.get('last_name', '').strip()
        rsa_id_number = user_data.get('rsa_id_number', '').strip()

        # Create the folder name based on the user's information
        pdf_folder_name = f"{first_name} {last_name} - {rsa_id_number}"

        # Create the directory if it does not exist
        if not os.path.exists(pdf_folder_name):
            os.makedirs(pdf_folder_name)

        pages_by_name = {}
        for name, page_file in zip(updated_page_names, page_files):
            if name not in pages_by_name:
                pages_by_name[name] = [page_file]
            else:
                pages_by_name[name].append(page_file)

        for name, pages in pages_by_name.items():
            writer = PdfWriter()
            for page in pages:
                page.seek(0)
                reader = PdfReader(page)
                writer.add_page(reader.pages[0])

            # Save the PDF in the new directory
            output_filename = os.path.join(pdf_folder_name, f"{name}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)
                print(f"Saved PDF file: {output_filename}")

        return list(pages_by_name.keys())

    # Assuming 'uploaded' is the dictionary returned from files.upload() and contains your PDF data
    # Assuming we already have user_data_json as a JSON string with the user's information
    page_files = split_pdf_into_pages(pdf_data)

    # Finally, call the function to merge the pages by name and save them to PDF files
    created_file_names = merge_pages_by_name(updated_page_names, page_files, user_data)

    user_data = json.loads(user_data)

    # Extract user information again
    first_name = user_data.get('first_name', '').strip()
    last_name = user_data.get('last_name', '').strip()
    rsa_id_number = user_data.get('rsa_id_number', '').strip()

    # Construct the folder name
    pdf_folder_name = f"{first_name} {last_name} - {rsa_id_number}"

    # Get the absolute path of the folder
    pdf_folder_path = os.path.abspath(pdf_folder_name)

    print(f"The folder path is: {pdf_folder_path}")

     ##################################
    # ㊙️ Upload FIles To SharePoint
    ##################################
    import requests

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
        # First, try to create the folder in SharePoint
        create_folder_in_sharepoint(access_token, site_id, folder_path)

        # Then, iterate over each file in the local folder and upload
        for root, dirs, files in os.walk(local_folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as file_data:
                    # Construct the path where the file will live inside SharePoint
                    relative_path = os.path.relpath(root, local_folder_path)
                    sharepoint_file_path = os.path.join(folder_path, relative_path, file_name).replace('\\', '/')

                    # Upload the file
                    try:
                        pdf_path = upload_file_to_sharepoint(access_token, site_id, sharepoint_file_path, file_name, file_data.read())
                        print(f'File {file_name} uploaded to SharePoint. PDF Path: {pdf_path}')
                    except Exception as e:
                        print(f'An error occurred while uploading {file_name}: {e}')
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
        folder_path = os.path.join(base_folder_path, folder_name_to_create).replace('\\', '/')

        # Create the folder and upload files to SharePoint
        if access_token:
            try:
                upload_folder_to_sharepoint(access_token, site_id, folder_path, local_folder_path)
                print(f'All files from {local_folder_path} have been uploaded to {folder_path} on SharePoint.')
            except Exception as e:
                print(f'An error occurred: {e}')
        else:
            print('Could not get access token')


     ##################################
    # ㊙️ Delete running files
    ##################################

    import shutil
    import os

    # Assuming pdf_folder_path contains the path to the local folder you want to delete
    pdf_folder_path = '/content/LISBETH NOBELA NGOBENI - 9904060525080'  # Update to your folder path

    # Check if the folder exists
    if os.path.exists(pdf_folder_path) and os.path.isdir(pdf_folder_path):
        shutil.rmtree(pdf_folder_path)
        print(f"The folder {pdf_folder_path} has been deleted.")
    else:
        print(f"The folder {pdf_folder_path} does not exist.")