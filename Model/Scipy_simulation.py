import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from Model import Data as data
import pandas as pd
from scipy import optimize

class Simulation:
    def run_scipy_simulation(self, daily_returns):
        number_of_companies = daily_returns.shape[1]

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
        for st, i in zip(data.get_ticker_symbols(), optimal_weights):
            print(f'Stock {st} has weight {np.round(i * 100, 2)} %')

        print('For a given portfolio we have: (Using SciPy optimizer)\n \n')
        for i, j in enumerate('Return Volatility SharpeRatio'.split()):
            print(f'{j} is : {get_ret_vol_sr(optimal_weights)[i]}\n')




if __name__ == "__main__":
    # daily_returns3 = pd.read_csv('stock_data.csv', index_col=0)
    # print("Simulation1:")
    # simulation.run_scipy_simulation(simulation, daily_returns3)
    pass