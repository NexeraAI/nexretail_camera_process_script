import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import requests

from PIL import Image
from scipy.ndimage import gaussian_filter

AGE_MAP = {
    0: "0-15",
    1: "16-30",
    2: "31-45",
    3: "46-60",
    4: "61-"
}
GENDER_MAP = {
    0: "Male",
    1: "Female"
}

if __name__ == "__main__":
    date_start = "2025-05-09"
    date_end = date_start
    
    # location = "新莊"
    # location = "新竹"
    # location = "西台南"
    location = "鳳山"
    # location = "中台中"
    # location = "新店"

    dates_processing = []
    dates_processed = []
    dates_error = {}

    dates_processing = pd.date_range(start=date_start, end=date_end).strftime("%Y-%m-%d").tolist()
    print(f"dates_processing: {dates_processing}")

    for date in dates_processing:
        folder_path = f"output/{location}/{date}"
        file_path = f"{folder_path}/{date}_combined_region_car.csv"

        if os.path.exists(file_path):
            dates_processed.append(date)

            df = pd.read_csv(file_path)

            df['datetime'] = df['datetime'].apply(lambda x: str(x))
            if location == "新莊":
                df["location"] = 1

            elif location == "新竹":
                df["location"] = 2
            
            elif location == "西台南":
                df["location"] = 3
            
            elif location == "鳳山":
                df["location"] = 4
            
            elif location == "中台中":
                df["location"] = 5
            
            elif location == "新店":
                df["location"] = 6

            json_payload = df.to_json(orient="records")
            print("------------------------------------")
            print(f"region car for {date}")
            print(f"size: {df.shape[0]}")
            
            print("uploading data...")
            url = "https://nexretail-camera-station-v2.de.r.appspot.com/data_storage/region_data_upload/"
            # url = "http://localhost:8000/data_storage/region_data_upload/"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json_payload, headers=headers)

            if response.status_code == 201:
                print("Data uploaded successfully.")
                print("Response message:", response.json().get("message", "No message in response"))
            else:
                print(f"Failed to upload data. Status code: {response.status_code}")
                print("Response message:", response.json().get("message", "No message in response"))

            print("\n")
        
        else:
            dates_error[date] = "File not found"
    
    print(f"dates_processed: {dates_processed}")
    print("dates_error:")
    for date, error in dates_error.items():
        print(f"{date}: {error}")
