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

df_txt = pd.read_csv(txt_file_path, delim_whitespace=True)

print("First three rows of cam002.txt content:")
print(df_txt.head(3))
print("Number of rows:", df_txt.shape[0])
print("Distinct IDs:", df_txt['id'].unique())
print("Distinct IDs count:", df_txt['id'].nunique())

camera_number = int(camera[3:])
modified_camera = f"cam_{camera_number}"

for key, solution in SOLUTION.items():
    csv_filename = f"{modified_camera}_{solution}_{base_time_stamp}.csv"
    csv_path = os.path.join(base_directory, camera, csv_filename)
    print("----------------------------------------------")
    print("csv_path: " + csv_path)

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"\nFirst three rows of {csv_filename}:")
        print(df.head(3))
        print("Number of rows:", df.shape[0])
        print("Distinct IDs:", df['track_id'].unique())
        print("Distinct IDs count:", df['track_id'].nunique())

        solution_data[f"{solution}"] = df
    else:
        print(f"{csv_filename} does not exist.")

df_object_list = (
    df_txt.groupby("id")
    .agg(
        object_id=("id", "first"),                          # 使用不重複的id為主鍵
        face_id=("face_id", "first"),                       # 使用第一個face id
        datetime=("id", lambda x: base_time_stamp),                           # 使用base_time_stamp
        first_show_time=("frame_idx", "min"),               # 最小的frame_idx為入場時間
        last_show_time=("frame_idx", "max"),                # 最大的frame_idx為出場時間
        age=("age", lambda x: x.mode()[0]),                 # age取眾數
        gender=("gender", lambda x: x.mode()[0])            # gender取眾數
    )
    .reset_index(drop=True)
)
print("----------------------------------------------")
print("df_object_list: ")
print(df_object_list.head(10))

processed_dfs = []

for solution_type, df in solution_data.items():
    df['solution_type'] = solution_type
    
    if 'staytime' in df.columns:
        df['property'] = df['staytime']
    elif 'direction' in df.columns:
        df['property'] = df['direction']
    
    processed_dfs.append(df[['track_id', 'datetime', 'baseline', 'solution_type', 'property']])

df_solution = pd.concat(processed_dfs, ignore_index=True)
df_solution.sort_values(by='track_id', inplace=True)
print("----------------------------------------------")
print("Number of rows:", df_solution.shape[0])
print("Distinct IDs:", df_solution['track_id'].unique())
print("Distinct IDs count:", df_solution['track_id'].nunique())
print("df_solution(sort by id): ")
print(df_solution)

df_solution.sort_values(by=['solution_type', 'track_id'], inplace=True)
print("----------------------------------------------")
print("df_solution(sort by solution_type): ")
print(df_solution)
print("Number of rows:", df_solution.shape[0])
print("Distinct IDs:", df_solution['track_id'].unique())
print("Distinct IDs count:", df_solution['track_id'].nunique())