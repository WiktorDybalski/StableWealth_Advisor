import os
import numpy as np
import pandas
from PySide6.QtWidgets import QMessageBox
from matplotlib import pyplot as plt

from Data.Companies import Companies
from Model.UpdateData import UpdateData
from scipy import optimize
import multiprocessing
from Utils import Utils


class Simulation:
    def __init__(self):
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def select_columns_from_csv(self, csv_file, columns):
        df = pandas.read_csv(csv_file)
        selected_columns = df[columns]
        return selected_columns

    def process_combination(self, data, columns):
        selected_df = data.iloc[:, columns]
        optimal_weights, metrics = self.run_scipy_simulation(selected_df)
        return (optimal_weights, metrics, columns)

    def run_best_of_three(self, stock_data_path):
        stock_data = pandas.read_csv(stock_data_path)
        n = stock_data.shape[1]
        max_sr = 0
        best_result = None
        tasks = []
        num_cores = os.cpu_count()
        for i in range(1, n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    tasks.append((stock_data, [i, j, k]))

        with multiprocessing.Pool(processes=num_cores - 1) as pool:
            results = pool.starmap(self.process_combination, tasks)

        for weights, metrics, columns in results:
            if metrics[2] > max_sr:
                max_sr = metrics[2]
                best_result = (weights, metrics, [stock_data.columns[i] for i in columns])

        print(best_result[1], best_result[0], best_result[2])
        return best_result

    def run_best_of_four(self):
        pass

    def run_best_of_five(self):
        pass

    def run_scipy_simulation_with_vol(self, daily_returns, vol):
        pass

    def run_scipy_simulation_with_ret(self, daily_returns, ret):
        pass

    def run_scipy_simulation(self, daily_returns, desired_return, desired_risk):
        # desired_return = 15
        # desired_risk = None
        number_of_companies = daily_returns.shape[1]
        tickers = [daily_returns.columns[i] for i in range(number_of_companies)]
        companies_list = [Companies.get_companies_without_polish().get(ticker) for ticker in tickers]
        log_ret = np.log(daily_returns / daily_returns.shift(1))

        log_mean = log_ret.mean() * 252
        cov = log_ret.cov() * 252

        def get_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = log_mean.dot(weights) * 100
            vol = np.sqrt(weights.T.dot(cov.dot(weights))) * 100
            sr = ret / vol
            return np.array([ret, vol, sr])

        # Negate Sharpe ratio as we need to max it but Scipy minimize the given function
        def neg_sr(weights):
            return get_ret_vol_sr(weights)[-1] * -1

        # check sum of weights
        def check_sum(weights):
            return np.sum(weights) - 1

        # def risk_constraint(weights):
        #     vol = np.sqrt(weights.T.dot(cov.dot(weights))) * 100
        #     return vol - 20  # Ograniczenie, aby ryzyko wynosiło 20%
        #
        # def return_constraint(weights):
        #     ret = log_mean.dot(weights) * 100
        #     return ret - 10  # Ograniczenie, aby zwrot wynosił 10%

        # Constraints for the optimization problem
        cons = [{'type': 'eq', 'fun': check_sum}]
        # # Constraints for the optimization proble
        # if user_constraint_type == 'risk':
        #     cons.append({'type': 'eq', 'fun': risk_constraint}) # meq oznacza funkcja musi zwrocic 0
        # elif user_constraint_type == 'return':
        #     cons.append({'type': 'eq', 'fun': return_constraint})

        if desired_return is not None:
            def return_constraint(weights):
                return get_ret_vol_sr(weights)[0] - desired_return

            cons.append({'type': 'eq', 'fun': return_constraint})

        if desired_risk is not None:
            def risk_constraint(weights):
                return get_ret_vol_sr(weights)[1] - desired_risk

            cons.append({'type': 'eq', 'fun': risk_constraint})



        # bounds on weights
        # bounds = ((0, 1), (0, 1), (0, 1), (0, 1))
        bounds = ((0, 1) for _ in range(number_of_companies))
        # initial guess for optimization to start with
        init_guess = [1. / number_of_companies] * number_of_companies

        # Call minimizer
        opt_results = optimize.minimize(neg_sr, init_guess, method='SLSQP', constraints=cons, bounds=bounds)

        # if no success
        if not opt_results.success:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Simulation failed')
            msg_box.setText('Try changing the value of your desired risk and/or return as in current arrangement it is not possible to reach such value')
            msg_box.setObjectName("msg_box")
            msg_box.exec()

            # tutaj uzytkownik moze wprowadzic inna wartosc
            raise BaseException("Optimization failed: " + opt_results.message)


        optimal_weights = opt_results.x
        # optimal_weights
        ticker_symbols_without_polish = UpdateData.get_ticker_symbols_without_polish()
        for st, i in zip(companies_list, optimal_weights):
            print(f'Stock {st} has weight {np.round(i * 100, 2)} %')

        print('For a given portfolio we have: (Using SciPy optimizer)\n \n')

        tab = []
        for i, j in enumerate('Return Volatility SharpeRatio'.split()):
            print(f'{j} is : {get_ret_vol_sr(optimal_weights)[i]}\n')
            tab.append(get_ret_vol_sr(optimal_weights)[i])
        self.send_data_to_controller(companies_list, optimal_weights, tab)

        def portfolio_performance(weights):
            ret = log_mean.dot(weights) * 100
            vol = np.sqrt(weights.T.dot(cov.dot(weights))) * 100
            return vol, ret

        vols, rets = [], []
        for _ in range(10000):
            weights = np.random.random(number_of_companies)
            weights /= np.sum(weights)
            vol, ret = portfolio_performance(weights)
            vols.append(vol)
            rets.append(ret)

        plt.figure(figsize=(10, 6))
        plt.scatter(vols, rets, c=(np.array(rets) / np.array(vols)), cmap='viridis')
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility (%)')
        plt.ylabel('Return (%)')
        plt.title('Efficient Frontier')
        plt.show()

        return optimal_weights, tab

    def send_data_to_controller(self, companies_list, optimal_weights, tab, desired_return, desired_risk):
        self.controller.show_data_in_GUI(companies_list, optimal_weights, tab, desired_return, desired_risk)


if __name__ == "__main__":


    simulation = Simulation()
    print(simulation.run_best_of_three(Utils.get_absolute_file_path("stock_data_without_polish.csv")))
