import pandas as pd
import os

date_stamp = "2024-11-02"
time_stamp = "09_00_00"
base_time_stamp = date_stamp + "T" + time_stamp
# 選擇建立的solution, 選項： region_car, region_table
selected_solution_name = "region_table"

CAMERA = ["cam002", "cam003", "cam004", "cam005", "cam006"]\

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
AGE_MAP = {
    0: "0-15",
    1: "16-30",
    2: "31-45",
    3: "46-60",
    4: "61-"
}

entrance = [1]
region_car = [4, 5, 7, 11, 12, 13, 17, 18, 21]
region_table = [2, 3, 6, 8, 9, 10, 14, 15, 16, 19, 20]

solution_sets = {
    "entrance": entrance,
    "region_car": region_car,
    "region_table": region_table
}

selected_set = solution_sets[selected_solution_name]

base_directory = os.path.join("csv", date_stamp, base_time_stamp)
print("base_directory: " + base_directory)

dfs = []

print("----------------------------------------------")
for camera in CAMERA:
    camera_number = int(camera[3:])
    modified_camera = f"cam_{camera_number}"

    for solution_id in selected_set:
        solution_name = SOLUTION[solution_id]
        csv_filename = f"{modified_camera}_{solution_name}_{base_time_stamp}.csv"
        csv_path = os.path.join(base_directory, camera, csv_filename)

        # Check if the file exists before attempting to read it
        if os.path.exists(csv_path):
            print("find csv_path:", csv_path)
            df = pd.read_csv(csv_path)

            df['age'] = df['age'].map(AGE_MAP)

            print("\n")
            print("------------------------")
            print(f"First three rows of {csv_path}:")
            print(df.head(3))
            print("Number of rows:", df.shape[0])
            print("Distinct IDs:", df['track_id'].unique())
            print("Distinct IDs count:", df['track_id'].nunique())
            
            dfs.append(df)

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True).sort_values(by=['track_id', 'baseline']).reset_index(drop=True)

    if 'baseline' in combined_df.columns:
        combined_df = combined_df.rename(columns={'baseline': 'solution'})
    
    column_order = ['track_id', 'gender', 'age', 'solution', 'staytime', 'datetime', 'Camera', 'Shop']
    combined_df = combined_df[column_order]

    # Display and save the combined DataFrame
    print("\n")
    print("------------------------------------------------")
    print("Combined DataFrame:")
    print(combined_df.head(3))
    print("Total number of rows:", combined_df.shape[0])

    # Save the combined DataFrame to a CSV file
    output_directory = "output"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, date_stamp, f"{base_time_stamp}_combined_{selected_solution_name}.csv")
    combined_df.to_csv(output_file_path, index=False)

    print(f"\nCombined DataFrame for {selected_solution_name} saved to: {output_file_path}")
else:
    print(f"No files found for the specified {selected_solution_name} solutions.")
