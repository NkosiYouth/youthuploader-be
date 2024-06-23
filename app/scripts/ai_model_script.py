import json
import os
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



from app.models import User, RawData, FailedDocuments


def store_to_failed_documents(file_name):
    raw_data = FailedDocuments(file_name)
    raw_data.save()

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
    # ⭐ Image Text Model || Retry Required
    ##################################
    print("㊙️ IMAGE TO TEXT MODEL")

    try:
        results_list = image_text_model(image_file_paths)
    except Exception as e:
        store_to_failed_documents(file_name)
        print(f"An error occurred: {e}")
        print("Exiting main function.")
        return

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
    # ✏️ Combine All OCR | Retry Required - 2 Tries
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
    # ㊙️ LLM Chains to Extract Data | Retry Required
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
    # ㊙️ Extract User Data from String | Retry Required
    ##################################
    output = get_user_output_data(merged_text)
    print(output)
    user_data_str = output['text']
    user_data_json = json.loads(output['text'])
    print(user_data_json)
    # Todo: Create a user inside MONGO DB... Wait for validation...
    # We need to put conslidated somwhere...

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
    # ㊙️ Uploading Data to MONGO DB
    ##################################

    user_data_json.pop('host_name')
    user_data_json.pop('host_site')
    user_data_json.pop('supervisor')

    user = User(**user_data_json)
    user.files = [ file_name ]
    user.cohort = cohort
    user.isValidated = False
    user.isUpdated = False


    print("㊙️ USER DATA:")
    print(user)

    result = user.save()
    print(f"MONGO DB Record ID: {result}")

    raw_data = RawData(**user_data_json)
    raw_data.user_id = result._id
    raw_data.save()

    # ##################################
    # # ㊙️ Upload to SharePoint
    # ##################################


    ##################################
    # ㊙️ Delete Files
    ##################################

