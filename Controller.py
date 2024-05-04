import pandas as pd
from Data.Companies import Companies as comp
from Model.ScipySimulation import Simulation

class Controller:
    def __init__(self, view, model, path_data):
        self.path_data = path_data
        self.data = pd.read_csv(path_data, index_col=0)
        self.view = view
        self.model = model
        self.companies_list = []

    def set_companies_list(self, companies):
        self.companies_list = companies
    def get_tickers(self):
        companies_obj = comp()
        tickers = []
        for company in self.companies_list:
            for ticker, name in companies_obj.companies.items():
                if name == company:
                    tickers.append(ticker)
                    break
        return tickers

    def select_columns_from_csv(self, csv_file, columns):
        df = pd.read_csv(csv_file)
        selected_columns = df[columns]
        return selected_columns

    def run_simulation(self):
        tickers_list = self.get_tickers()
        print(tickers_list)
        results = self.select_columns_from_csv(self.path_data, tickers_list)
        print("Simulation running")
        self.model.run_standard_scipy_simulation(results)

    def show_data_in_GUI(self, companies_list, optimal_weights, tab):
        self.view.show_shares_assistant_results(companies_list, optimal_weights, tab)

