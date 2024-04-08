import pandas as pd
from Model.companies import Companies as comp


class Controller:
    def __init__(self, view, model, data):
        self.data = data
        self.view = view
        self.model = model
    def get_tickers(self, companies_list):
        companies_obj = comp()
        tickers = []
        for company in companies_list:
            for ticker, name in companies_obj.companies.items():
                if name == company:
                    tickers.append(ticker)
                    break
        return tickers

    def select_columns_from_csv(self, csv_file, columns):
        df = pd.read_csv(csv_file)
        selected_columns = df[columns]
        return selected_columns

    def calculate(self, companies_list):
        tickers = self.get_tickers(companies_list)

    def runSimulation(self, data):
        self.model.runSimulation(data)
        results = self.model.getResults()
        self.view.displayResults(results)
