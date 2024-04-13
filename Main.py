from PySide6.QtWidgets import QApplication
import pandas as pd
import sys
import Controller
from Model.ScipySimulation import Simulation
from GUI import Home
from Utils import Utils


def main():
    app = QApplication(sys.argv)
    view = Home.HomeWindow(app)
    model = Simulation()
    daily_returns1 = Utils.get_absolute_file_path("stock_data_without_polish.csv")
    controller = Controller.Controller(view, model, daily_returns1)
    model.set_controller(controller)
    view.set_controller(controller)
    view.show()
    print("Działa")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()