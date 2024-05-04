import os
import numpy as np
import pandas

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
        optimal_weights, metrics = self.run_standard_scipy_simulation(selected_df)
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

    def run_standard_scipy_simulation(self, daily_returns):
        number_of_companies = daily_returns.shape[1]
        tickers = [daily_returns.columns[i] for i in range(number_of_companies)]
        companies_list = [Companies.get_companies_without_polish().get(ticker) for ticker in tickers]
        log_ret = np.log(daily_returns / daily_returns.shift(1))

        log_mean = log_ret.mean() * 252
        cov = log_ret.cov() * 252

        def get_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = log_mean.dot(weights)
            vol = np.sqrt(weights.T.dot(cov.dot(weights)))
            sr = ret / vol
            return np.array([ret, vol, sr])

        # Negate Sharpe ratio as we need to max it but Scipy minimize the given function
        def neg_sr(weights):
            return get_ret_vol_sr(weights)[-1] * -1

        # check sum of weights
        def check_sum(weights):
            return np.sum(weights) - 1

        # Constraints for the optimization problem
        cons = {'type': 'eq', 'fun': check_sum}
        # bounds on weights
        # bounds = ((0, 1), (0, 1), (0, 1), (0, 1))
        bounds = ((0, 1) for _ in range(number_of_companies))
        # initial guess for optimization to start with
        init_guess = [.25 for _ in range(number_of_companies)]

        # Call minimizer
        opt_results = optimize.minimize(neg_sr, init_guess, constraints=cons, bounds=bounds, method='SLSQP')
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
        return optimal_weights, tab

    def send_data_to_controller(self, companies_list, optimal_weights, tab):
        self.controller.show_data_in_GUI(companies_list, optimal_weights, tab)


if __name__ == "__main__":
    simulation = Simulation()
    print(simulation.run_best_of_three(Utils.get_absolute_file_path("stock_data_without_polish.csv")))
