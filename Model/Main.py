import Data as data
import Monte_carlo_simulation as mcs
import pandas as pd


def main():
    tickers1 = ["AAPL", "MSFT", "AMZN"]
    tickers2 = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    "V", "JNJ"]
    data.create_csv_data(tickers1, "test_stock_data1.csv")
    data.create_csv_data(tickers2, "test_stock_data2.csv")
    daily_returns1 = pd.read_csv('test_stock_data1.csv', index_col=0)
    # daily_returns2 = pd.read_csv('stock_data.csv', index_col=0)
    mcs.run_monte_carlo_simulation(daily_returns1)
    # mcs.run_monte_carlo_simulation(daily_return2)

if __name__ == "__main__":
    main()