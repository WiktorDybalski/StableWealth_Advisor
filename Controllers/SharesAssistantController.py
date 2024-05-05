import pandas as pd
from Data.Companies import Companies as comp
from Configurators.SharesAssistantConfigurator import SharesAssistantConfigurator as config

class Controller:
    def __init__(self, view, model, path_data):
        self.path_data = path_data
        self.data = pd.read_csv(path_data, index_col=0)
        self.view = view
        self.model = model
        self. config = config()


    def get_tickers(self):
        companies_obj = comp()
        tickers = []
        for company in self.config.companies:
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
        if not self.config.desired_return_min and not self.config.desired_return_max and not self.config.desired_risk_min and not self.config.desired_risk_max:
            self.model.run_scipy_simulation(results)
        elif self.config.desired_risk_min is not None and self.config.desired_risk_max is not None:
            self.model.run_scipy_simulation(results, None, None, self.config.desired_risk_min, self.config.desired_risk_max)
        elif self.config.desired_return_min is not None and self.config.desired_return_min is not None:
            self.model.run_scipy_simulation(results, self.config.desired_return_min, self.config.desired_return_max)
        print("Simulation done")

    def show_data_in_GUI(self):
        self.view.show_shares_assistant_results()

