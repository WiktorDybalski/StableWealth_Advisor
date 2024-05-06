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

        result = pd.concat([df_last_two_rows.head(1), daily_difference])
        print(result)
        return result

    def create_month_data(self):
        end_date = self.data['Date'].max()
        start_date = end_date - pd.DateOffset(months=2)

        df_last_two_months = self.data[(self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]
        monthly_difference = df_last_two_months.set_index('Date').resample('M').last().diff().tail(1)
        monthly_difference.reset_index(inplace=True)

        result = pd.concat([df_last_two_months.head(1), monthly_difference])
        result['Percent Change'] = (result['Close'].pct_change() * 100).round(2)
        print(result)
        return result

    def create_year_data(self):
        end_date = self.data['Date'].max()
        start_date = end_date - pd.DateOffset(years=2)

        df_last_two_years = self.data[(self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)]
        yearly_difference = df_last_two_years.set_index('Date').resample('Y').last().diff().tail(1)
        yearly_difference.reset_index(inplace=True)

        result = pd.concat([df_last_two_years.head(1), yearly_difference])
        result['Percent Change'] = (result['Close'].pct_change() * 100).round(2)
        print(result)
        return  result

if __name__ == "__main__":
    sic = StockInformationCalculation()