import os
import pandas as pd

# from lib.resource_monitor import resource_monitor

from processor.camera_data_processor_v2 import CameraDataProcessor


if __name__ == "__main__":
    # @resource_monitor
    def main():
        # ------------ INPUT section ------------
        date_stamp = "2025-05-09"
        inference_start_time = 9
        inference_end_time = 20
        # ---------------------------------------
        inference_path = f"csv/{date_stamp}/"
        processor = CameraDataProcessor(inference_path, date_stamp, start_time = inference_start_time, end_time = inference_end_time, output_base_direction = "output/")
        processor.output_process()

    main()