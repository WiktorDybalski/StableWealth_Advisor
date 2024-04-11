import pandas as pd
import yfinance as yf

def get_ticker_symbols():
    return ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    "V", "JNJ", "WMT", "BABA", "NVDA", "JPM", "UNH", "HD",
    "PG", "DIS", "MA", "NFLX", "XOM", "IBM", "PYPL",
    "INTC", "CSCO", "PFE", "KO", "PEP", "BA", "ORCL", "ABBV",
    "MRK", "VZ", "COST", "NKE", "LLY", "MCD", "GILD", "F",
    "CVX", "BAC", "WFC", "C", "SCHW", "GS", "MS", "BLK",
    "AMGN", "MO", "PM", "GE", "HON"]

def create_csv_data(tickers, file_name):
    merged_df = pd.DataFrame()

    for ticker in tickers:
        # Fetch historical data for the ticker
        tickerData = yf.Ticker(ticker)
        data = tickerData.history(period='1d', start='1974-01-01')

        close_prices = data[['Close']].rename(columns={'Close': ticker})

        if merged_df.empty:
            merged_df = close_prices
        else:
            merged_df = merged_df.join(close_prices, how='outer')
    merged_df.to_csv(file_name)

if __name__ == "__main__":
    pass

