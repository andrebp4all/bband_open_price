import pandas as pd
from datetime import datetime, timedelta

# Define the cutoff date as two years ago from today
cutoff_date = datetime.now() - timedelta(days=730)

# Load bb5m.csv and open_data.csv
bb5m_df = pd.read_csv('data/bb5m.csv')
open_data_df = pd.read_csv('data/open_data.csv')

# Convert the 'formatted_date' column to datetime format
bb5m_df['formatted_date'] = pd.to_datetime(bb5m_df['formatted_date'], format='%m/%d/%Y')
open_data_df['date'] = pd.to_datetime(open_data_df['date'], format='%d/%m/%Y')

# Merge the DataFrames on 'formatted_date'
merged_df = pd.merge(bb5m_df, open_data_df, left_on='formatted_date', right_on='date', how='left')

# Apply the cutoff date filter to limit data to the last two years
merged_df = merged_df[merged_df['formatted_date'] >= cutoff_date]

# Filter the data for the upper and lower Bollinger Band criteria
ubb_df = merged_df[(merged_df['time'] == '09:30:00') & (merged_df['open'] > merged_df['bollinger_band_upper'])]
lbb_df = merged_df[(merged_df['time'] == '09:30:00') & (merged_df['open'] < merged_df['bollinger_band_lower'])]

# Format the date and create a single string of dates separated by commas
ubb_dates = ','.join(ubb_df['formatted_date'].dt.strftime('%Y-%m-%d').tolist())
lbb_dates = ','.join(lbb_df['formatted_date'].dt.strftime('%Y-%m-%d').tolist())

# Save the formatted date strings to text files
with open('data/result_ubb.txt', 'w') as f:
    f.write(ubb_dates)

with open('data/result_lbb.txt', 'w') as f:
    f.write(lbb_dates)

print("Filtered dates within the last two years saved to result_ubb.txt and result_lbb.txt")
