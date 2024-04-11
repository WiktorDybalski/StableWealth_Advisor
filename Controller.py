import pandas as pd
from Data.companies import Companies as comp
from Model import Scipy_simulation as Sci_sim
from Utils import Utils

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

    def runSimulation(self, companies_list):
        print("Simulation running")
        tickers_list = self.get_tickers(companies_list)
        print(tickers_list)
        results = self.select_columns_from_csv(Utils.get_absolute_file_path("stock_data.csv"), tickers_list)
        print("Simulation running")
        simulation = Sci_sim.Simulation()
        simulation.run_scipy_simulation(results)
