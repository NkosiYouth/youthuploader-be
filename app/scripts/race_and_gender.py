import json

def race_and_gender_json_to_text(race_and_gender):
    if race_and_gender is None:
        return 'None'
    # Assuming json_data is a string representation of a JSON object.
    try:
        # Convert string to a dictionary
        data_dict = json.loads(race_and_gender)
        # Join the key-value pairs into a string
        return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
    except (json.JSONDecodeError, TypeError):
        return 'Invalid JSON or input type'


def payroll_json_to_text(payroll_data):
    if payroll_data is None:
        return 'None'
    # Assuming json_data is a string representation of a JSON object.
    try:
        # Convert string to a dictionary
        data_dict = json.loads(payroll_data)
        # Join the key-value pairs into a string
        return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
    except (json.JSONDecodeError, TypeError):
        return 'Invalid JSON or input type'

def contract_data_json_to_text(contract_data, payroll_data):
            if contract_data is None:
                return 'None'
            # Assuming json_data is a string representation of a JSON object.
            try:
                # Convert string to a dictionary
                data_dict = json.loads(payroll_data)
                # Join the key-value pairs into a string
                return ', '.join(f"{key}: {value}" for key, value in data_dict.items())
            except (json.JSONDecodeError, TypeError):
                return 'Invalid JSON or input type'