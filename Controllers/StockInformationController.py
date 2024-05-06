from Configurators.StockInformationConfigurator import StockInformationConfigurator as config
class StockInformationController:
    def __init__(self, model, view):
        self.config = config("day")
        self.model = model
        self.view = view

    def create_data(self):
        period = self.config.period
        if period == "day":
            model.create_day_data()
        elif period == "month":
            model.create_month_data()
        else:
            model.create_year_data()