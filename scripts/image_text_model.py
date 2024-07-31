from gradio_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

def image_text_model(image_file_paths):

    # Replace 'Your_HuggingFace_Token' with your actual Hugging Face token
    hf_token = os.getenv('HFT')

    # Initialize the Gradio client with your Hugging Face token
    client = Client("NkosiYouth/Updated-OCR-image-to-text-2.0/", hf_token=hf_token)

    results_list = []

    root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


    index = 0  # Start from the beginning initially
    while index < len(image_file_paths):
        file_path = os.path.join(root_folder,image_file_paths[index])

        print("########################################## FILE PATH")
        print(file_path)
        try:
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

            index += 1  # Move to the next file

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")
            print("Resuming from the same file...")
            # If an error occurred, continue with the same file in the next iteration
            # No need to increment index, it will be the same in the next iteration

    return results_list
