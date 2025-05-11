import json
import pandas as pd
from datetime import datetime, timedelta
import requests

AGE_MAP = {
    0: "0-15",
    1: "16-30",
    2: "31-45",
    3: "46-60",
    4: "61-"
}

def summarize_action(actions: list) -> str:
    if "category" in actions:
        return "category"
    elif "document" in actions:
        return "document"
    else:
        return "other"

def calculate_table_head_count(combined_gender) -> int:
    if isinstance(combined_gender, list):
        return len(combined_gender)
    return 1
        
def process_camera_data(file_path: str) -> pd.DataFrame:
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Sort by 'solution' first and then by 'datetime'
    df = df.sort_values(by=['solution', 'datetime'])
    df['actions'] = df['actions'].apply(eval)  # Convert string representation of list to actual list
    
    # Drop rows with no value in gender column
    # df = df.dropna(subset=['gender'])

    # Remove rows with 'staytime' smaller than 500
    df = df[df['staytime'] >= 200]

    df['datetime'] = pd.to_datetime(df['datetime'])

    # Iterate through the DataFrame and remove rows based on the condition
    df["combined_gender"] = ""
    df["combined_age"] = ""
    df["table_head_count"] = ""
    # df["combined_track_id"] = ""

    # rows_to_remove = set()
    # for solution, group in df.groupby('solution'):
    #     for i in range(len(group) - 1):
    #         current_row = group.iloc[i]
    #         next_row = group.iloc[i + 1]
            
    #         staytime_seconds = int(current_row['staytime'])
    #         end_time = current_row['datetime'] + timedelta(seconds=staytime_seconds)
            
    #         if next_row['datetime'] <= end_time:
    #             rows_to_remove.add(next_row.name)

    #             if not current_row['combined_gender']:
    #                 df.at[current_row.name, 'combined_gender'] = [current_row['gender']]
    #                 df.at[current_row.name, 'combined_age'] = [current_row['age']]
    #             df.at[current_row.name, 'combined_gender'].append(next_row['gender'])
    #             df.at[current_row.name, 'combined_age'].append(next_row['age'])
    
    # df.drop(index=rows_to_remove, inplace=True)

    df = df.sort_values(by=['solution', 'datetime'])

    # df['age'] = df['age'].map(AGE_MAP)

    rows_to_remove = set()
    for solution, group in df.groupby('solution'):
        for i in range(len(group) - 1, 0, -1):
            current_row = group.iloc[i]
            prev_row = group.iloc[i - 1]
            
            staytime_seconds = int(prev_row['staytime'])
            end_time = prev_row['datetime'] + timedelta(seconds=staytime_seconds)
            
            if df.at[current_row.name, 'combined_gender'] == "":
                df.at[current_row.name, 'combined_gender'] = [current_row['gender']]
                df.at[current_row.name, 'combined_age'] = [str(current_row['age'])]
                # df.at[current_row.name, 'combined_track_id'] = [str(current_row['track_id'])]

            if current_row['datetime'] <= end_time:
                rows_to_remove.add(current_row.name)

                if df.at[prev_row.name, 'combined_gender'] == "":
                    df.at[prev_row.name, 'combined_gender'] = [prev_row['gender']]
                    df.at[prev_row.name, 'combined_age'] = [str(prev_row['age'])]
                    # df.at[prev_row.name, 'combined_track_id'] = [str(prev_row['track_id'])]
                
                df.at[prev_row.name, 'combined_gender'] = df.at[prev_row.name, 'combined_gender'] + df.at[current_row.name, 'combined_gender']
                df.at[prev_row.name, 'combined_age'] = df.at[prev_row.name, 'combined_age'] + df.at[current_row.name, 'combined_age']
                # df.at[prev_row.name, 'combined_track_id'] = df.at[prev_row.name, 'combined_track_id'] + df.at[current_row.name, 'combined_track_id']
                
                # df.at[prev_row.name, 'combined_gender'].append(current_row['gender'])
                # df.at[prev_row.name, 'combined_age'].append(current_row['age'])
    
    df.drop(index=rows_to_remove, inplace=True)

    # Filter rows based on minutes part of datetime is 00:00
    df = df.sort_values(by=['solution', 'datetime'])
    df["joint_staytime"] = ""
    df["joint_action"] = ""
    
    rows_to_remove = set()
    for solution, group in df.groupby('solution'):
        for i in range(len(group) - 1, 0, -1):
            current_row = group.iloc[i]
            prev_row = group.iloc[i - 1]

            if current_row['datetime'].minute == 0 and current_row['datetime'].second == 0 and i != 0:
                # df.at[prev_row.name, 'joint_action'] = prev_row.actions + current_row.actions
                # df.at[prev_row.name, 'joint_staytime'] = prev_row.staytime + current_row.staytime
                df.at[prev_row.name, 'actions'] = prev_row.actions + current_row.actions
                df.at[prev_row.name, 'staytime'] = prev_row.staytime + current_row.staytime
                rows_to_remove.add(current_row.name)
    
    df.drop(index=rows_to_remove, inplace=True)

    # Filter rows based on 'actions' column
    df["doc_catalog_count"] = ""
    df["action_summary"] = ""
    # df['actions'] = df['actions'].apply(eval)  # Convert string representation of list to actual list
    rows_to_remove = set()
    for i in range(len(df)):
        print(f"i: {i}")
        current_row = df.iloc[i]
        
        if not any(action in current_row['actions'] for action in ["document", "category", "catalog", "other"]):
            print(f"no action, removing row {current_row.name}")
            rows_to_remove.add(current_row.name)
        else:
            # Count the number of "document" and "catalog" actions
            doc_catalog_count = sum(action in ["document", "category", "catalog"] for action in current_row['actions'])
            # df.at[current_row.name, 'doc_catalog_count'] = doc_catalog_count
            if doc_catalog_count < 2:
                print(f"less than 2 actions, removing row {current_row.name}")
                rows_to_remove.add(current_row.name)   
    
    df.drop(index=rows_to_remove, inplace=True)

    df['action_summary'] = df['actions'].apply(summarize_action)
    df['table_head_count'] = df['combined_gender'].apply(calculate_table_head_count)

    column_order = ['track_id', 'table_head_count', 'combined_gender', 'gender', 'combined_age', 'age', 'solution', 'action_summary', 'actions', 'staytime', 'datetime', 'Camera', 'Shop']
    df = df[column_order]

    df = df.sort_values(by=['solution', 'datetime'])
    
    return df

