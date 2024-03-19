import pandas as pd
import yfinance as yf

tickerSymbols = ['AAPL', 'MSFT', 'AMZN','GOOGL', 'TSLA', 'META', 'V', 'NVDA', 'BABA', 'WMT', 'JPM', 'UNH', 'HD', 'DIS', 'NFLX', 'IBM', 'KO', 'BA', 'MCD', 'BAC', 'BLK', 'F', 'PFE']

merged_df = pd.DataFrame()

for ticker in tickerSymbols:
    # Fetch historical data for the ticker
    tickerData = yf.Ticker(ticker)
    data = tickerData.history(period='1d', start='1974-01-01', end='2024-03-16')

    close_prices = data[['Close']].rename(columns={'Close': ticker})

    if merged_df.empty:
        merged_df = close_prices
    else:
        merged_df = merged_df.join(close_prices, how='outer')


# Save the combined DataFrame to a CSV file
merged_df.to_csv('stock_data.csv')
# Check the first few rows of the combined DataFrame
print(merged_df.head())