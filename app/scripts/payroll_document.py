

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

def get_ocr_text_for_pay_roll(data, document_name):
    matching_ocr_texts = []  # List to hold all matching OCR text entries

    for entry in data:
        # Check if the entry is a list or tuple and has at least 3 elements (including image classification)
        if not (isinstance(entry, (list, tuple)) and len(entry) > 2):
            continue  # Skip entries that don't meet the criteria

        image_classification = entry[2]  # Assuming the 3rd element is image classification info

        # Check if image_classification is a dictionary and has the key 'document_name'
        if (isinstance(image_classification, dict) and
            image_classification.get('document_name') == document_name):
            # Append the OCR text to the list if it exists
            if isinstance(entry[1], str):
                matching_ocr_texts.append(entry[1])

    # Combine all OCR texts into a single string separated by newlines
    return '\n'.join(matching_ocr_texts) if matching_ocr_texts else None  # Return None if no matching documents are found

