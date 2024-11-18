from datetime import datetime, timedelta
import os
import pandas as pd

source ="output/2024-11-05/2024-11-05_combined_bast_text_filtered.csv"

df = pd.read_csv(source)

df['datetime'] = pd.to_datetime(df['datetime'])
df['hour'] = df['datetime'].dt.floor('h')
df_grouped = df.groupby(['id', 'hour']).filter(lambda x: len(x) >= 50)

df_grouped.to_csv("output/2024-11-05/2024-11-05_combined_bast_text_filtered_remove_noise.csv", index=False)