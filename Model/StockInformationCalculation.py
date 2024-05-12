from datetime import timedelta
import csv
import pandas as pd
import datetime

from Configurators.StockInformationConfigurator import StockInformationConfigurator as config
from Utils import Utils


class StockInformationCalculation:
    def __init__(self):
        self.config = config()
        self.controller = None
        self.data = pd.read_csv(Utils.get_absolute_file_path("stock_data_without_polish.csv"))
        #self.create_day_data()

    def set_controller(self, controller):
        self.controller = controller

    def create_day_data(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        df_last_two_rows = self.data.tail(2)

        daily_difference = df_last_two_rows.set_index('Date').diff().tail(1)
        daily_difference.reset_index(inplace=True)

        # najlepiej by zwracalo obecny dzien i pod nim % zmiane
        result = pd.concat([df_last_two_rows.head(2), daily_difference])
        # print(result)
        # print(type(result))

        df = pd.DataFrame(result)
        diff = df.diff().iloc[1]

        # percentage_diff = (df.iloc[-1] - df.iloc[-2]) / df.iloc[-2] * 100  # Percentage difference

        final_result = []

        for col in df.columns[1:]:  # Exclude the 'Date' column
            ticker = col
            today_value = df[col].iloc[0]
            difference = diff[col]
            #percentage_difference = percentage_diff[col]
            yesterday_value = df[col].iloc[-2]
            if yesterday_value != 0:
                percentage_difference = (difference / yesterday_value) * 100
            else:
                percentage_difference = float('inf') if difference > 0 else float('-inf')
            final_result.append((ticker, today_value, difference, percentage_difference))

        #print(final_result)

        self.config.companies_day = final_result

        return final_result

    def create_month_data(self):
        print("Calculating month data")
        df = self.data
        # Select the last recorded day's prices
        last_day_prices = df.iloc[-1, 1:]

        # Select the prices of the last 21 days (excluding the last recorded day)
        last_21_days_prices = df.iloc[-22:-1, 1:]

        # Calculate the average of the last 21 days' prices
        avg_last_21_days = last_21_days_prices.mean()

        # Create a list to store tuples for each stock
        result = []

        # Iterate over each column (ticker symbol)
        for column in df.columns[1:]:
            today_value = last_day_prices[column]
            avg_last_21_value = avg_last_21_days[column]
            diff = today_value - avg_last_21_value
            percentage_diff = ((today_value - avg_last_21_value) / avg_last_21_value) * 100

            # Append the tuple to the result list
            result.append((column, today_value, diff, percentage_diff))

        self.config.companies_month = result
        #print(result)
        return result

    def create_year_data(self):
        print("Calculating year data")
        df = self.data
        # Select the last recorded day's prices
        last_day_prices = df.iloc[-1, 1:]

        # Select the prices of the last 255 days (excluding the last recorded day)
        last_252_days_prices = df.iloc[-253:-1, 1:]

        # Calculate the average of the last 255 days' prices
        avg_last_252_days = last_252_days_prices.mean()

        # Create a list to store tuples for each stock
        result = []

        # Iterate over each column (ticker symbol)
        for column in df.columns[1:]:
            today_value = last_day_prices[column]
            avg_last_252_value = avg_last_252_days[column]
            diff = today_value - avg_last_252_value
            percentage_diff = ((today_value - avg_last_252_value) / avg_last_252_value) * 100

            # Append the tuple to the result list
            result.append((column, today_value, diff, percentage_diff))

        #print(result)
        self.config.companies_year = result
        return result

    def get_last_date(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            last_line = file.readlines()[-1].strip().split(',')
            date_time = last_line[0]
        last_day = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S%z").date()
        return last_day


if __name__ == "__main__":
    stock_calc = StockInformationCalculation()
    # daily_data = stock_calc.create_day_data()
    # monthly_data = stock_calc.create_month_data()
    # yearly_data = stock_calc.create_year_data()