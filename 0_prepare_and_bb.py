import pandas as pd
from ta.volatility import BollingerBands

# Load the daily open price CSV file
df_daily = pd.read_csv('sourcedata/spx-1d.csv', sep=';', header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df_daily = df_daily[['date', 'open']]

# Save the open price data
df_daily.to_csv('data/open_data.csv', index=False)

# Load the 5-minute interval data
df_spx = pd.read_csv('sourcedata/spx-5m.csv', sep=';', header=None, names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])

# Combine date and time into a single datetime column
df_spx['datetime'] = pd.to_datetime(df_spx['date'] + ' ' + df_spx['time'], format='%d/%m/%Y %H:%M:%S')
df_spx.set_index('datetime', inplace=True)

# Extract day, month, and year
df_spx['day'] = df_spx.index.day
df_spx['month'] = df_spx.index.month
df_spx['year'] = df_spx.index.year

# Convert the date to MM/DD/YYYY format
df_spx['formatted_date'] = df_spx.index.strftime('%m/%d/%Y')

# Save the transformed data
df_spx.to_csv('data/spx-5m-with-day-month-year.csv', index=False, columns=['formatted_date', 'time', 'open', 'high', 'low', 'close', 'volume', 'day', 'month', 'year'])
print("Data saved to spx-5m-with-day-month-year.csv")

# Calculate Bollinger Bands
df_spx['close'] = pd.to_numeric(df_spx['close'], errors='coerce')
bb_indicator = BollingerBands(close=df_spx['close'], window=20, window_dev=2)
df_spx['bollinger_band_upper'] = bb_indicator.bollinger_hband()

# Save the Bollinger Bands data
df_spx[['formatted_date', 'time', 'close', 'bollinger_band_upper']].to_csv('data/bb5m.csv', index=False)
print("Bollinger Bands calculated and data saved to bb5m.csv")
