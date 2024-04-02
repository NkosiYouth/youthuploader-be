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

def consolidate_data(image_file_paths, results_list, image_classification):
    # Zip the four lists together to create a list of tuples
    consolidated_data = list(zip(image_file_paths, results_list, image_classification))
    # Return the consolidated data
    return consolidated_data