from PySide6.QtWidgets import QApplication
import sys
from Controllers import SharesAssistantController
from Model.ScipySimulation import Simulation
from GUI import Home
from Utils import Utils
from Model.UpdateData import UpdateData



def main():
    app = QApplication(sys.argv)
    view = Home.HomeWindow(app)
    sa_model = Simulation()
    file_path = Utils.get_absolute_file_path("stock_data_without_polish.csv")
    daily_returns_path = UpdateData.update_data(file_path)
    sa_controller = SharesAssistantController.Controller(view, sa_model, daily_returns_path)
    sa_model.set_controller(sa_controller)
    view.set_controller(sa_controller)
    view.show()
    print("Starting Application")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()