from datetime import timedelta

import pandas as pd

from Configurators.StockInformationConfigurator import StockInformationConfigurator as config
from Utils import Utils


class StockInformationCalculation:
    def __init__(self):
        self.config = config()
        self.data = pd.read_csv(Utils.get_absolute_file_path("stock_data_without_polish.csv"))

    def create_day_data(self):
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        df_last_two_rows = self.data.tail(2)

        daily_difference = df_last_two_rows.set_index('Date').diff().tail(1)
        daily_difference.reset_index(inplace=True)

        # najlepiej by zwracalo obecny dzien i pod nim % zmiane
        result = pd.concat([df_last_two_rows.head(2), daily_difference])
        print(result)
        return result

    def create_month_data(self):
        # 42 trading days for two months
        df_last_42_rows = self.data.tail(42)
        monthly_difference = df_last_42_rows.set_index('Date').diff().tail(1)
        monthly_difference.reset_index(inplace=True)

        result = pd.concat([df_last_42_rows.head(1), monthly_difference])
        result['Percent Change'] = (result['Close'].pct_change() * 100).round(2)
        print(result)
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

if __name__ == "__main__":
    stock_calc = StockInformationCalculation()
    daily_data = stock_calc.create_day_data()
    # monthly_data = stock_calc.create_month_data()
    # yearly_data = stock_calc.create_year_data()