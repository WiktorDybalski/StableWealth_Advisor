from PySide6.QtWidgets import QApplication
import sys
from Controllers import SharesAssistantController
from Controllers import StockInformationController
from Model.ScipySimulation import Simulation
from Model.StockInformationCalculation import StockInformationCalculation
from GUI import Home
from Utils import Utils
from Model.UpdateData import UpdateData



def main():
    app = QApplication(sys.argv)
    view = Home.HomeWindow(app)

    sa_model = Simulation()
    si_model = StockInformationCalculation()

    file_path = Utils.get_absolute_file_path("stock_data_without_polish.csv")
    daily_returns_path = UpdateData.update_data(file_path)

    sa_controller = SharesAssistantController.Controller(view, sa_model, daily_returns_path)
    si_controller = StockInformationController.StockInformationController(view, si_model, daily_returns_path)

    sa_model.set_controller(sa_controller)
    si_model.set_controller(si_controller)

    view.set_sa_controller(sa_controller)
    view.set_si_controller(si_controller)

    view.show()
    print("Starting Application")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()