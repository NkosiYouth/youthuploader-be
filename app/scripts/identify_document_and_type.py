from openai import OpenAI
#For PDF
from PyPDF2 import PdfReader, PdfWriter
import io
#For Image
import base64
from io import BytesIO
from pdf2image import convert_from_bytes
#image storage
import os
#OCR image-to-text
from gradio_client import Client
#Document Identification Chain Flowise
import requests
#Hand writing identification model
import json
#create PDF
from fpdf import FPDF

import fitz  # PyMuPDF
import os
from PIL import Image
import io

API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/b33c7596-4cf7-4d43-b116-8388f361a326"

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

def identify_document_and_type(results_list):
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
    return image_classification