import pandas as pd

# Load bb5m.csv and open_data.csv
bb5m_df = pd.read_csv('data/bb5m.csv')
open_data_df = pd.read_csv('data/open_data.csv')

# Convert the 'formatted_date' column to datetime format
bb5m_df['formatted_date'] = pd.to_datetime(bb5m_df['formatted_date'], format='%m/%d/%Y')
open_data_df['date'] = pd.to_datetime(open_data_df['date'], format='%d/%m/%Y')

# Merge the DataFrames on 'formatted_date'
merged_df = pd.merge(bb5m_df, open_data_df, left_on='formatted_date', right_on='date', how='left')

# Filter the data for the upper and lower Bollinger Band criteria
ubb_df = merged_df[(merged_df['time'] == '09:30:00') & (merged_df['open'] > merged_df['bollinger_band_upper'])]
lbb_df = merged_df[(merged_df['time'] == '09:30:00') & (merged_df['open'] < merged_df['bollinger_band_lower'])]

# Create a copy to modify without warnings
ubb_result = ubb_df[['formatted_date', 'bollinger_band_upper']].copy()
ubb_result.loc[:, 'formatted_date'] = ubb_result['formatted_date'].dt.strftime('%Y-%m-%d')

lbb_result = lbb_df[['formatted_date', 'bollinger_band_lower']].copy()
lbb_result.loc[:, 'formatted_date'] = lbb_result['formatted_date'].dt.strftime('%Y-%m-%d')

# Save the filtered data to two different CSV files
ubb_result.to_csv('data/result_ubb.csv', index=False, float_format='%.2f')
lbb_result.to_csv('data/result_lbb.csv', index=False, float_format='%.2f')

print("Filtered data saved to result_ubb.csv and result_lbb.csv")
