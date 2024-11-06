import os
import pandas as pd

CAMERA = ["cam002", "cam003", "cam004", "cam005", "cam006"]

entrance = [1]
region_car = [4, 5, 7, 11, 12, 13, 17, 18, 21]
region_table = [2, 3, 6, 8, 9, 10, 14, 15, 16, 19, 20]

solution_sets = {
    "entrance": entrance,
    "region_car": region_car,
    "region_table": region_table
}

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

class CameraDataProcessor:
    def __init__(self, base_directory, base_time_stamp, processor_type="default"):
        self.base_directory = base_directory
        self.base_time_stamp = base_time_stamp
        self.processor_type = processor_type
        self.df = None
        
        print(self.base_directory + " processing " + self.processor_type)

    def process_base_text(self):
        dfs_text = []

        for camera in CAMERA:
            txt_file_path = os.path.join(self.base_directory, f"{camera}.txt")

            df_txt = pd.read_csv(txt_file_path, sep='\s+')
            df_txt = df_txt.sort_values(by=['id', 'frame_idx']).reset_index(drop=True)

            # Add a 'camera' field to record the camera
            df_txt.insert(df_txt.columns.get_loc('id'), 'camera', camera)

            # Apply mappings to the 'gender' and 'age' columns
            df_txt['gender'] = df_txt['gender'].map(GENDER_MAP)
            df_txt['age'] = df_txt['age'].map(AGE_MAP)

            # Append the DataFrame to the list
            dfs_text.append(df_txt)

        # Combine all DataFrames
        self.df = pd.concat(dfs_text, ignore_index=True).sort_values(by=['id', 'camera', 'frame_idx']).reset_index(drop=True)

        # print("\n")
        # print("------------------------------------------------")
        # print("Combined DataFrame:")
        # print(self.df.head(24))
        # print("Total number of rows:", self.df.shape[0])
        # print("Distinct IDs across all cameras:", self.df['id'].unique())
        # print("Distinct IDs count across all cameras:", self.df['id'].nunique())
        # print("------------------------------------------------")

    def process_entrance(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["entrance"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.base_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    df['age'] = df['age'].map(AGE_MAP)

                    dfs.append(df)
        if dfs:
            self.df = pd.concat(dfs, ignore_index=True).sort_values(by=['track_id', 'baseline']).reset_index(drop=True)

            if 'baseline' in self.df.columns:
                self.df = self.df.rename(columns={'baseline': 'solution'})
            
            self.df['group_head_count'] = self.df.groupby('group')['group'].transform('size')
            self.df['group_gender'] = self.df.groupby('group')['gender'].transform(lambda x: ', '.join(x))
            self.df['group_with_youth'] = self.df.groupby('group')['age'].transform(lambda x: 'Y' if '0-15' in x.values else 'N')

            column_order = ['track_id', 'gender', 'age', 'solution', 'direction', 'group', 'group_head_count', 'group_with_youth', 'datetime', 'Camera', 'Shop' , 'img_path']
            self.df = self.df[column_order]

            # Display and save the combined DataFrame
            # print("\n")
            # print("------------------------------------------------")
            # print("Combined DataFrame:")
            # print(self.df.head(3))
            # print("Total number of rows:", self.df.shape[0])

    def process_region_car(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["region_car"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.base_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    df['age'] = df['age'].map(AGE_MAP)

                    # print("\n")
                    # print("------------------------")
                    # print(f"First three rows of {csv_path}:")
                    # print(df.head(3))
                    # print("Number of rows:", df.shape[0])
                    # print("Distinct IDs:", df['track_id'].unique())
                    # print("Distinct IDs count:", df['track_id'].nunique())
                    
                    dfs.append(df)

        if dfs:
            self.df = pd.concat(dfs, ignore_index=True).sort_values(by=['track_id', 'baseline']).reset_index(drop=True)

            if 'baseline' in self.df.columns:
                self.df = self.df.rename(columns={'baseline': 'solution'})
            
            column_order = ['track_id', 'gender', 'age', 'solution', 'staytime', 'datetime', 'Camera', 'Shop']
            self.df = self.df[column_order]

            # Display and save the combined DataFrame
            # print("\n")
            # print("------------------------------------------------")
            # print("Combined DataFrame:")
            # print(self.df.head(3))
            # print("Total number of rows:", self.df.shape[0])

    def process_region_table(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["region_table"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.base_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    df['age'] = df['age'].map(AGE_MAP)

                    # print("\n")
                    # print("------------------------")
                    # print(f"First three rows of {csv_path}:")
                    # print(df.head(3))
                    # print("Number of rows:", df.shape[0])
                    # print("Distinct IDs:", df['track_id'].unique())
                    # print("Distinct IDs count:", df['track_id'].nunique())
                    
                    dfs.append(df)

        if dfs:
            self.df = pd.concat(dfs, ignore_index=True).sort_values(by=['track_id', 'baseline']).reset_index(drop=True)

            if 'baseline' in self.df.columns:
                self.df = self.df.rename(columns={'baseline': 'solution'})
            
            column_order = ['track_id', 'gender', 'age', 'solution', 'staytime', 'datetime', 'Camera', 'Shop']
            self.df = self.df[column_order]

            # Display and save the combined DataFrame
            # print("\n")
            # print("------------------------------------------------")
            # print("Combined DataFrame:")
            # print(self.df.head(3))
            # print("Total number of rows:", self.df.shape[0])

    def process(self):
        if self.processor_type == "base_text":
            self.process_base_text()
        if self.processor_type == "entrance":
            self.process_entrance()
        if self.processor_type == "region_car":
            self.process_region_car()
        if self.processor_type == "region_table":
            self.process_region_table()
        
        return self.df