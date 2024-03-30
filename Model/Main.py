import Data as data
import Monte_carlo_simulation as mcs
import pandas as pd
import time

def main():
    tickers1 = ["AAPL", "MSFT", "AMZN"]
    tickers2 = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    "V", "JNJ"]
    # data.create_csv_data(tickers1, "test_stock_data11.csv")
    # data.create_csv_data(tickers1, "test_stock_data12.csv")
    # data.create_csv_data(tickers2, "test_stock_data2.csv")
    daily_returns1 = pd.read_csv('test_stock_data11.csv', index_col=0)
    daily_returns2 = pd.read_csv('test_stock_data12.csv', index_col=0)
    # daily_returns2 = pd.read_csv('test_stock_data2.csv', index_col=0)
    print("Simulation1:")
    print("Number of companies:", len(tickers1))
    mcs.run_monte_carlo_simulation(daily_returns1)
    # print("Simulation2:")
    # mcs.run_monte_carlo_simulation(daily_returns2)

if __name__ == "__main__":
    main()