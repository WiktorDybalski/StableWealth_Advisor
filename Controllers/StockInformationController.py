from Configurators.StockInformationConfigurator import StockInformationConfigurator as config


class StockInformationController:
    def __init__(self, view, model, path_data):
        self.path_data = path_data
        self.config = config("Day")
        self.model = model
        self.view = view

    def get_companies_names(self):
        pass

    def create_data(self):
        period = self.config.period

        if period == "Day":
            self.model.create_day_data()
            print(self.config.companies_day)
        elif period == "Month":
            self.model.create_month_data()
            print(self.config.companies_month)
        else:
            self.model.create_year_data()
            print(self.config.companies_year)
