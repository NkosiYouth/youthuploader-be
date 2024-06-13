import json
from PyPDF2 import PdfReader, PdfWriter
import io
import os

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


def update_page_names_with_user(page_names, user_data_str):
    # Parse the JSON string into a dictionary
    user_data = json.loads(user_data_str)

    # Extract first name, last name, and RSA ID number from the user_data dictionary
    first_name = user_data.get('first_name', '').strip()  # Ensure the keys match those in your JSON
    last_name = user_data.get('last_name', '').strip()    # Ensure the keys match those in your JSON
    rsa_id_number = user_data.get('rsa_id_number', '').strip()  # Ensure the keys match those in your JSON

    # Update page_names with the user's information
    updated_page_names = [f"{name} - {first_name} {last_name} - {rsa_id_number}" for name in page_names]

    return updated_page_names


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

