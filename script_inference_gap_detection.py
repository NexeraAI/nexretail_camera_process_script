import pandas as pd
import json
import os

date = "2024-12-25"

inference_gap_list = []
base_directory = f"csv/{date}"
cam_list = ["cam002", "cam003", "cam004", "cam005", "cam006", "cam007"]
# cam_list = ["cam002", "cam003", "cam004", "cam005", "cam006"]

for hourly_folder in sorted(os.listdir(base_directory)):
    folder_path = os.path.join(base_directory, hourly_folder)

    if os.path.isdir(folder_path):
        hourly_cam_id_list = []
        for cam in cam_list:
            cam_txt_path = os.path.join(folder_path, cam + ".txt")

            try:
                with open(cam_txt_path, "r") as file:
                    df_cam_txt = pd.read_csv(cam_txt_path, sep='\s+')

                    first_row = df_cam_txt.iloc[0].to_dict() if not df_cam_txt.empty else None

                    hourly_cam_id_list.append(first_row['id'])

            except Exception as e:
                print(f"Error reading file {cam_txt_path}: {e}")
        
        if 1 in hourly_cam_id_list:
            inference_gap_list.append(hourly_folder)

print(inference_gap_list)
        