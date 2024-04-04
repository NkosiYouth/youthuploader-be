from scripts import ai_model_script, delete_folder
import os

# file_name = 'A1 9904060525080 copy.pdf'
file_name = 'a1-short'

cohort = 'data'

pdf_path = os.path.join(os.path.dirname(__file__), 'uploads', file_name)

ai_model_script.ai_model(pdf_path, file_name, cohort)