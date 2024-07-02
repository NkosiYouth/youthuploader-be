#For PDF
from PyPDF2 import PdfReader, PdfWriter
#For Image
import base64
from pdf2image import convert_from_bytes
#image storage
#OCR image-to-text
from gradio_client import Client
#Document Identification Chain Flowise
import requests
#Hand writing identification model
import json
#create PDF

def ai_model(file_path, file_name, cohort):

    """# File Upload"""
    storage_path = f'content/{file_name}'

    # Construct the absolute path to the PDF file
    pdf_path = file_path

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    import io
    # Create BytesIO object from the PDF bytes
    pdf_data = io.BytesIO(pdf_bytes)

    """# PDF To Image with PyMuPDF
    works well on windows
    """

    import fitz  # PyMuPDF
    import os

    def convert_pdf_to_images(pdf_path):
        # Open the PDF file using PyMuPDF
        pdf = fitz.open(pdf_path)
        images = []

        # Iterate over each page in the PDF
        for page_num in range(len(pdf)):
            # Get the page
            page = pdf[page_num]

            # Render page to an image (pix) object
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            images.append(img_data)

        pdf.close()
        return images

    from PIL import Image
    import io

    def save_images_to_files(images, directory="/content/data"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_paths = []
        for i, img_data in enumerate(images):
            file_path = f"{directory}/page_{i}.png"
            # Since image data is in bytes, it can be directly written to a file in 'wb' mode
            with open(file_path, 'wb') as f:
                f.write(img_data)
            file_paths.append(file_path)
        return file_paths

    # Replace 'path_to_your_pdf_file.pdf' with the actual path to the PDF file
    pdf_path = f"/content/{file_name}"

    # Step 2: Convert each PDF page to an image
    images = convert_pdf_to_images(pdf_path)  # Updated function call

    # Step 3: Save each image to a file and get the file paths
    image_file_paths = save_images_to_files(images)  # Updated function call

    # Output the results
    print(image_file_paths)

    """# PDF To Image Poppler
    In this step we split each page of the PDF up and then we convert each page of the PDF into an image and get the image URL
    """

    # Split PDF into page streams function:

    def split_pdf_into_pages_stream(pdf_data):
        reader = PdfReader(pdf_data)
        pages_streams = []

        for page in reader.pages:
            writer = PdfWriter()
            writer.add_page(page)
            page_stream = io.BytesIO()
            writer.write(page_stream)
            page_stream.seek(0)  # Rewind the stream to the beginning
            pages_streams.append(page_stream)

        return pages_streams

    # Convert PDF stream to images function:

    def convert_pdf_stream_to_images(pdf_streams):
        images = []
        for pdf_stream in pdf_streams:
            temp_images = convert_from_bytes(pdf_stream.getvalue())
            images.extend(temp_images)
        return images

    # Save images to files function:

    def save_images_to_files(images):
        file_paths = []
        directory = "/content/data"  # Change the path as needed

        if not os.path.exists(directory):
            os.makedirs(directory)

        for i, image in enumerate(images):
            file_path = f"{directory}/page_{i}.png"  # Saves in the /content/data directory
            image.save(file_path, "PNG")
            file_paths.append(file_path)

        return file_paths

    # Execution of the functions:

    # Step 1: Split the PDF into page streams
    page_streams = split_pdf_into_pages_stream(pdf_data)

    # Step 2: Convert each page stream into an image
    images = convert_pdf_stream_to_images(page_streams)

    # Step 3: Save each image to a file and get the file paths
    image_file_paths = save_images_to_files(images)

    # Output the results
    print(image_file_paths)

    """# Image Text Model
    In this step we convert all images to text with the huggingFace model: https://huggingface.co/spaces/pragnakalp/OCR-image-to-text
    """

    # Replace 'Your_HuggingFace_Token' with your actual Hugging Face token
    hf_token = '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'

    # Initialize the Gradio client with your Hugging Face token
    client = Client("https://nkosiyouth-ocr-image-to-text.hf.space/--replicas/sszfq/", hf_token=hf_token)

    results_list = []

    for file_path in image_file_paths:
        result = client.predict(
            "PaddleOCR",
            file_path,
            api_name="/predict"
        )

        # Append the OCR result directly to the results_list if 'result' is already a text string
        results_list.append(result)

        # Print the OCR result
        print(f"OCR Result for {file_path}:")
        print(result)
        print("---")  # Separator for readability

    # The results_list now contains the OCR text results from each image, each as a separate element

    """# Identify Document & type"""

    API_URL = "https://flowiseai-p6lo.onrender.com/api/v1/prediction/76c568d8-cf58-403d-819e-5c80d8213cd4"

    def query(payload):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # This will raise an error for HTTP error codes
            return response.json()  # Try to decode JSON
        except requests.HTTPError as http_err:
            # If an HTTP error occurs, print the HTTP status code
            print(f"HTTP error occurred: {http_err}")
            print(response.text)  # This will print the raw response text, which might contain clues
        except requests.RequestException as err:
            # If a different request error occurs, print it
            print(f"Request error occurred: {err}")
        except ValueError as json_err:
            # If the response isn't valid JSON, print the error and the content anyway
            print(f"JSON decode error: {json_err}")
            print("Here's the response content anyway:", response.content)
        return None  # If we get here, something went wrong

    image_classification = []

    for ocr_result in results_list:
        formatted_text = ocr_result.strip()
        response = query({"question": formatted_text})

        if response is not None:
            print(response)
            # Construct a dictionary with only the 'document_name' and 'isDigital' keys
            classification_item = {
                'document_name': response['json']['document_name'],
                'isDigital': response['json']['isDigital']
            }
            # Append the dictionary to the list
            image_classification.append(classification_item)
        else:
            print("No valid response received.")
            # Optionally append a placeholder if no valid response
            # image_classification.append({'document_name': None, 'isDigital': None})

    # Now image_classification is a list containing dictionaries with only 'document_name' and 'isDigital'
    print(image_classification)

    """# Consolidate Data
    From page_streams, image_file_paths, results_list, and image_classification lists into a single data structure


    """

    def consolidate_data(page_streams, images, image_file_paths, results_list, image_classification):
        # Zip the four lists together to create a list of tuples
        consolidated_data = list(zip(page_streams, images, image_file_paths, results_list, image_classification))

        # Return the consolidated data
        return consolidated_data

    # Usage:
    # Assuming that page_streams, image_file_paths, results_list, and image_classification are already defined and populated
    consolidated_data = consolidate_data(page_streams, images, image_file_paths, results_list, image_classification)

    # Now consolidated_data is a list where each item is a tuple containing
    # corresponding elements from each of the four input lists.

    print(consolidated_data)

    """# Verify Non-Digital Documents

    This should only verify the first 3 pages of non-digital documents not the entire document
    """

    API_URL = "https://flowiseai-p6lo.onrender.com/api/v1/prediction/de9807e2-2fd7-47f6-ae67-c773b2694680"

    def encode_image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def query(ocr_result, image_path):
        image_base64 = encode_image_to_base64(image_path)
        payload = {
            "question": ocr_result,
            "uploads": [
                {
                    "data": f'data:image/png;base64,{image_base64}',  # base64 string
                    "type": 'file',
                    "name": 'Flowise.png',
                    "mime": 'image/png'
                }
            ]
        }
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            return response.json()  # Try to decode JSON
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.RequestException as err:
            print(f"Request error occurred: {err}")
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")
            print("Here's the response content anyway:", response.content)
        return None

    def process_non_digital_responses(consolidated_data):
        non_digital_responses = []

        for data in consolidated_data:
            page_stream, image, image_file_path, ocr_results, image_classification = data

            # Check if the image is not digital and thus needs processing
            if not image_classification.get('isDigital', True):
                # Process the OCR text and the image path
                response = query(ocr_results, image_file_path)  # 'query' should be a defined function

                # If a response is received, add it to the list with its file path
                if response is not None:
                    non_digital_responses.append({
                        'text': response.get('text'),  # assuming 'text' is the key for the OCR text
                        'image_file_path': image_file_path  # include the image file path
                    })

        return non_digital_responses

    # Then, you would call this function as before and pass its output to `update_ocr_responses`:
    consolidated_data
    processed_responses = process_non_digital_responses(consolidated_data)
    print(processed_responses)

    """# Update image texts from non-digital documents"""

    def update_ocr_responses(consolidated_data, processed_responses):
        if not processed_responses:
            return consolidated_data

        # Ensure that processed_responses is a list of dictionaries
        if not isinstance(processed_responses, list) or not all(isinstance(response, dict) for response in processed_responses):
            raise ValueError("processed_responses must be a list of dictionaries")

        # Create a dictionary to map image file paths to processed responses
        response_dict = {response['image_file_path']: response for response in processed_responses if 'image_file_path' in response}

        updated_consolidated_data = []
        for data in consolidated_data:
            # Extract relevant data from the tuple
            page_stream, image, image_file_path, ocr_results, image_classification = data

            # Check if the image_classification indicates the document is not digital
            is_digital = False
            if isinstance(image_classification, str):
                try:
                    image_classification = json.loads(image_classification)
                    is_digital = image_classification.get('isDigital', False)
                except json.JSONDecodeError:
                    print(f"Invalid JSON in image_classification: {image_classification}")
                    continue  # Skip this iteration because of invalid JSON
            elif isinstance(image_classification, dict):
                is_digital = image_classification.get('isDigital', False)

            # If there's a processed response and the document is not digital, update the OCR text
            if not is_digital and image_file_path in response_dict:
                updated_response = response_dict[image_file_path]
                updated_text = updated_response.get('text', ocr_results)
                updated_data_tuple = (page_stream, image, image_file_path, updated_text, image_classification)
            else:
                updated_data_tuple = data

            updated_consolidated_data.append(updated_data_tuple)

        return updated_consolidated_data

    # Usage of the function goes here
    # Assuming consolidated_data and processed_responses are already defined and populated
    updated_data = update_ocr_responses(consolidated_data, processed_responses)
    print(updated_data)

    """# Combine all ORC results into a string from transcription Files

    Consolidate OCR results into a single string based on digitization status.
        Prioritizes documents where isDigital is true.
        If no such documents are found, it uses those where isDigital is false.
        For documents where isDigital is false, only the first 3 instance of a document_name is used.

        Parameters:
        - data: A list of tuples, where each tuple contains image_classification info and OCR result.

        Returns:
        A single string that is a concatenation of all OCR results based on the conditions.
    """

    def consolidate_ocr_results_based_on_digitization(data):
        digital_ocr_texts = []
        non_digital_documents_seen = {}
        non_digital_ocr_texts = []

        for entry in data:
            # Check if the entry is a list or tuple and has at least 4 elements
            if not (isinstance(entry, (list, tuple)) and len(entry) > 3):
                print(f"Invalid entry format: {entry}")
                continue  # Skip this entry

            # Check if the OCR text entry is a string, if not set to an empty string
            ocr_text = entry[3] if isinstance(entry[3], str) else ""
            image_classification = entry[4]  # Assuming the 5th element is image classification info

            is_digital = image_classification.get('isDigital')  # Assuming image_classification is a dictionary
            document_name = image_classification.get('document_name')

            if is_digital:
                digital_ocr_texts.append(ocr_text)
            else:
                document_count = non_digital_documents_seen.get(document_name, 0)
                if document_count < 3:
                    non_digital_documents_seen[document_name] = document_count + 1
                    non_digital_ocr_texts.append(ocr_text)

        if digital_ocr_texts:
            consolidated_text = ' '.join(digital_ocr_texts)
        else:
            consolidated_text = ' '.join(non_digital_ocr_texts)

        return consolidated_text

    updated_data

    consolidated_text = consolidate_ocr_results_based_on_digitization(updated_data)
    print(consolidated_text)

    """In this step we want to explicitly look into the EEA1 document as it is the only place where we get race and disability?"""

    def get_ocr_text_for_document(data, document_name):
        for entry in data:
            # Check if the entry is a list or tuple and has at least 5 elements (including image classification)
            if not (isinstance(entry, (list, tuple)) and len(entry) > 4):
                continue  # Skip entries that don't meet the criteria

            image_classification = entry[4]  # Assuming the 5th element is image classification info
            # Check if image_classification is a dictionary and has the key 'document_name'
            if isinstance(image_classification, dict) and image_classification.get('document_name') == document_name:
                # Return the OCR text if it exists
                return entry[3] if isinstance(entry[3], str) else None
        return None  # Return None if no matching document name is found or if OCR text does not exist

    # Example usage:
    # Assuming updated_data is a list of entries where each entry is a list or tuple as expected
    document_name_to_search = "EEA1"
    ee_ocr_text = get_ocr_text_for_document(updated_data, document_name_to_search)
    print(ee_ocr_text)

    API_URL = "https://flowiseai-p6lo.onrender.com/api/v1/prediction/f4797834-673e-4769-9ff1-38d199abe21e"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    # Assuming ee_ocr_text is obtained from get_ocr_text_for_document function
    if ee_ocr_text is not None:
        payload = {
            "question": ee_ocr_text,
        }
        output = query(payload)
        race_and_gender = output
        print(race_and_gender)
    else:
        race_and_gender = None

    def dict_to_text(dictionary):
        if dictionary is None:
            return 'None'  # Return the string 'None'
        else:
            return ', '.join([f"{key}: {value}" for key, value in dictionary.items()])

    # Assuming the variable race_and_gender might be defined elsewhere
    try:
        race_and_gender_text = dict_to_text(race_and_gender)
    except NameError:
        race_and_gender_text = 'None'  # Set to 'None' if race_and_gender is not defined

    print(race_and_gender_text)

    """Update this function to either merge consolidated_Text but if race_gender is not defined then upadate consolidated text so that the ouput is always merged_text"""

    def dict_to_text(dictionary):
        if dictionary is None:
            return "Race: N/A, Gender: N/A"
        else:
            return ', '.join([f"{key}: {value}" for key, value in dictionary.items()])

    def merge_texts(consolidated_text, race_and_gender_dict):
        # First, convert the dictionary to a string
        race_and_gender_text = dict_to_text(race_and_gender_dict)

        # Now, check if consolidated_text is None and handle it appropriately
        if consolidated_text is None:
            consolidated_text = "Consolidated Text: N/A"

        # Now, concatenate the two strings.
        merged_text = consolidated_text + " " + race_and_gender_text
        return merged_text

    merged_text = merge_texts(consolidated_text, race_and_gender)
    print(merged_text)

    """# Get User Data"""

    API_URL = "https://flowiseai-p6lo.onrender.com/api/v1/prediction/2ec3a1ce-912d-4bc2-9494-655b86ecd8dd"

    def query(payload):
        response = requests.post(API_URL, json=payload)
        return response.json()

    output = query({
        "question": merged_text,
    })
    print(output)

    def extract_user_data(output):
        # Extract the 'text' field which contains the JSON string
        json_str = output['text']

        # Remove newline and backslash characters
        json_str_clean = json_str.replace('\\n', '').replace('\\', '')

        # Convert the string back to a JSON object
        json_obj = json.loads(json_str_clean)

        return json_obj

    user_data = extract_user_data(output)
    print(json.dumps(user_data, indent=2))

    # def extract_clean_json(output):
    #     # Extract the 'text' field which contains the JSON string
    #     json_str = output['text']

    #     # Remove newline and backslash characters
    #     json_str_clean = json_str.replace('\\n', '').replace('\\\\', '\\')

    #     # Convert the string back to a JSON object
    #     json_obj = json.loads(json_str_clean)

    #     # Convert the JSON object to a text string
    #     text_string = "\n".join(f"{key}: {value}" for key, value in json_obj.items())

    #     return text_string

    # # Assuming 'output' contains the JSON-like data structure, such as:
    # # output = {'text': '{"Title": "Miss", "First Name": "Lisbeth", ...}'}
    # clean_text = extract_clean_json(output)

    # # Print the text string
    # print(clean_text)

    """# Refine User Data
    Change this function so that it validates that at least the ID number first and last name is present.
    """

    # def validate_user_data_and_query_api(user_data):
    #     # Check if all fields in user_data are full
    #     if all(value.strip() for value in user_data.values()):
    #         # All fields are full, proceed with the API call
    #         API_URL = "https://flowiseai-p6lo.onrender.com/api/v1/prediction/93a43d9a-edd0-4829-a4b5-ab9cb6d2aea8"
    #         response = requests.post(API_URL, json={"question": clean_text})
    #         return response.json() if response.status_code == 200 else None
    #     else:
    #         # At least one field is empty, skip the API call
    #         print("Not all user data found. Do not add to Excel")
    #         return None  # Or appropriate action

    # # The API will only be queried if all fields in user_data are full
    # formatted_user_data = validate_user_data_and_query_api(user_data)
    # if result:
    #     print(formatted_user_data)

    """# Compile PDF/s
    Rename and make availbale to Download
    """

    def extract_page_names(consolidated_data):
        page_names = []
        for data in consolidated_data:
            page_stream, image, image_file_path, ocr_results, image_classification = data

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
        # No need to parse user_data with json.loads() since it's already a dictionary
        first_name = user_data.get('First Name', '').strip('",')  # Remove extra characters
        last_name = user_data.get('Last Name', '').strip('",')    # Remove extra characters

        # Update page_names with the user's first and last name
        updated_page_names = [f"{name} - {first_name} {last_name}" for name in page_names]

        return updated_page_names

    # Now call the function to get updated page names
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

    # Assuming 'uploaded' is the dictionary returned from files.upload() and contains your PDF data
    page_files = split_pdf_into_pages(pdf_data)

    # Finally, call the function to merge the pages by name and save them to PDF files
    created_file_names = merge_pages_by_name(updated_page_names, page_files)
    print("Created PDFs:", created_file_names)

    """# Check Documents created"""

    # !ls /content

    """# Upload user_data to Excel Sheet"""



    """# save file to SharePoint"""

