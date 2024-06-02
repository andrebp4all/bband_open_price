import pandas as pd

# Load bb5m.csv and open_data.csv
bb5m_df = pd.read_csv('data/bb5m.csv')
open_data_df = pd.read_csv('data/open_data.csv')

# Convert the 'formatted_date' column to datetime format
bb5m_df['formatted_date'] = pd.to_datetime(bb5m_df['formatted_date'], format='%m/%d/%Y')
open_data_df['date'] = pd.to_datetime(open_data_df['date'], format='%d/%m/%Y')

# Merge the DataFrames on 'formatted_date'
merged_df = pd.merge(bb5m_df, open_data_df, left_on='formatted_date', right_on='date', how='left')

# Filter the data to get rows where time is 9:30:00 and open > bollinger_band_upper
filtered_df = merged_df[(merged_df['time'] == '09:30:00') & (merged_df['open'] > merged_df['bollinger_band_upper'])]

# Select the required columns
result_df = filtered_df[['formatted_date', 'open', 'bollinger_band_upper']]

# Save the filtered data to result.csv
result_df.to_csv('data/result.csv', index=False, float_format='%.2f')

print("Filtered data saved to result.csv")
