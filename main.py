import os
import pandas as pd
import time

from processor.camera_data_processor import CameraDataProcessor

start_time = 9
end_time = 20

if __name__ == "__main__":
    start_time = time.time()

    # ------------ INPUT section ------------
    inference_path = "csv/2024-11-02/"
    date_stamp = "2024-11-02"
    # ---------------------------------------
    processor = CameraDataProcessor(inference_path, date_stamp)
    processor.output_process()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")

    # dfs_base_text = []
    # dfs_entrance = []
    # dfs_region_car = []
    # dfs_region_table = []


    # for hour in range(start_time, end_time + 1):
    #     print("------------------------------------------------")
    #     hour_str = f"{hour:02d}_00_00"
    #     base_time_stamp = date_stamp + "T" + hour_str
    #     base_directory = os.path.join("csv", date_stamp, base_time_stamp)
    #     print(base_directory)

    #     processor_base_text = CameraDataProcessor(base_directory, base_time_stamp, processor_type="base_text")
    #     dfs_base_text.append(processor_base_text.hourly_process())

        # processor_entrance = CameraDataProcessor(base_directory, base_time_stamp, processor_type="entrance")
        # dfs_entrance.append(processor_entrance.process())

        # processor_region_car = CameraDataProcessor(base_directory, base_time_stamp, processor_type="region_car")
        # dfs_region_car.append(processor_region_car.process())

        # processor_region_table = CameraDataProcessor(base_directory, base_time_stamp, processor_type="region_table")
        # dfs_region_table.append(processor_region_table.process())

    # output_directory = os.path.join("output", date_stamp)
    # os.makedirs(output_directory, exist_ok=True)

    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    #     print(f"Directory {output_directory} created.")
        
    # if dfs_base_text:
    #     df_base_text = pd.concat(dfs_base_text, ignore_index=True)

    #     print("\n")
    #     print("------------------------------------------------")
    #     print("Combined DataFrame:")
    #     print(df_base_text.head(3))
    #     print("Total number of rows:", df_base_text.shape[0])

    #     output_file_path = os.path.join(output_directory, f"{base_time_stamp}_combined_text.csv")
    #     df_base_text.to_csv(output_file_path, index=False)

    #     print(f"\nCombined DataFrame saved to: {output_file_path}")
    
    # if dfs_entrance:
    #     df_entrance = pd.concat(dfs_entrance, ignore_index=True)

    #     df_filtered = df_base_text[df_base_text['id'].isin(df_entrance['track_id'])]

    #     df_staytime = (
    #         df_filtered.groupby('id')['frame_idx']
    #         .agg(staytime=lambda x: f"{int((x.max() - x.min())/10 // 60)} min {int((x.max() - x.min())/10 % 60)} sec")
    #         .reset_index()
    #     )

    #     staytime_df = df_staytime.rename(columns={'id': 'track_id'})
    #     df_entrance_with_staytime = df_entrance.merge(staytime_df, on='track_id', how='left')

    #     print("\n")
    #     print("------------------------------------------------")
    #     print("Combined DataFrame:")
    #     print(df_entrance_with_staytime.head(3))
    #     print("Total number of rows:", df_entrance_with_staytime.shape[0])

    #     output_file_path = os.path.join(output_directory, f"{base_time_stamp}_combined_entrance.csv")
    #     df_entrance_with_staytime.to_csv(output_file_path, index=False)

    #     print(f"\nCombined DataFrame for entrance saved to: {output_file_path}")

    # if dfs_region_car:
    #     df_region_car = pd.concat(dfs_region_car, ignore_index=True)

    #     print("\n")
    #     print("------------------------------------------------")
    #     print("Combined DataFrame:")
    #     print(df_region_car.head(3))
    #     print("Total number of rows:", df_region_car.shape[0])

    #     output_file_path = os.path.join(output_directory, f"{base_time_stamp}_combined_region_car.csv")
    #     df_region_car.to_csv(output_file_path, index=False)

    #     print(f"\nCombined DataFrame for region car saved to: {output_file_path}")

    # if dfs_region_table:
    #     df_region_table = pd.concat(dfs_region_table, ignore_index=True)

    #     print("\n")
    #     print("------------------------------------------------")
    #     print("Combined DataFrame:")
    #     print(df_region_table.head(3))
    #     print("Total number of rows:", df_region_table.shape[0])

    #     output_file_path = os.path.join(output_directory, f"{base_time_stamp}_combined_region_table.csv")
    #     df_region_table.to_csv(output_file_path, index=False)

    #     print(f"\nCombined DataFrame for region table saved to: {output_file_path}")
        
