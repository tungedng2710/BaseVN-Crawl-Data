import requests
import pandas as pd
import os
import json
from tqdm import tqdm
import numpy as np

def get_data(url: str = "https://workflow.base.vn/extapi/v1/workflow/jobs", 
             payload: dict = {}):
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    print("Status code:", response.status_code)
    try:
        return response.json()
    except ValueError:
        return {}

def save_dict_to_json(data_dict, filename):
  """Saves a dictionary to a JSON file.

  Args:
    data_dict: The dictionary to be saved.
    filename: The name of the JSON file to create (e.g., "data.json").
  """
  try:
    with open(filename, 'w', encoding='utf-8') as f:
      json.dump(data_dict, f, ensure_ascii=False, indent=4)
    print(f"Successfully saved data to {filename}")
  except Exception as e:
    print(f"An error occurred while saving to {filename}: {e}")


if __name__ == "__main__":
    access_token = open("token.txt", "r").read()

    payload = {
        "access_token": f"{access_token}",
        "id": "13080",
        "created_from": "3/4/2025",
        "created_to": "9/4/2025"
    }

    # --------------------------------------------------------- #
    data = get_data(payload=payload)
    # full_values = []
    max_length_headers = []
    full_data = []
    save_dict_to_json(data, "outputs/data.json")
    for job in tqdm(data["jobs"]):
        form = job["form"]
        headers, values = [], []
        form_dict = {}
        for item in form:
            # print(item)
            name = item['name']
            value = item['value']
            form_dict[name] = value
            headers.append(name)
        if len(headers) > len(max_length_headers):
            max_length_headers = headers.copy()

        full_data.append(form_dict)
        # full_values.append(values)
    
    all_keys = set()
    for sample in full_data:
        all_keys.update(sample.keys())

    # Create dataframe and save to file
    df = pd.DataFrame(full_data, columns=max_length_headers)
    df.fillna('', inplace=True)
    df.to_excel(f'outputs/full_output.xlsx', index=False)