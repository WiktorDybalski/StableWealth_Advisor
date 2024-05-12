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
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        df_last_two_rows = self.data.tail(22)
        print(df_last_two_rows)
        result = []
        # daily_difference = df_last_two_rows.set_index('Date').diff().tail(1)
        # daily_difference.reset_index(inplace=True)
        #
        # # najlepiej by zwracalo obecny dzien i pod nim % zmiane
        # result = pd.concat([df_last_two_rows.head(2), daily_difference])
        # print(result)
        # print(type(result))
        #
        #
        # # 42 trading days for two months
        # df_last_42_rows = self.data.tail(42)
        # monthly_difference = df_last_42_rows.set_index('Date').diff().tail(1)
        # monthly_difference.reset_index(inplace=True)
        #
        # result = pd.concat([df_last_42_rows.head(1), monthly_difference])
        # result['Percent Change'] = (result['Close'].pct_change() * 100).round(2)
        # print(result)
        return result

    def create_year_data(self):
        # 504 trading days for two years
        df_last_504_rows = self.data.tail(504)
        yearly_difference = df_last_504_rows.set_index('Date').diff().tail(1)
        yearly_difference.reset_index(inplace=True)

        result = pd.concat([df_last_504_rows.head(1), yearly_difference])
        result['Percent Change'] = (result['Close'].pct_change() * 100).round(2)
        print(result)
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
    #daily_data = stock_calc.create_day_data()
    monthly_data = stock_calc.create_month_data()
    # yearly_data = stock_calc.create_year_data()