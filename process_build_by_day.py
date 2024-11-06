import pandas as pd
import os

date_stamp = "2024-11-02"
start_time = 9
end_time = 20

# 選擇建立的csv, 選項： text, entrance, region_car, region_table
csv_type = "entrance"

base_directory = os.path.join("output", date_stamp)
print("base_directory: " + base_directory)

dfs = []

for hour in range(start_time, end_time + 1):
    hour_str = f"{hour:02d}_00_00"
    csv_filename = f"{date_stamp}T{hour_str}_combined_{csv_type}.csv"
    csv_path = os.path.join(base_directory, csv_filename)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)

        print("\n")
        print("------------------------")
        print(f"First three rows of {csv_path}:")
        print(df.head(3))
        print("Number of rows:", df.shape[0])
        
        dfs.append(df)

if dfs:
    df_combined = pd.concat(dfs, ignore_index=True)

    print("\n")
    print("------------------------------------------------")
    print("Combined DataFrame:")
    print(df_combined.head(3))
    print("Total number of rows:", df_combined.shape[0])

    output_directory = "output"
    os.makedirs(output_directory, exist_ok=True)
    output_file_path = os.path.join(output_directory, date_stamp, f"{date_stamp}_combined_{csv_type}.csv")
    df_combined.to_csv(output_file_path, index=False)