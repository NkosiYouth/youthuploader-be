

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


API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/b74b5c85-c7ae-414f-801b-35a65d290b46"

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
        image_file_path, ocr_results, image_classification = data

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
