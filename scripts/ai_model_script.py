from PyPDF2 import PdfReader, PdfWriter
import io
import json
import requests
import os
import shutil
from dotenv import load_dotenv
load_dotenv()

from .pdf_image import convert_pdf_to_images, save_images_to_files

from .image_text_model import image_text_model
from .identify_document_and_type import identify_document_and_type
from .consolidate_data import consolidate_data

from .combine_all_orc import consolidate_ocr_results_based_on_digitization, get_ocr_text_for_document

from .llm_chain_extract_data import get_race_and_gender, get_pay_roll_data, get_contract_data

from .llm_json_to_single_string import json_to_text, merge_texts

from .user_data import get_user_output_data

from .split_rename_pdf import extract_page_names, update_page_names_with_user, split_pdf_into_pages, merge_pages_by_name

from .sharepoint import upload_file_to_sharepoint, upload_folder_to_sharepoint, create_folder_in_sharepoint, get_access_token

from .delete_folder import delete_file_or_folder

from app.models import User

def ai_model(file_path, file_name, cohort):
    ##################################
    # ㊙️ PDF To Image with PyMuPDF
    ##################################
    # Replace 'path_to_your_pdf_file.pdf' with the actual path to the PDF file

    storage_path =os.path.join('content', file_name)
    pdf_path = f"/uploads/{file_name}"
    pdf_path = file_path
    pdf_data = pdf_path

    # Step 2: Convert each PDF page to an image
    images = convert_pdf_to_images(pdf_path)  # Updated function call
    # Step 3: Save each image to a file and get the file paths
    image_file_paths = save_images_to_files(images, storage_path)  # Updated function call

    # Output the results
    print("㊙️ IMAGE FILE PATHS")
    print(image_file_paths)

    ##################################
    # ⭐ Image Text Model
    ##################################
    print("㊙️ IMAGE TO TEXT MODEL")
    results_list = image_text_model(image_file_paths)

    ##################################
    # 〽️ Identify Document and Type
    ##################################
    print("㊙️ IMAGE CLASSIFICATION")
    image_classification = identify_document_and_type(results_list)


    ##################################
    # ㊙️ Consolidate Data
    ##################################
    consolidated_data = consolidate_data(image_file_paths, results_list, image_classification)
    updated_data = consolidated_data

    ##################################
    # ✏️ Combine All ORC
    ##################################
    consolidated_text = consolidate_ocr_results_based_on_digitization(updated_data)
    print(consolidated_text)
    # Assuming updated_data is a list of entries where each entry is a list or tuple as expected
    document_name_to_search = "EEA1"
    ee_ocr_text = get_ocr_text_for_document(updated_data, document_name_to_search)
    print(ee_ocr_text)

    document_name_to_search = "Payroll"
    payroll_ocr_text = get_ocr_text_for_document(updated_data, document_name_to_search)
    print(payroll_ocr_text)

    document_name_to_search = "Employment Contract"
    ep_contract_ocr_text = get_ocr_text_for_document(updated_data, document_name_to_search)
    print(ep_contract_ocr_text)

    ##################################
    # ㊙️ LLM Chains to Extract Data
    ##################################
    race_and_gender = get_race_and_gender(ee_ocr_text)
    payroll_data = get_pay_roll_data(payroll_ocr_text)
    contract_data = get_contract_data(ep_contract_ocr_text)

    ##################################
    # ㊙️ LLM JSON to Single String
    ##################################
    llm_document_to_text = race_and_gender
    race_and_gender_text = json_to_text(race_and_gender)
    print(race_and_gender_text)

    llm_document_to_text = payroll_data
    payroll_data_text = json_to_text(payroll_data)
    print(payroll_data_text)

    llm_document_to_text = contract_data
    contract_data_text = json_to_text(contract_data)
    print(contract_data_text)

    # Merge the texts
    merged_text = merge_texts(consolidated_text, race_and_gender_text, payroll_data_text, contract_data_text)
    print(merged_text)

    ##################################
    # ㊙️ Extract User Data from String
    ##################################
    output = get_user_output_data(merged_text)
    print(output)
    user_data_str = output['text']
    user_data_json = json.loads(output['text'])
    print(user_data_json)

    ##################################
    # ㊙️ Split and Rename PDF
    ##################################
    page_names = extract_page_names(consolidated_data)
    print(page_names)

    updated_page_names = update_page_names_with_user(page_names, user_data_str)
    print(updated_page_names)

    page_files = split_pdf_into_pages(pdf_data)
    # Funct ion to merge the pages by name and save them to PDF files
    created_file_names = merge_pages_by_name(updated_page_names, page_files, user_data_str)

    user_data = json.loads(user_data_str)

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
    # ㊙️ Upload to SharePoint
    ##################################
    # Credentials and SharePoint information
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    tenant_id = os.getenv('TENANT_ID')
    site_id = os.getenv('SITE_ID')

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
    # ㊙️ Uploading Data to MONGO DB
    ##################################
    user = User(**user_data_json)
    user.files = [ file_name ]
    user.cohort = cohort
    user.isValidated = False

    print("㊙️ USER DATA:")
    print(user)

    result = user.save()
    print(f"MONGO DB Record ID: {result}")

    ##################################
    # ㊙️ Delete Files
    ##################################
    # Delete the folders and all their contents recursively
    delete_path = os.path.join('uploads', file_name)
    delete_file_or_folder(delete_path)

    delete_path = os.path.join('content', file_name)
    delete_file_or_folder(delete_path)

    delete_file_or_folder(local_folder_path)

    print("Folders and all their contents have been deleted successfully.")

