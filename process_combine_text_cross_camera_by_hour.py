import pandas as pd
import os

base_time_stamp = "2024-11-01T09_00_00"

CAMERA = ["cam002", "cam003", "cam004", "cam005", "cam006"]

SOLUTION = {
    1: "entrance_shop",
    2: "Negotiation_table_1",
    3: "Negotiation_table_2",
    4: "YARIS_CROSS",
    5: "bZ4x",
    6: "Negotiation_table_None",
    7: "RAV4",
    8: "Negotiation_table_4",
    9: "Negotiation_table_5",
    10: "Negotiation_table_6",
    11: "VIOS",
    12: "car_None",
    13: "COROLLA_SPORT",
    14: "Negotiation_table_7",
    15: "Negotiation_table_8",
    16: "Negotiation_table_9",
    17: "SIENTA",
    18: "ALTIS",
    19: "Negotiation_table_10",
    20: "Negotiation_table_11",
    21: "SIENTA",
}

GENDER_MAP = {
    0: "Male",
    1: "Female"
}
AGE_MAP = {
    0: "0-15",
    1: "16-30",
    2: "31-45",
    3: "46-60",
    4: "61-"
}

base_directory = os.path.join("csv", base_time_stamp)
print("base_directory: " + base_directory)

dfs_text = []

for camera in CAMERA:
    txt_file_path = os.path.join(base_directory, f"{camera}.txt")

    df_txt = pd.read_csv(txt_file_path, sep='\s+')
    df_txt = df_txt.sort_values(by=['id', 'frame_idx']).reset_index(drop=True)

    # Add a 'camera' field to record the camera
    df_txt.insert(df_txt.columns.get_loc('id'), 'camera', camera)

    # Apply mappings to the 'gender' and 'age' columns
    df_txt['gender'] = df_txt['gender'].map(GENDER_MAP)
    df_txt['age'] = df_txt['age'].map(AGE_MAP)

    # Print details for each camera's file
    print("\n")
    print("------------------------")
    print(f"Text file path for {camera}: {txt_file_path}")
    print(f"First three rows of {camera}.txt content:")
    print(df_txt.head(10))
    print(f"Number of rows in {camera}.txt:", df_txt.shape[0])
    # print(f"Distinct IDs in {camera}.txt:", df_txt['id'].unique())
    print(f"Distinct IDs count in {camera}.txt:", df_txt['id'].nunique())

    # Append the DataFrame to the list
    dfs_text.append(df_txt)

# Combine all DataFrames
df_combined_text = pd.concat(dfs_text, ignore_index=True).sort_values(by=['id', 'camera', 'frame_idx']).reset_index(drop=True)

print("\n")
print("------------------------------------------------")
print("Combined DataFrame:")
print(df_combined_text.head(24))
print("Total number of rows:", df_combined_text.shape[0])
# print("Distinct IDs across all cameras:", df_combined_text['id'].unique())
print("Distinct IDs count across all cameras:", df_combined_text['id'].nunique())
print("------------------------------------------------")

output_file_path = os.path.join("output", f"{base_time_stamp}_combined_text.csv")
df_combined_text.to_csv(output_file_path, index=False)

print(f"\nCombined DataFrame saved to: {output_file_path}")