if __name__ == "__main__":
    date = "2025-05-09"
    # location = "新莊"
    # location = "新竹"
    # location = "西台南"
    location = "鳳山"
    # location = "中台中"
    # location = "新店"
    
    folder_path = f"output/{location}/{date}"

    file_path = f"{folder_path}/{date}_combined_region_table.csv"
    processed_df = process_camera_data(file_path)
    
    # Print the processed DataFrame
    # print(processed_df)

    # processed_df.to_csv(f"{folder_path}/{date}_combined_region_table_filtered02_by_endtime_overlap.csv", index=False)
    # processed_df.to_csv(f"{folder_path}/{date}_combined_region_table_filtered03_by_action.csv", index=False)

    if location == "新莊":
        processed_df["location"] = 1

    elif location == "新竹":
        processed_df["location"] = 2
    
    elif location == "西台南":
        processed_df["location"] = 3

    elif location == "鳳山":
        processed_df["location"] = 4
    
    elif location == "中台中":
        processed_df["location"] = 5
    
    elif location == "新店":
        processed_df["location"] = 6

    processed_df['datetime'] = processed_df['datetime'].apply(lambda x: str(x))

    json_payload = processed_df.to_json(orient="records")
    print(json_payload)

    # Upload the JSON payload to the server
    url = "https://nexretail-camera-station-v2.de.r.appspot.com/data_storage/action_data_upload/"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_payload, headers=headers)

    if response.status_code == 201:
        print("\nData uploaded successfully.")
        print("Response message:", response.json().get("message", "No message in response"))
    else:
        print(f"\nFailed to upload data. Status code: {response.status_code}")
        print("Response message:", response.json().get("message", "No message in response"))

    print("")
    print("rows: ", len(processed_df))
    print(f"--------------------End Json Payload { date } --------------------")
    processed_df.to_csv(f"{folder_path}/{date}_combined_region_table_filtered.csv", index=False)