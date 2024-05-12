from Configurators.StockInformationConfigurator import StockInformationConfigurator as config
from Data.Companies import Companies as comp
class StockInformationController:
    def __init__(self, view, model, path_data):
        self.path_data = path_data
        self.config = config("day")
        self.model = model
        self.view = view

    def get_companies_names(self):
        pass

    def create_data(self):
        period = self.config.period

        # self.model.get_last_day(self.path_data)
        #print(period)
        if period == "day":
            print("creating day data - in controller")
            self.model.create_day_data()
        elif period == "month":
            self.model.create_month_data()
        else:
            self.model.create_year_data()