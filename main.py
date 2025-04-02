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
    

if __name__ == "__main__":
    access_token = open("token.txt", "r").read()
    payload = {
        "access_token": f"{access_token}",
        "id": "13080",
        "created_from": "2/4/2025",
        "created_to": "2/4/2025"
    }
    data = get_data(payload=payload)
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    full_values = []
    for idx, job in tqdm(enumerate(data["jobs"])):
        form = job["form_origin"]
        headers, values = [], []
        for item in form:
            # print(item)
            name = item['name']
            value = item['value']
            headers.append(name)
            values.append(value)
        full_values.append(values)
    df = pd.DataFrame(full_values, columns=headers)
    df.to_excel(f'outputs/full_output.xlsx', index=False)