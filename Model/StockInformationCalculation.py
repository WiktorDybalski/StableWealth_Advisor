import datetime

import pandas as pd

from Configurators.StockInformationConfigurator import StockInformationConfigurator as config
from Model.UpdateData import UpdateData
from Utils import Utils


class StockInformationCalculation:
    def __init__(self):
        self.config = config()
        self.controller = None
        self.data = pd.read_csv(Utils.get_absolute_file_path("stock_data_without_polish.csv"))

    def set_controller(self, controller):
        self.controller = controller

    def create_day_data(self):
        self.config.last_update_time = UpdateData.get_last_date(
            Utils.get_absolute_file_path("stock_data_without_polish.csv"))
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        df_last_two_rows = self.data.tail(2)

        daily_difference = df_last_two_rows.set_index('Date').diff().tail(1)
        daily_difference.reset_index(inplace=True)
        result = pd.concat([df_last_two_rows.head(2), daily_difference])

        df = pd.DataFrame(result)
        diff = df.diff().iloc[1]

        final_result = []

        for col in df.columns[1:]:
            ticker = col
            today_value = df[col].iloc[0]
            difference = diff[col]
            yesterday_value = df[col].iloc[-2]
            if yesterday_value != 0:
                percentage_difference = (difference / yesterday_value) * 100
            else:
                percentage_difference = float('inf') if difference > 0 else float('-inf')
            final_result.append((ticker, today_value, difference, percentage_difference))

        self.config.companies_day = final_result

        return final_result

    def create_month_data(self):
        df = self.data
        last_day_prices = df.iloc[-1, 1:]
        last_21_days_prices = df.iloc[-22:-1, 1:]
        avg_last_21_days = last_21_days_prices.mean()
        result = []
        for column in df.columns[1:]:
            today_value = last_day_prices[column]
            avg_last_21_value = avg_last_21_days[column]
            diff = today_value - avg_last_21_value
            percentage_diff = ((today_value - avg_last_21_value) / avg_last_21_value) * 100
            result.append((column, today_value, diff, percentage_diff))

        self.config.companies_month = result
        return result

    def create_year_data(self):
        df = self.data
        last_day_prices = df.iloc[-1, 1:]
        last_252_days_prices = df.iloc[-253:-1, 1:]
        avg_last_252_days = last_252_days_prices.mean()
        result = []

        for column in df.columns[1:]:
            today_value = last_day_prices[column]
            avg_last_252_value = avg_last_252_days[column]
            diff = today_value - avg_last_252_value
            percentage_diff = ((today_value - avg_last_252_value) / avg_last_252_value) * 100

            result.append((column, today_value, diff, percentage_diff))

        self.config.companies_year = result
        return result

    def get_last_date(self, file_path):
        with open(file_path, 'r') as file:
            last_line = file.readlines()[-1].strip().split(',')
            date_time = last_line[0]
        last_day = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S%z").date()
        return last_day


if __name__ == "__main__":
    pass
