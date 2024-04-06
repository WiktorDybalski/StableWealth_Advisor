from PyQt5.QtWidgets import QApplication
import pandas as pd
import sys
from Controllers import Controller
from Model import Scipy_simulation
from GUI import Home_GUI

def main():
    # tickers1 = ["AAPL", "MSFT", "AMZN"]
    # tickers2 = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA",
    # "V", "JNJ"]
    # # data.create_csv_data(tickers1, "test_stock_data11.csv")
    # # data.create_csv_data(tickers1, "test_stock_data12.csv")
    # # data.create_csv_data(tickers2, "test_stock_data2.csv")
    # daily_returns1 = pd.read_csv('test_stock_data11.csv', index_col=0)
    # daily_returns2 = pd.read_csv('test_stock_data12.csv', index_col=0)
    # daily_returns3 = pd.read_csv('stock_data.csv', index_col=0)
    # # daily_returns2 = pd.read_csv('test_stock_data2.csv', index_col=0)
    # print("Simulation1:")
    # print("Number of companies:", len(tickers1))
    # mcs.run_monte_carlo_simulation(daily_returns1)
    #
    # print("Simulation2:")
    # print("Number of companies:", len(tickers1))
    # start = datetime.now()
    # Sci_sim.run_scipy_simulation(daily_returns3)
    # end = datetime.now()
    # print(end - start)

    app = QApplication(sys.argv)
    view = Home_GUI.HomeWindow(app)
    view.show()

    model = Scipy_simulation.simulation
    daily_returns1 = pd.read_csv('test_stock_data11.csv', index_col=0)
    controller_instance = Controller.Controller(view, model, daily_returns1)
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()