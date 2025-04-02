import requests
import pandas as pd
import os
import json
from tqdm import tqdm

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
    }
    data = get_data(payload=payload)
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    for idx, job in tqdm(enumerate(data["jobs"])):
        form = job["form"]
        form = data["jobs"][0]['form']
        ids, names, values = [], [], []
        for item in form:
            # print(item)
            id = item['id'] 
            name = item['name']
            value = item['value']
            ids.append(id)
            names.append(name)
            values.append(value)
        df = pd.DataFrame({'id': ids, 'name': names, 'value': values})
        df.to_excel(f'outputs/output{idx}.xlsx', index=False)