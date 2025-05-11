import json
import pandas as pd


def load_json(json_path):
    with open(json_path) as f:
        for line in f:
            data = json.loads(line)
    return data

system_json_path = '/home/nexretail/Documents/example/yolo_tracking/bus/2024-11-02T09:00:00/system.json'
mot_path = '/home/nexretail/Documents/example/yolo_tracking/bus/2024-11-02T09:00:00/cam002.txt'
system_json = load_json(system_json_path)
df_mot = pd.read_csv(mot_path, sep=" ")
if system_json.get('remap_reid', False): # 確認系統檔中reid的資訊
    df_mot['raw_id'] = df_mot['id'] # 先將track_id 存起來
    df_mot['id'] = df_mot['id'].astype(str) # 從json讀來的檔中key會變字串，因此先轉字串
    # 如果 remap表中有該track_id，就重新remap id(pre_id), 沒有則保持元id
    df_mot['id'] = df_mot['id'].apply(lambda x: system_json['remap_reid'].get(x, {"pre_id": x})["pre_id"])
    df_mot['id'] = df_mot['id'].astype(int)# 轉回int
print (df_mot)