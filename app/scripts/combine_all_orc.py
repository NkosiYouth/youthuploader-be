

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

def consolidate_ocr_results_based_on_digitization(data):
    digital_ocr_texts = []
    non_digital_documents_seen = {}
    non_digital_ocr_texts = []

    for entry in data:
        # Check if the entry is a list or tuple and has at least 4 elements
        if not (isinstance(entry, (list, tuple)) and len(entry) > 1):
            print(f"Invalid entry format: {entry}")
            continue  # Skip this entry

        # Check if the OCR text entry is a string, if not set to an empty string
        ocr_text = entry[1] if isinstance(entry[1], str) else ""
        image_classification = entry[2]  # Assuming the 5th element is image classification info

        is_digital = image_classification.get('isDigital')  # Assuming image_classification is a dictionary
        document_name = image_classification.get('document_name')

        if is_digital:
            digital_ocr_texts.append(ocr_text)
        else:
            document_count = non_digital_documents_seen.get(document_name, 0)
            if document_count < 1:
                non_digital_documents_seen[document_name] = document_count + 1
                non_digital_ocr_texts.append(ocr_text)

    if digital_ocr_texts:
        consolidated_text = ' '.join(digital_ocr_texts)
    else:
        consolidated_text = ' '.join(non_digital_ocr_texts)

    return consolidated_text

def get_ocr_text_for_document(data, document_name):
    ocr_texts = []

    for entry in data:
        if not (isinstance(entry, (list, tuple)) and len(entry) >= 3):
            continue

        image_classification = entry[2]
        if isinstance(image_classification, dict) and image_classification.get('document_name') == document_name:
            ocr_text = entry[1] if isinstance(entry[1], str) else ""
            ocr_texts.append(ocr_text)

    return " ".join(ocr_texts)  # Consolidate all OCR texts for the given document_name