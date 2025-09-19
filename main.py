import os
import pandas as pd

from processor.camera_data_processor_v2 import CameraDataProcessor
import json

from script_actions_filter import process_action_data
from script_region_processor import process_region_data
from script_car_plate_processor import process_car_plate_data
from script_camera_heatmap import process_camera_heatmap_data

# @resource_monitor
def main_process(location, date_stamp):

    print(f"Processing data for location: {location}, date: {date_stamp}")

    inference_start_time = 9
    inference_end_time = 20
    
    # Load configuration from a JSON file
    config_path = "config.json"
    
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    camera = config["locations"][location]["CAMERA"]
    location_id = config["locations"][location]["LOCATION"]
    entrance = config["locations"][location]["entrance"]
    region_car = config["locations"][location]["region_car"]
    region_table = config["locations"][location]["region_table"]

    inference_path = f"csv/{location}/{date_stamp}/"
    output_path = f"output/{location}/"

    processor = CameraDataProcessor(
        camera,
        location_id,
        entrance,
        region_car,
        region_table,
        inference_path,
        date_stamp,
        start_time = inference_start_time,
        end_time = inference_end_time,
        output_base_direction = output_path,
    )
    processor.output_process()

    process_action_data(date_stamp, location)
    process_region_data(date_stamp, location)
    process_car_plate_data(date_stamp, location)
    process_camera_heatmap_data(date_stamp, location)

if __name__ == "__main__":

    date_stamp = "2025-09-17"

    locations = [
        # "新莊",
        # "新竹",
        # "西台南",
        # "鳳山",
        # "中台中",
        "新店",
        # "桃園PIC",
    ]
    
    for location in locations:
        main_process(location, date_stamp)
