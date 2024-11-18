from datetime import datetime, timedelta
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

solution_data_processor = {
    "entrance": [],
    "region_car": [],
    "region_table": []
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
    def __init__(self, base_directory, base_day_stamp, processor_type="default", start_time = 9, end_time = 20, output_base_direction = "output"):
        self.base_directory = base_directory
        self.file_directory = ""

        self.base_day_stamp = base_day_stamp
        self.base_time_stamp = ""
        self.current_time = ""

        self.processor_type = processor_type
        
        self.start_time = start_time
        self.end_time = end_time 
        
        self.df = None
        self.df_object = None
        self.df_object_reference = None
        
        self.output_directory = os.path.join(output_base_direction, self.base_day_stamp)
        os.makedirs(self.output_directory, exist_ok=True)

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
            print(f"Directory {self.output_directory} created.")
        
        print(self.base_directory + " processing " + self.processor_type)

    def hourly_process_base_text(self):
        dfs_text = []

        for camera in CAMERA:
            txt_file_path = os.path.join(self.file_directory, f"{camera}.txt")

            df_txt = pd.read_csv(txt_file_path, sep='\s+')
            df_txt = df_txt.sort_values(by=['id', 'frame_idx']).reset_index(drop=True)

            # Add a 'camera' field to record the camera
            df_txt.insert(df_txt.columns.get_loc('id'), 'camera', camera)

            # Apply mappings to the 'gender' and 'age' columns
            # df_txt['gender'] = df_txt['gender'].map(GENDER_MAP)
            # df_txt['age'] = df_txt['age'].map(AGE_MAP)

            # Append the DataFrame to the list
            dfs_text.append(df_txt)

        # Combine all DataFrames
        self.df = pd.concat(dfs_text, ignore_index=True).sort_values(by=['id', 'camera', 'frame_idx']).reset_index(drop=True)
        self.df['datetime'] = self.df.apply(
            lambda row: self.current_time + timedelta(seconds=row['frame_idx'] / 10), axis=1
        )

        # print("\n")
        # print("------------------------------------------------")
        # print("Combined DataFrame:")
        # print(self.df.head(24))
        # print("Total number of rows:", self.df.shape[0])
        # print("Distinct IDs across all cameras:", self.df['id'].unique())
        # print("Distinct IDs count across all cameras:", self.df['id'].nunique())
        # print("------------------------------------------------")

    def hourly_process_entrance(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["entrance"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.file_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    # df['age'] = df['age'].map(AGE_MAP)
                    df['group'] = self.base_time_stamp + '_' + df['group'].astype(str)
                    df['age'] = df['track_id'].map(self.df_object_reference.set_index('id')['age'])
                    df['gender'] = df['track_id'].map(self.df_object_reference.set_index('id')['gender'])

                    dfs.append(df)
        if dfs:
            self.df = pd.concat(dfs, ignore_index=True).sort_values(by=['track_id', 'baseline']).reset_index(drop=True)

            if 'baseline' in self.df.columns:
                self.df = self.df.rename(columns={'baseline': 'solution'})

            # Display and save the combined DataFrame
            # print("\n")
            # print("------------------------------------------------")
            # print("Combined DataFrame:")
            # print(self.df.head(3))
            # print("Total number of rows:", self.df.shape[0])

    def hourly_process_region_car(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["region_car"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.file_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    # df['age'] = df['age'].map(AGE_MAP)
                    df['age'] = df['track_id'].map(self.df_object_reference.set_index('id')['age'])
                    df['gender'] = df['track_id'].map(self.df_object_reference.set_index('id')['gender'])

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

    def hourly_process_region_table(self):
        dfs = []

        for camera in CAMERA:
            camera_number = int(camera[3:])
            modified_camera = f"cam_{camera_number}"

            for solution_id in solution_sets["region_table"]:
                solution_name = SOLUTION[solution_id]
                csv_filename = f"{modified_camera}_{solution_name}_{self.base_time_stamp}.csv"
                csv_path = os.path.join(self.file_directory, camera, csv_filename)

                # Check if the file exists before attempting to read it
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)

                    # df['age'] = df['age'].map(AGE_MAP)
                    df['age'] = df['track_id'].map(self.df_object_reference.set_index('id')['age'])
                    df['gender'] = df['track_id'].map(self.df_object_reference.set_index('id')['gender'])

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

    def hourly_process(self):
        """
        combine data from multiple camera and create a hourly dataset
        """
        if self.processor_type == "base_text":
            self.hourly_process_base_text()
        if self.processor_type == "entrance":
            self.hourly_process_entrance()
        if self.processor_type == "region_car":
            self.hourly_process_region_car()
        if self.processor_type == "region_table":
            self.hourly_process_region_table()
        
        return self.df
    
    def daily_process(self):
        """
        combine data from multiple camera and create a daily dataset and apply filters
        """
        list_dfs = []
        for hour in range(self.start_time, self.end_time + 1):
            hour_str = f"{hour:02d}_00_00"
            self.base_time_stamp = self.base_day_stamp + "T" + hour_str
            self.current_time = datetime.strptime(self.base_day_stamp, "%Y-%m-%d").replace(hour=hour)
            self.file_directory = os.path.join(self.base_directory, self.base_time_stamp)

            list_dfs.append(self.hourly_process())
        
        if list_dfs:
            self.df = pd.concat(list_dfs, ignore_index=True)

            if self.processor_type == "entrance":
            #     if 'baseline' in self.df.columns:
            #         self.df = self.df.rename(columns={'baseline': 'solution'})
                
            #     self.df['group_head_count'] = self.df.groupby('group')['group'].transform('size')
            #     self.df['group_gender'] = self.df.groupby('group')['gender'].transform(lambda x: ', '.join(x))
            #     self.df['group_with_youth'] = self.df.groupby('group')['age'].transform(lambda x: 'Y' if '0-15' in x.values else 'N')

                # calculate staytime
                self.df_object = self.df_object[self.df_object['id'].isin(self.df['track_id'])]

                self.df_object['datetime'] = pd.to_datetime(self.df_object['datetime'])
                self.df_object['hour'] = self.df_object['datetime'].dt.floor('h')
                self.df_object = self.df_object.groupby(['id', 'hour']).filter(lambda x: len(x) >= 20)
                # self.df_object['h_mark'] = self.df_object.groupby(['id', 'hour'])['id'].transform('size').apply(lambda x: 'Y' if x < 20 else 'N')

                self.df['staytime'] = ''

                end_of_day = datetime.strptime(self.base_day_stamp, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                rows_to_remove = []

                # self.df['max_datetime'] = None
                # self.df['min_datetime'] = None
                # self.df['is_remove'] = ''

                for track_id, group in self.df.groupby('track_id'):
                    # if track_id == 200:
                    #     print(group)
                    for _, row in group.iterrows():
                        start_time = row['datetime']
                        next_index = group.index.get_loc(row.name) + 1
                        if next_index < len(group):
                            end_time = group.iloc[next_index]['datetime']
                        else:
                            end_time = end_of_day

                        filtered_df = self.df_object[(self.df_object['id'] == track_id) & 
                                                     (self.df_object['datetime'] >= start_time) & 
                                                     (self.df_object['datetime'] <= end_time)]

                        # if track_id == 200:
                        #     print("group: " + str(len(group)))
                        #     print("start time: " + str(start_time))
                        #     print("end time: " + str(end_time))
                        #     print(filtered_df)
                        
                        max_datetime = filtered_df['datetime'].max() if not filtered_df.empty else None
                        min_datetime = filtered_df['datetime'].min() if not filtered_df.empty else None

                        # self.df.at[row.name, 'max_datetime'] = max_datetime
                        # self.df.at[row.name, 'min_datetime'] = min_datetime

                        if max_datetime and min_datetime:
                            time_difference = max_datetime - min_datetime
                            if time_difference < timedelta(minutes=5):
                                rows_to_remove.append(row.name)
                                # self.df.at[row.name, 'is_remove'] = 'Y'
                                continue

                            hours = time_difference.seconds // 3600
                            minutes = (time_difference.seconds % 3600) // 60
                            seconds = time_difference.seconds % 60
                            formatted_time_difference = f"{hours:02}:{minutes:02}:{seconds:02}"

                            self.df.at[row.name, 'staytime'] = formatted_time_difference

                self.df.drop(index=rows_to_remove, inplace=True)
                # self.df.dropna(subset=['staytime'], inplace=True)
                self.df = self.df[self.df['staytime'] != ""]

                self.df['second_show'] = ''
                mask = (self.df.groupby('track_id')['track_id'].transform('size') > 1) & (self.df.groupby('track_id').cumcount() != 0)
                self.df.loc[mask, 'second_show'] = 'Y'

                self.df['group_head_count'] = self.df.groupby('group')['group'].transform('size')
                # self.df['track_id_count'] = self.df.groupby('track_id')['track_id'].transform('size')
                self.df['group_gender'] = self.df.groupby('group')['gender'].transform(lambda x: ', '.join(x))
                self.df['group_with_youth'] = self.df.groupby('group')['age'].transform(lambda x: 'Y' if '0-15' in x.values else 'N')
                # self.df['is_group'] = self.df.groupby('group').cumcount().apply(lambda x: 'Y' if x == 0 else '')
                self.df['is_group'] = self.df.groupby('group').cumcount().apply(
                    # lambda x: 'Y' if x == 0 and self.df.loc[x, 'group_head_count'] > 1 else ''
                    lambda x: 'Y' if x == 0 else ''
                )
                self.df['is_group'] = ''
                self.df.loc[self.df.groupby('group').head(1).index, 'is_group'] = \
                    self.df.groupby('group')['group'].transform('size').gt(1).map({True: 'Y', False: ''})

                # column_order = ['track_id', 'gender', 'age', 'solution', 'direction', 'group', 'is_group', 'group_head_count', 'group_gender', 'group_with_youth', 'datetime', 'Camera', 'Shop' , 'img_path']
                # self.df = self.df[column_order]

                column_order = ['track_id', 'second_show', 'gender', 'age', 'staytime', 'solution', 'direction', 'group', 'is_group', 'group_head_count', 'group_gender', 'group_with_youth', 'datetime', 'Camera', 'Shop' , 'img_path']
                self.df = self.df[column_order]
                output_file_path = os.path.join(self.output_directory, f"{self.base_day_stamp}_combined_bast_text_filtered.csv")
                self.df_object.to_csv(output_file_path, index=False)
            
            print("\n------------------------------------------------")
            print("Combined DataFrame: " + f"{self.processor_type}")
            print(self.df.head(3))
            print("\nTotal number of rows:", self.df.shape[0])

            if self.processor_type == "aaa":
                pass
            else:
                output_file_path = os.path.join(self.output_directory, f"{self.base_day_stamp}_combined_{self.processor_type}.csv")
                self.df.to_csv(output_file_path, index=False)

                print(f"Combined DataFrame saved to: {output_file_path}")
            
            if self.processor_type == "base_text":
                print("\n------------------------------------------------")
                print("creating object reference")

                self.df_object = self.df

                self.df_object_reference = self.df.groupby('id').agg({
                    # 'age': 'mean',
                    'age': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
                    'gender': lambda x: x.mode().iloc[0] if not x.mode().empty else None,
                }).reset_index()

                self.df_object_reference['gender'] = self.df_object_reference['gender'].map(GENDER_MAP)
                self.df_object_reference['age'] = self.df_object_reference['age'].map(AGE_MAP)

                print("Combined DataFrame: " + f"{self.processor_type}")
                print(self.df_object_reference.head(3))
                print("\nTotal number of rows:", self.df_object_reference.shape[0])

                output_file_path = os.path.join(self.output_directory, f"{self.base_day_stamp}_combined_{self.processor_type}_object_reference.csv")
                self.df_object_reference.to_csv(output_file_path, index=False)
                
            return True
    
    def output_process(self, start_time = 9, end_time = 20):
        """
        create all output files for camera data
        """
        print("Processing output for NexRetail camera data")

        output_set = ["base_text", "entrance", "region_car", "region_table"]
        # output_set = ["base_text", "entrance"]

        for output in output_set:
            self.processor_type = output
            self.daily_process()