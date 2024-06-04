from gradio_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

def image_text_model(image_file_paths):

    # Replace 'Your_HuggingFace_Token' with your actual Hugging Face token
    hf_token = os.getenv('HFT')

    # Initialize the Gradio client with your Hugging Face token
    client = Client("https://nkosiyouth-updated-ocr-image-to-text-2-0.hf.space/--replicas/fluc7/", hf_token=hf_token)

    results_list = []

for file_path in image_file_paths:
    result = client.predict(
        "PaddleOCR",
        file_path,
        api_name="/predict"
    )

    # Append the OCR result directly to the results_list if 'result' is already a text string
    results_list.append(result)

    # Print the OCR result
    print(f"OCR Result for {file_path}:")
    print(result)
    print("---")  # Separator for readability

# The results_list now contains the OCR text results from each image, each as a separate element