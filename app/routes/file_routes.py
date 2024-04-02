from flask import request, jsonify, Blueprint
import os

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

        # process = Process(target=manipulate_file, args=(filename, file_path, cohort))
        # processes.append(process)

    # Start and join each process sequentially
    for process in processes:
        process.start()
        process.join()

    # Collect information about uploaded files
    for uploaded_file in uploaded_files:
        filename = uploaded_file.filename
        file_path = os.path.join("app", "uploads", filename)
        uploaded_files_info.append({'file_name': filename, 'file_path': file_path, 'cohort': cohort})

    return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files_info}), 201

# Define other file-related routes as needed...

def is_valid_pdf_extension(filename):
    valid_extensions = ('.pdf', '.PDF')
    return filename.lower().endswith(valid_extensions)