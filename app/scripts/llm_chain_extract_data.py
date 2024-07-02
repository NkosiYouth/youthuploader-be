import requests

def query(payload, api_url):
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Assuming ee_ocr_text is obtained from get_ocr_text_for_document function
def get_race_and_gender(ee_ocr_text):
    race_and_gender = None
    if ee_ocr_text is not None:
        payload = {"question": ee_ocr_text}
        try:
            output = query(payload, "https://flowise-zm2z.onrender.com/api/v1/prediction/b4c504c2-24f0-423a-8884-dc88ea143607")
            race_and_gender = output.get('text', 'No result found')
        except Exception as e:
            print(f"An error occurred: {e}")
            race_and_gender = None
    return race_and_gender


# Assuming ee_ocr_text is obtained from get_ocr_text_for_document function

def get_pay_roll_data(payroll_ocr_text):
    payroll_data = None
    if payroll_ocr_text is not None:
        payload = {
            "question": payroll_ocr_text,
        }
        output = query(payload, "https://flowise-zm2z.onrender.com/api/v1/prediction/3b379972-f629-40c3-a70f-fc7899d3a0db")
        payroll_data = output['text']
        print(payroll_data)
    return payroll_data


def get_contract_data(ep_contract_ocr_text):
    contract_data = None
    if ep_contract_ocr_text is not None:
        payload = {
            "question": ep_contract_ocr_text,
        }
        output = query(payload,"https://flowise-zm2z.onrender.com/api/v1/prediction/a6fb0bf0-0612-4236-8fd6-a4bb5d2085ce")
        contract_data = output['text']
        print(contract_data)
    return contract_data

