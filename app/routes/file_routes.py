from flask import request, jsonify, Blueprint
import os
from multiprocessing import Process
import boto3
from scripts import ai_model_script

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

        process = Process(target=ai_model_script.ai_model, args=(filename, file_path, cohort))
        processes.append(process)

    # # Start and join each process sequentially
    for process in processes:
        process.start()
        process.join()

    # Collect information about uploaded files
    for uploaded_file in uploaded_files:
        filename = uploaded_file.filename
        file_path = os.path.join("uploads", filename)
        print('㊗️ UPLOADING TO S3')
        print(file_path)
        print(filename)
        upload_pdf_to_s3(file_path, filename)
        uploaded_files_info.append({'file_name': filename, 'file_path': file_path, 'cohort': cohort})

    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files_info}), 201

# Define other file-related routes as needed...

def is_valid_pdf_extension(filename):
    valid_extensions = ('.pdf', '.PDF')
    return filename.lower().endswith(valid_extensions)


def upload_pdf_to_s3(file_path, file_name):
    AWS_S3_BUCKET_NAME = 'youthatwork'
    AWS_REGION = 'eu-north-1'
    AWS_ACCESS_KEY = 'AKIA6ODU3VKKXED23UPW'
    AWS_SECRET_KEY = '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'
    file_path = os.path.join("uploads", file_name)

    try:
        s3_client = boto3.client(
            service_name='s3',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        response = s3_client.upload_file(file_path, AWS_S3_BUCKET_NAME, file_name)
        print(f'upload_log_to_aws response: {response}')
    except Exception as e:
        print(f"Error uploading file '{file_name}' to S3 bucket : {e}")