import pandas as pd
import numpy as np

file_path = 'csv/mask_新店/solutions_masks.npy'
data = np.load(file_path, allow_pickle=True).item()

for key, value in data.items():
    print(f"Key: {key}, Value: {value}")

# print(data['cam_3'])
# print(type(data))

# xy_values_1 = data['cam_3']['cam_3_bZ4x']
# xy_values_2 = data['cam_3']['cam_3_RAV4']
# print("xy_values_1")
# print(xy_values_1)
# print(type(xy_values_1))
# print("xy_values_2")
# print(xy_values_2)
# print(type(xy_values_2))

# xy_values = np.vstack((xy_values_1, xy_values_2))

# print(xy_values)
# print(type(xy_values))
# print(xy_values.shape)

# # xy_values = data['cam_3']['cam_2_YARIS_CROSS']
# # df = pd.DataFrame(xy_values, columns=['x', 'y'])
# # print(df)