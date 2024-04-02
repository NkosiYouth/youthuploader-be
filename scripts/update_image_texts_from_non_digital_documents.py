def update_ocr_responses(consolidated_data, processed_responses):
    if not processed_responses:
        return consolidated_data

    # Ensure that processed_responses is a list of dictionaries
    if not isinstance(processed_responses, list) or not all(isinstance(response, dict) for response in processed_responses):
        raise ValueError("processed_responses must be a list of dictionaries")

    # Create a dictionary to map image file paths to processed responses
    response_dict = {response['image_file_path']: response for response in processed_responses if 'image_file_path' in response}

    updated_consolidated_data = []
    for data in consolidated_data:
        # Extract relevant data from the tuple
        image_file_path, ocr_results, image_classification = data

        # Check if the image_classification indicates the document is not digital
        is_digital = False
        if isinstance(image_classification, str):
            try:
                image_classification = json.loads(image_classification)
                is_digital = image_classification.get('isDigital', False)
            except json.JSONDecodeError:
                print(f"Invalid JSON in image_classification: {image_classification}")
                continue  # Skip this iteration because of invalid JSON
        elif isinstance(image_classification, dict):
            is_digital = image_classification.get('isDigital', False)

        # If there's a processed response and the document is not digital, update the OCR text
        if not is_digital and image_file_path in response_dict:
            updated_response = response_dict[image_file_path]
            updated_text = updated_response.get('text', ocr_results)
            updated_data_tuple = (image_file_path, updated_text, image_classification)
        else:
            updated_data_tuple = data

        updated_consolidated_data.append(updated_data_tuple)

    return updated_consolidated_data

