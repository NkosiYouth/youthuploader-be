import requests
import json

API_URL = "https://flowise-zm2z.onrender.com/api/v1/prediction/ce5137d2-eb6e-497f-82d5-1ad3cfd7b3d4"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()


def get_user_output_data(merged_text):
    output = query({
    "question": merged_text,
    })
    return output