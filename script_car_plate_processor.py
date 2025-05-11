from datetime import datetime, timedelta

import ast
import json
import pandas as pd
import requests
import os


def print_variants(variants):
    for key, value in variants.items():
        print(f"{key}: {value}")

def calculate_time_difference(start_time_str, end_time_str):
    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.fromisoformat(end_time_str)
    time_difference = end_time - start_time
    return time_difference

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def car_plate_processor(path: str) -> pd.DataFrame:
    print("\n----------------------------------------")
    print(f"Processing car plate data...{path}")
    df_car_plate = pd.read_csv(path)
    df_car_plate["staytime"] = ""

    rows_to_remove = []
    for index, row in df_car_plate.iterrows():
        dict_part = row["variants"].split(", ", 1)[1][:-1]
        parsed_variants = ast.literal_eval(dict_part)

        if parsed_variants[row["car_plate"]] <= 3:
            rows_to_remove.append(index)
        else:
            time_difference = calculate_time_difference(row["start_time"], row["end_time"])
            df_car_plate.at[index, "staytime"] = format_timedelta(time_difference)

    print(f"count of row: {len(df_car_plate)}")
    print(f"count of row to remove: {len(rows_to_remove)}")

    df_car_plate.drop(rows_to_remove, inplace=True)
    df_car_plate = df_car_plate[["car_plate", "staytime", "start_time", "end_time", "img_path"]]

    return df_car_plate

if __name__ == "__main__":
    folder_path = "csv/car_plate"

    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = car_plate_processor(file_path)

        filename_without_ext = os.path.splitext(file)[0]
        date_part = filename_without_ext.split('_')[3].split('T')[0]

        new_filename = f"鳳山車牌_{date_part}.csv"
        new_file_path = os.path.join(folder_path, "output", new_filename)

        df.to_csv(new_file_path, index=False)

        column_order = ['car_plate', 'staytime', 'start_time']
        df = df[column_order]
        df.rename(columns={'start_time': 'datetime'}, inplace=True)
        df['location'] = 4
        json_payload = df.to_json(orient="records")
        print(json_payload)

        # Upload the JSON payload to the server
        url = "https://nexretail-camera-station-v2.de.r.appspot.com/data_storage/car_plate_data_upload/"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json_payload, headers=headers)

        if response.status_code == 201:
            print("\nData uploaded successfully.")
            print("Response message:", response.json().get("message", "No message in response"))
        else:
            print(f"\nFailed to upload data. Status code: {response.status_code}")
            print("Response message:", response.json().get("message", "No message in response"))
