from Configurators.CalculatorConfigurator import CalculatorConfigurator as config

class BondController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.config = config()

    def run_calculation(self):
        self.model.bond_result([
            self.config.bond_type,
            self.config.number_of_bonds,
            self.config.curr_inflation,
            self.config.period,
            self.config.NBP
        ])
