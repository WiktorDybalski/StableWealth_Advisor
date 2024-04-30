from PySide6.QtWidgets import QApplication
import sys
import Controller
from Model.ScipySimulation import Simulation
from GUI import Home
from Utils import Utils
from Model.UpdateData import UpdateData


def main():
    app = QApplication(sys.argv)
    view = Home.HomeWindow(app)
    model = Simulation()
    file_path = Utils.get_absolute_file_path("stock_data_without_polish.csv")
    # We have to load a GUI waiting screen when user has to wait for updating data and change a little bit
    # the update data logic
    daily_returns_path = UpdateData.update_data(file_path)
    controller = Controller.Controller(view, model, daily_returns_path)
    model.set_controller(controller)
    view.set_controller(controller)
    view.show()
    print("Działa")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()