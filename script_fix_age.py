import pandas as pd

# Read the CSV files
df = pd.read_csv("output/output/entrance_with_staytime.csv")

AGE_MAP = {
    0: "0-15",
    1: "16-30",
    2: "31-45",
    3: "46-60",
    4: "61-"
}

df['age'] = df['age'].map(AGE_MAP)

output_file_path = "output/output/entrance_with_staytime_fix_age.csv"
df.to_csv(output_file_path, index=False)