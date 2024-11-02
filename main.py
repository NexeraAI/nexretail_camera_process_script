import pandas as pd
import os

SOLUTION = {
    1: "car_near_door",
    2: "desk_near_door",
    3: "desk_near_first_car",
    4: "entrance_shop",
}

base_time_stamp = "2024-10-28T09_00_00"
camera = "cam002"

solution_data = {}

base_directory = os.path.join("csv", base_time_stamp)
print("base_directory: " + base_directory)

txt_file_path = os.path.join(base_directory, f"{camera}.txt")

print("text file path: " + txt_file_path)

txt_df = pd.read_csv(txt_file_path, delim_whitespace=True)

print("First three rows of cam002.txt content:")
print(txt_df.head(3))
print("Number of rows:", txt_df.shape[0])
print("Distinct IDs:", txt_df['id'].unique())
print("Distinct IDs count:", txt_df['id'].nunique())

camera_number = int(camera[3:])
modified_camera = f"cam_{camera_number}"

for key, solution in SOLUTION.items():
    csv_filename = f"{modified_camera}_{solution}_{base_time_stamp}.csv"
    csv_path = os.path.join(base_directory, camera, csv_filename)

    print("csv_path: " + csv_path)

    if os.path.exists(csv_path):
        # Load the CSV file into a DataFrame and display the first three rows
        df = pd.read_csv(csv_path)
        print(f"\nFirst three rows of {csv_filename}:")
        print(df.head(3))
        print("Number of rows:", df.shape[0])
        print("Distinct IDs:", df['track_id'].unique())
        print("Distinct IDs count:", df['track_id'].nunique())

        solution_data[f"{solution}"] = df
    else:
        print(f"{csv_filename} does not exist.")

print(solution_data)