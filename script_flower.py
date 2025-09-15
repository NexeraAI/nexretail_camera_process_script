import pandas as pd
from datetime import datetime

# Read the CSV file
df = pd.read_csv('csv/flower_tasks.csv')

# Convert the 'started' column to datetime
df['started'] = df['started'].apply(lambda x: datetime.utcfromtimestamp(float(x)))

# Optional: print the dataframe to verify
print(df.head())
print(df['started'])

# Find the peak count of tasks started within any one-minute interval
df_sorted = df.sort_values('started')
df_sorted['minute'] = df_sorted['started'].dt.floor('T')
minute_counts = df_sorted.groupby('minute').size()

print(minute_counts)

peak_minute = minute_counts.idxmax()
peak_count = minute_counts.max()

print(f"Peak count: {peak_count} at {peak_minute}")