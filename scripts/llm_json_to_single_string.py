import json

def json_to_text(llm_document_to_text):
    if llm_document_to_text is None:
        return 'None'
    # Assuming json_data is a string representation of a JSON object.
    try:
        # Convert string to a dictionary
        data_dict = json.loads(llm_document_to_text)
        # Join the key-value pairs into a string
        return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
    except (json.JSONDecodeError, TypeError):
        return 'Invalid JSON or input type'

def merge_texts(consolidated_text, race_and_gender_text, payroll_data_text, contract_data_text):
    # Initialize a list to hold all text parts
    texts = []

    # Check each text and add it to the list if it exists, otherwise add "N/A"
    texts.append(consolidated_text if consolidated_text is not None else "Consolidated Text: N/A")
    texts.append(race_and_gender_text if race_and_gender_text is not None else "Race and Gender Text: N/A")
    texts.append(payroll_data_text if payroll_data_text is not None else "Payroll Data Text: N/A")
    texts.append(contract_data_text if contract_data_text is not None else "Contract Data Text: N/A")

    # Now, concatenate all parts with a space in between
    merged_text = ' '.join(texts)
    return merged_text