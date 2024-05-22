from PySide6.QtWidgets import QApplication
import sys
from Controllers import SharesAssistantController
from Controllers import StockInformationController
from Controllers import CalculatorController
from Model.ScipySimulation import Simulation
from Model.TreasuryBondCalculator import TreasuryBondCalculator
from Model.StockInformationCalculation import StockInformationCalculation
from GUI import Home
from Utils import Utils
from Model.UpdateData import UpdateData


def main():
    file_path = Utils.get_absolute_file_path("stock_data_without_polish.csv")
    daily_returns_path = UpdateData.update_data(file_path)

    sa_model = Simulation()
    si_model = StockInformationCalculation()
    calc_model = TreasuryBondCalculator()

    si_model.create_day_data()
    si_model.create_month_data()
    si_model.create_year_data()

    app = QApplication(sys.argv)
    view = Home.HomeWindow(app)

    sa_controller = SharesAssistantController.Controller(view, sa_model, daily_returns_path)
    si_controller = StockInformationController.StockInformationController(view, si_model, daily_returns_path)
    calc_controller = CalculatorController.BondController(view, calc_model)

    sa_model.set_controller(sa_controller)
    si_model.set_controller(si_controller)
    calc_model.set_controller(calc_controller)

    view.set_sa_controller(sa_controller)
    view.set_si_controller(si_controller)
    view.set_calc_controller(calc_controller)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
