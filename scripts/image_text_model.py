from gradio_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

## Upper Limit for retry is 10
## If any document fails for 10 times, then stop processing and move the file to the failed Document
def image_text_model(image_file_paths):
    # Replace 'Your_HuggingFace_Token' with your actual Hugging Face token
    hf_token = os.getenv('HFT')

    # Initialize the Gradio client with your Hugging Face token
    client = Client("https://nkosiyouth-ocr-image-to-text.hf.space/--replicas/sszfq/", hf_token=hf_token)

    results_list = []
    max_retries = 10

    index = 0  # Start from the beginning initially
    while index < len(image_file_paths):
        file_path = image_file_paths[index]
        retries = 0  # Reset retry counter for each file

        while retries < max_retries:
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
                break  # Exit the retry loop

            except Exception as e:
                retries += 1
                print(f"An error occurred while processing {file_path} (attempt {retries}): {e}")
                if retries >= max_retries:
                    raise Exception(f"Failed to process {file_path} after {max_retries} attempts. Stopping execution.")

                print("Resuming from the same file...")
                # Optional: Add a small delay before retrying
                # time.sleep(1)

    return results_list
