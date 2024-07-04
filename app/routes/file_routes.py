from flask import request, jsonify, Blueprint
import os
from multiprocessing import Process, current_process
import boto3
from scripts import ai_model_script
from dotenv import load_dotenv
import time

load_dotenv()

file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    uploaded_files = request.files.getlist('file')
    uploaded_files_info = []

    cohort = request.form.get('cohort')
    if not cohort:
        return jsonify({'error': 'Cohort not provided'}), 400

    processes = []

    for uploaded_file in uploaded_files:
        filename = uploaded_file.filename
        file_path = os.path.join("uploads", filename)

        if not is_valid_pdf_extension(filename):
            return jsonify({'error': f'Invalid file extension for "{filename}"'}), 400

        try:
            uploaded_file.save(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {e}'}), 500

        print('㊗️ UPLOADING TO S3')
        upload_pdf_to_s3(file_path, filename)
        process = Process(target=ai_model_script.ai_model, args=(file_path, filename, cohort))
        processes.append(process)
        uploaded_files_info.append({'file_name': filename, 'file_path': file_path, 'cohort': cohort})

    for process in processes:
        process.start()

    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files_info}), 201

def is_valid_pdf_extension(filename):
    valid_extensions = ('.pdf', '.PDF')
    return filename.lower().endswith(valid_extensions)

def upload_pdf_to_s3(file_path, file_name):
    file_path = os.path.join("uploads", file_name)
    try:
        s3_client = boto3.client(
            service_name='s3',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
        )
        response = s3_client.upload_file(file_path, os.getenv('AWS_S3_BUCKET_NAME'), file_name)
        print(f'upload_log_to_aws response: {response}')
    except Exception as e:
        print(f"Error uploading file '{file_name}' to S3 bucket : {e}")
