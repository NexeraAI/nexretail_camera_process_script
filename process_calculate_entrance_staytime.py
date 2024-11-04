import pandas as pd

# Read the CSV files
df_entrance = pd.read_csv("output/2024-11-01T09_00_00_combined_entrance.csv")
df_combined_text = pd.read_csv("output/2024-11-01T09_00_00_combined_text.csv")

print("\n")
print("------------------------")
print(df_entrance.head(10))
print(f"Number of rows in df_entrance:", df_entrance.shape[0])
print(df_combined_text.head(10))
print(f"Number of rows in df_combined_text:", df_combined_text.shape[0])
# print(f"Distinct IDs in df_combined_text:", df_combined_text['id'].unique())
# print(f"Distinct IDs count in df_combined_text:", df_combined_text['id'].nunique())

df_filtered_combined = df_combined_text[df_combined_text['id'].isin(df_entrance['track_id'])]

df_staytime = (
    df_filtered_combined.groupby('id')['frame_idx']
    .agg(staytime=lambda x: f"{int((x.max() - x.min())/10 // 60)} min {int((x.max() - x.min())/10 % 60)} sec")
    .reset_index()
)

print(f"Number of rows in df_staytime:", df_staytime.shape[0])
print(df_staytime)

staytime_df = df_staytime.rename(columns={'id': 'track_id'})
entrance_df = df_entrance.merge(staytime_df, on='track_id', how='left')

entrance_df.to_csv("output/entrance_with_staytime.csv", index=False)

print("Updated entrance.csv with staytime saved as entrance_with_staytime.csv")