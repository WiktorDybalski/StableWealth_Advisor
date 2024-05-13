import csv
import datetime
import os
import pandas as pd
import yfinance as yf

from Utils import Utils

# TODO
# Add data_validation  - DONE
# Fix UpdateData class

class UpdateData:
    @staticmethod
    def is_already_updated(stock_data_path):
        last_day = UpdateData.get_last_date(stock_data_path)
        return last_day >= datetime.date.today() - datetime.timedelta(days=1)

    @staticmethod
    def update_data(stock_data_path):
        if UpdateData.is_already_updated(stock_data_path):
            print("Data is already updated today.")
            return stock_data_path
        new_stock_data_path = Utils.get_absolute_file_path("new_stock_data.csv")
        last_day = UpdateData.get_last_date(stock_data_path)

        next_day_string = (last_day + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        UpdateData.create_csv_data_with_start(UpdateData.get_ticker_symbols_without_polish(), new_stock_data_path,
                                              next_day_string)

        new_last_day = UpdateData.get_last_date(new_stock_data_path)
        if last_day < new_last_day:
            UpdateData.update_csv_file(stock_data_path, new_stock_data_path)
        print("Data file updated with new data.")
        return stock_data_path

    @staticmethod
    def get_last_date(file_path):
        with open(file_path, 'r') as file:
            last_line = file.readlines()[-1].strip().split(',')
            date_time = last_line[0]
        last_day = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S%z").date()
        return last_day

    # Nie potrzebna
    @staticmethod
    def get_last_update_date(file_path):
        with open(file_path, 'r') as file:
            last_line = file.readlines()[-1].strip()
        return datetime.datetime.strptime(last_line, '%Y-%m-%d').date()

    @staticmethod
    def update_csv_file(old_data_file, new_data_file):
        df_old = pd.read_csv(old_data_file)
        df_new = pd.read_csv(new_data_file)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.to_csv(old_data_file, index=False)

    @staticmethod
    def get_reduced_ticker_symbols_without_polish():
        # 40 companies
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "BRK-A", "TSLA", "UNH", "JNJ", "V", "NVDA",
            "XOM", "TSM", "WMT", "META", "PG", "LLY", "HD", "CVX", "KO",
            "PFE", "ABBV", "MRK", "PEP", "TMO", "ORCL", "COST", "AZN", "RIL",
            "MCD", "CSCO", "TMUS", "SHEL", "DIS", "DHR", "TM", "NVS", "ABT"
        ]

    @staticmethod
    def get_reduced_ticker_symbols():
        # 50 companies
        return [
            "PKN.WA", "PKO.WA", "SAN.WA", "DNP.WA", "PZU.WA", "LPP.WA", "KGH.WA", "MBK.WA", "PGE.WA",
            "AAPL", "MSFT", "GOOGL", "AMZN", "BRK-A", "TSLA", "UNH", "JNJ", "V", "NVDA",
            "XOM", "TSM", "WMT", "META", "PG", "LLY", "HD", "CVX", "KO",
            "PFE", "ABBV", "MRK", "PEP", "TMO", "ORCL", "COST", "AZN", "RIL",
            "MCD", "CSCO", "TMUS", "SHEL", "DIS", "DHR", "TM", "NVS", "ABT"
        ]

    @staticmethod
    def get_ticker_symbols_without_polish():
        # 90 companies
        return ["AAPL", "MSFT", "GOOGL", "AMZN", "BRK-A", "TSLA", "UNH", "JNJ", "V", "NVDA",
                "XOM", "TSM", "WMT", "META", "PG", "LLY", "HD", "CVX", "KO",
                "PFE", "ABBV", "MRK", "PEP", "TMO", "ORCL", "COST", "AZN",
                "MCD", "CSCO", "TMUS", "SHEL", "DIS", "DHR", "TM", "NVS", "ABT",
                "ACN", "VZ", "TXN", "BHP", "WFC", "LIN", "MS", "INTC", "CMCSA", "ADBE",
                "SAP", "UPS", "TTE", "IBM", "HSBC", "AMGN", "LOW", "C", "BABA", "RTX",
                "SBUX", "BMY", "GE", "NKE", "CVS", "SNY", "T", "AMD", "NFLX", "UNP",
                "MDT", "GSK", "BA", "HON", "QCOM", "SIEGY", "UL", "DE", "BLK", "GS",
                "MMM", "F", "ISNPY", "CRWD", "CARR", "AMAT", "MO", "COP", "PM", "LMT"
                ]

    @staticmethod
    def get_ticker_symbols():
        # 100 companies
        return [
            "PKN.WA", "PKO.WA", "SAN.WA", "DNP.WA", "PZU.WA", "LPP.WA", "KGH.WA", "MBK.WA", "PGE.WA",
            "AAPL", "MSFT", "GOOGL", "AMZN", "BRK-A", "TSLA", "UNH", "JNJ", "V", "NVDA",
            "XOM", "TSM", "WMT", "META", "PG", "LLY", "HD", "CVX", "KO",
            "PFE", "ABBV", "MRK", "PEP", "TMO", "ORCL", "COST", "AZN", "RIL",
            "MCD", "CSCO", "TMUS", "SHEL", "DIS", "DHR", "TM", "NVS", "ABT",
            "ACN", "VZ", "TXN", "BHP", "WFC", "LIN", "MS", "INTC", "CMCSA", "ADBE",
            "SAP", "UPS", "TTE", "IBM", "HSBC", "AMGN", "LOW", "C", "BABA", "RTX",
            "SBUX", "BMY", "GE", "NKE", "CVS", "SNY", "T", "AMD", "NFLX", "UNP",
            "MDT", "GSK", "BA", "HON", "QCOM", "SIEGY", "UL", "DE", "BLK", "GS",
            "MMM", "F", "ISNPY", "CRWD", "CARR", "AMAT", "MO", "COP", "PM", "LMT"
        ]

    @staticmethod
    def create_csv_data_with_start(tickers, file_name, start_time):
        merged_df = pd.DataFrame()

        for ticker in tickers:
            # Fetch historical data for the ticker
            ticker_data = yf.Ticker(ticker)
            data = ticker_data.history(period='1d', start=start_time)

            close_prices = data[['Close']].rename(columns={'Close': ticker})

            if merged_df.empty:
                merged_df = close_prices
            else:
                merged_df = merged_df.join(close_prices, how='outer')
        merged_df.to_csv(file_name)

    @staticmethod
    def create_csv_data(tickers, file_name):
        merged_df = pd.DataFrame()

        for ticker in tickers:
            # Fetch historical data for the ticker
            ticker_data = yf.Ticker(ticker)
            data = ticker_data.history(period='1d', start='1974-01-01')

            close_prices = data[['Close']].rename(columns={'Close': ticker})

            if merged_df.empty:
                merged_df = close_prices
            else:
                merged_df = merged_df.join(close_prices, how='outer')
        merged_df.to_csv(file_name)


if __name__ == "__main__":
    pass
    # UpdateData.create_csv_data(UpdateData.get_ticker_symbols(), "../Data/stock_data.csv")
    # UpdateData.create_csv_data(UpdateData.get_reduced_ticker_symbols(), "../Data/stock_data_reduced.csv")
    # UpdateData.create_csv_data(UpdateData.get_ticker_symbols_without_polish(), "../Data/stock_data_without_polish.csv")
    # UpdateData.create_csv_data(UpdateData.get_reduced_ticker_symbols_without_polish(),"../Data/stock_data_without_polish_reduced.csv")