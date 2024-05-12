import csv
import datetime
import os
import pandas as pd
import yfinance as yf

from Utils import Utils

# TODO
# Add data_validation
# Fix UpdateData class

class UpdateData:
    @staticmethod
    def is_already_updated():
        file_path = Utils.get_absolute_file_path("recently_updated_day.txt")
        if not os.path.exists(file_path):
            return False
        with open(file_path, 'r') as file:
            last_line = file.readlines()[-1].strip()
        last_update_date = datetime.datetime.strptime(last_line, '%Y-%m-%d').date()
        return last_update_date >= datetime.date.today() - datetime.timedelta(days=1)

    @staticmethod
    def update_data(stock_data_path):
        if UpdateData.is_already_updated():
            print("Data is already updated today.")
            return stock_data_path

        today = datetime.date.today()
        # print(today)
        file_path = Utils.get_absolute_file_path("recently_updated_day.txt")
        # = Utils.get_absolute_file_path("new_stock_data_reduced.csv")
        # dodane do Utilsów nowe csv
        new_stock_data_path = Utils.get_absolute_file_path("new_stock_data.csv")
        last_date = UpdateData.get_last_update_date(file_path)

        next_day_string = (last_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        print(next_day_string)
        # UpdateData.create_csv_data_with_start(UpdateData.get_reduced_ticker_symbols_without_polish(), new_stock_data_path,next_day_string)
        UpdateData.create_csv_data_with_start(UpdateData.get_ticker_symbols_without_polish(), new_stock_data_path,
                                              next_day_string)
        #print("new_stock_data.csv")
        UpdateData.update_csv_file(stock_data_path, new_stock_data_path)

        with open(file_path, 'a') as file:
            file.write(today.strftime('%Y-%m-%d') + '\n')
        print("Data file updated with new data.")
        return stock_data_path

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

    def remove_last_n_rows(self, input_csv_path, output_csv_path, n):
        # Czytamy wszystkie wiersze z pliku CSV
        with open(input_csv_path, newline='', encoding='utf-8') as csv_file:
            rows = list(csv.reader(csv_file))

        # Usuwamy n ostatnich wierszy
        if n < len(rows):
            rows = rows[:-n]
        else:
            rows = rows[:1]  # Zachowujemy tylko nagłówki, jeśli n >= liczba wierszy

        # Zapisujemy zmodyfikowane dane do nowego pliku CSV
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

    def remove_empty_rows_except_date(self, input_csv_path, output_csv_path, date_column="Date"):
        # Wczytujemy dane z pliku CSV
        df = pd.read_csv(input_csv_path)

        # Wypełniamy puste wartości w kolumnie `date_column`
        df[date_column] = df[date_column].fillna("Missing Date")

        # Usuwamy wiersze z pustymi wartościami, z wyjątkiem kolumny `date_column`
        df_cleaned = df.dropna(how='any', subset=[col for col in df.columns if col != date_column])

        # Zapisujemy oczyszczone dane do nowego pliku CSV
        df_cleaned.to_csv(output_csv_path, index=False)


if __name__ == "__main__":
    pass
    # UpdateData.create_csv_data(UpdateData.get_ticker_symbols(), "../Data/stock_data.csv")
    # UpdateData.create_csv_data(UpdateData.get_reduced_ticker_symbols(), "../Data/stock_data_reduced.csv")
    # UpdateData.create_csv_data(UpdateData.get_ticker_symbols_without_polish(), "../Data/stock_data_without_polish.csv")
    # UpdateData.create_csv_data(UpdateData.get_reduced_ticker_symbols_without_polish(),"../Data/stock_data_without_polish_reduced.csv")

    # UpdateData.update_data("../Data/stock_data_without_polish_reduced.csv")
    #UpdateData.update_data("../Data/stock_data_without_polish.csv")
    # RIL USUNIETATY TYLKO Z stock_data_without_polish