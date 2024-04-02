

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

def get_ocr_text_for_eaa1_document(data, document_name):
    for entry in data:
        # Check if the entry is a list or tuple and has at least 3 elements (including image classification)
        if not (isinstance(entry, (list, tuple)) and len(entry) > 2):
            continue  # Skip entries that don't meet the criteria

        image_classification = entry[2]  # Assuming the 3rdth element is image classification info
        # Check if image_classification is a dictionary and has the key 'document_name'
        if isinstance(image_classification, dict) and image_classification.get('document_name') == document_name:
            # Return the OCR text if it exists
            return entry[1] if isinstance(entry[1], str) else None
    return None  # Return None if no matching document name is found or if OCR text does not exist

def json_to_text(race_and_geneder):
    if race_and_gender is None:
        return 'None'
    # Assuming json_data is a string representation of a JSON object.
    try:
        # Convert string to a dictionary
        data_dict = json.loads(race_and_gender)
        # Join the key-value pairs into a string
        return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
    except (json.JSONDecodeError, TypeError):
        return 'Invalid JSON or input type'

