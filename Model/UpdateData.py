import datetime
import os

import pandas as pd
import yfinance as yf

from Utils import Utils


class UpdateData:
    @staticmethod
    def is_already_updated():
        if not os.path.exists(Utils.get_absolute_file_path("recently_updated_day.txt")):
            return False
        with open(Utils.get_absolute_file_path("recently_updated_day.txt"), 'r') as recently_updated_file:
            lines = recently_updated_file.readlines()
            line = ""
            if lines:
                line = lines[-1].strip()
            date = datetime.datetime.strptime(line, '%Y-%m-%d').date()
            today = datetime.date.today()
            if today == date:
                return True
        return False

    @staticmethod
    def update_data():
        if UpdateData.is_already_updated():
            return True
        else:
            today = datetime.date.today()
            if not os.path.exists(Utils.get_absolute_file_path("recently_updated_day.txt")):
                with open(Utils.get_absolute_file_path("recently_updated_day.txt"), 'x') as recently_updated_day:
                    recently_updated_day.write(str(today) + '\n')
                    print("Creating file")
            else:
                with open(Utils.get_absolute_file_path("recently_updated_day.txt"), 'a') as recently_updated_file:
                    recently_updated_file.write(str(today) + '\n')
                    print("Updating file")

    @staticmethod
    def update_csv_file(last_app_start):
        pass

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
                "PFE", "ABBV", "MRK", "PEP", "TMO", "ORCL", "COST", "AZN", "RIL",
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
    # UpdateData.create_csv_data(UpdateData.get_reduced_ticker_symbols_without_polish(),
    #                            "../Data/stock_data_without_polish_reduced.csv")
