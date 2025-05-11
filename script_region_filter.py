import pandas as pd
import json

date = "2024-12-13"

# Read the CSV files
df = pd.read_csv(f"output/{date}/{date}_combined_region_table.csv")
df_customer = pd.read_csv(f"output/{date}/{date}_combined_entrance.csv")

df_filtered = df[df['track_id'].isin(df_customer['track_id'])]
df_filtered.to_csv(f"output/{date}/{date}_combined_region_table_id_filtered.csv", index=False)

df_filtered = df[df['staytime'] >= 500]
df_filtered.to_csv(f"output/{date}/{date}_combined_region_table_staytime_filtered.csv", index=False)

result_df = (
    df_filtered.groupby(['track_id', 'solution'])
    .agg(min_datetime=('datetime', 'min'), max_datetime=('datetime', 'max'))
    .reset_index()
)

result_df.to_csv(f"output/{date}/{date}_combined_region_table_result.csv", index=False)

solutions_by_track_id = (
    result_df.groupby('track_id')['solution']
    .apply(', '.join)
    .reset_index()
    .rename(columns={'solution': 'region'})
)

df_customer = df_customer.merge(solutions_by_track_id, on='track_id', how='left')

df_customer["M0-15"] = df_customer.apply(lambda row: 1 if row["age"] == "0-15" and row["gender"] == "Male" else 0, axis=1)
df_customer["M16-30"] = df_customer.apply(lambda row: 1 if row["age"] == "16-30" and row["gender"] == "Male" else 0, axis=1)
df_customer["M31-45"] = df_customer.apply(lambda row: 1 if row["age"] == "31-45" and row["gender"] == "Male" else 0, axis=1)
df_customer["M46-60"] = df_customer.apply(lambda row: 1 if row["age"] == "46-60" and row["gender"] == "Male" else 0, axis=1)
df_customer["F0-15"] = df_customer.apply(lambda row: 1 if row["age"] == "0-15" and row["gender"] == "Female" else 0, axis=1)
df_customer["F16-30"] = df_customer.apply(lambda row: 1 if row["age"] == "16-30" and row["gender"] == "Female" else 0, axis=1)
df_customer["F31-45"] = df_customer.apply(lambda row: 1 if row["age"] == "31-45" and row["gender"] == "Female" else 0, axis=1)
df_customer["F46-60"] = df_customer.apply(lambda row: 1 if row["age"] == "46-60" and row["gender"] == "Female" else 0, axis=1)

df_customer["Total Male + Female"] = df_customer["M0-15"] + df_customer["M16-30"] + df_customer["M31-45"] + df_customer["M46-60"] + df_customer["F0-15"] + df_customer["F16-30"] + df_customer["F31-45"] + df_customer["F46-60"]
df_customer["Total Male"] = df_customer["M0-15"] + df_customer["M16-30"] + df_customer["M31-45"] + df_customer["M46-60"]
df_customer["Total Female"] =df_customer["F0-15"] + df_customer["F16-30"] + df_customer["F31-45"] + df_customer["F46-60"]

column_order = ['track_id', 'second_show', 'gender', 'age', 'staytime', 'solution', 'direction', 'region', 'group', 'is_group', 'group_head_count', 'group_gender', 'group_with_youth', 'datetime', 'Camera', 'Shop', 'img_path', 'M0-15', 'M16-30', 'M31-45', 'M46-60', 'F0-15', 'F16-30', 'F31-45', 'F46-60', 'Total Male + Female', 'Total Male', 'Total Female']
df_customer = df_customer[column_order]

# df_customer.rename(columns={"second_show": "第二次出現"}, inplace=True)
# df_customer.rename(columns={"gender": "性別"}, inplace=True)
# df_customer.rename(columns={"age": "年齡"}, inplace=True)
# df_customer.rename(columns={"region": "使用商談區"}, inplace=True)
# df_customer.rename(columns={"is_group": "是群組"}, inplace=True)
# df_customer.rename(columns={"group_head_count": "群組人數"}, inplace=True)
# df_customer.rename(columns={"group_gender": "群組性別組成"}, inplace=True)
# df_customer.rename(columns={"group_with_youth": "群組是否有小孩"}, inplace=True)

df_customer.rename(columns={"Camera": "camera"}, inplace=True)
df_customer.rename(columns={"Shop": "shop"}, inplace=True)
df_customer.rename(columns={"M0-15": "m_0_15"}, inplace=True)
df_customer.rename(columns={"M16-30": "m_16_30"}, inplace=True)
df_customer.rename(columns={"M31-45": "m_31_45"}, inplace=True)
df_customer.rename(columns={"M46-60": "m_46_60"}, inplace=True)
df_customer.rename(columns={"F0-15": "f_0_15"}, inplace=True)
df_customer.rename(columns={"F16-30": "f_16_30"}, inplace=True)
df_customer.rename(columns={"F31-45": "f_31_45"}, inplace=True)
df_customer.rename(columns={"F46-60": "f_46_60"}, inplace=True)
df_customer.rename(columns={"Total Male + Female": "total_male_female"}, inplace=True)
df_customer.rename(columns={"Total Male": "total_male"}, inplace=True)
df_customer.rename(columns={"Total Female": "total_female"}, inplace=True)


json_payload = df_customer.to_json(orient="records")
print(json_payload)

df_customer.to_csv(f"output/{date}/{date}_combined_entrance_with_region_dbready.csv", index=False)