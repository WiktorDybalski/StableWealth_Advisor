import numpy as np
import pandas
from PySide6.QtWidgets import QMessageBox
from matplotlib import pyplot as plt
from scipy import optimize

from Configurators.SharesAssistantConfigurator import SharesAssistantConfigurator as config
from Data.Companies import Companies


class Simulation:
    def __init__(self):
        self.controller = None
        self.config = config()

    def set_controller(self, controller):
        self.controller = controller

    def select_columns_from_csv(self, csv_file, columns):
        df = pandas.read_csv(csv_file)
        selected_columns = df[columns]
        return selected_columns

    def process_combination(self, data, columns):
        selected_df = data.iloc[:, columns]
        optimal_weights, metrics = self.run_scipy_simulation(selected_df)
        return optimal_weights, metrics, columns

    def run_scipy_simulation(self, daily_returns, desired_return_min=None, desired_return_max=None,
                             desired_risk_min=None, desired_risk_max=None):
        number_of_companies = daily_returns.shape[1]
        tickers = [daily_returns.columns[i] for i in range(number_of_companies)]
        companies_list = [Companies.get_companies_without_polish().get(ticker) for ticker in tickers]
        log_ret = np.log(daily_returns / daily_returns.shift(1))

        log_mean = log_ret.mean() * 252  # number of working days on the stock
        cov = log_ret.cov() * 252

        def get_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = log_mean.dot(weights) * 100
            vol = np.sqrt(weights.T.dot(cov.dot(weights))) * 100
            sr = ret / vol
            return np.array([ret, vol, sr])

        # Negate Sharpe ratio because optimize.minimize finds a minimum not maximum so we have to invert our function
        def neg_sr(weights):
            return get_ret_vol_sr(weights)[-1] * -1

        # check sum of weights
        def check_sum(weights):
            return np.sum(weights) - 1

        # Constraints for the optimization problem
        cons = [{'type': 'eq', 'fun': check_sum}]

        if desired_return_min is not None:
            def return_min_constraint(weights):
                return get_ret_vol_sr(weights)[0] - desired_return_min

            cons.append({'type': 'ineq', 'fun': return_min_constraint})

        if desired_return_max is not None:
            def return_max_constraint(weights):
                return desired_return_max - get_ret_vol_sr(weights)[0]

            cons.append({'type': 'ineq', 'fun': return_max_constraint})

        if desired_risk_min is not None:
            def risk_min_constraint(weights):
                return get_ret_vol_sr(weights)[1] - desired_risk_min

            cons.append({'type': 'ineq', 'fun': risk_min_constraint})

        if desired_risk_max is not None:
            def risk_max_constraint(weights):
                return desired_risk_max - get_ret_vol_sr(weights)[1]

            cons.append({'type': 'ineq', 'fun': risk_max_constraint})

        # bounds on weights
        bounds = ((0, 1) for _ in range(number_of_companies))
        # initial guess for optimization to start with
        init_guess = [1. / number_of_companies] * number_of_companies

        # minimizer
        opt_results = optimize.minimize(neg_sr, init_guess, method='SLSQP', constraints=cons, bounds=bounds)

        # if it was not successful - the desired result cannot be achieved
        if not opt_results.success:
            msg_box = QMessageBox()
            msg_box.setWindowTitle('Simulation failed')
            msg_box.setText(
                'Try changing the value of your desired risk and/or return as in current arrangement it is not possible to reach such value')
            msg_box.setObjectName("msg_box")
            msg_box.exec()

            raise BaseException("Optimization failed: " + opt_results.message)

        optimal_weights = opt_results.x

        results = []
        for i, j in enumerate('Return Volatility SharpeRatio'.split()):
            results.append(get_ret_vol_sr(optimal_weights)[i])

        self.config.companies = companies_list
        self.config.weights = optimal_weights
        self.config.results = results
        self.send_data_to_controller()
        return optimal_weights, results

    def send_data_to_controller(self):
        self.controller.show_data_in_GUI()

    def plot_risk_return_scatter(self, daily_returns):
        log_ret = np.log(daily_returns / daily_returns.shift(1))
        mean_returns = log_ret.mean() * 252
        cov_matrix = log_ret.cov() * 252

        num_portfolios = 10000
        results = np.zeros((3, num_portfolios))
        for i in range(num_portfolios):
            weights = np.random.random(len(mean_returns))
            weights /= np.sum(weights)

            portfolio_return = np.sum(weights * mean_returns) * 100
            portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * 100
            sharpe_ratio = portfolio_return / portfolio_stddev

            results[0, i] = portfolio_return
            results[1, i] = portfolio_stddev
            results[2, i] = sharpe_ratio

        max_sharpe_idx = np.argmax(results[2])
        max_sharpe_return = results[0, max_sharpe_idx]
        max_sharpe_stddev = results[1, max_sharpe_idx]

        plt.figure(figsize=(10, 6))
        plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='YlGnBu', marker='o')
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility (%)')
        plt.ylabel('Return (%)')
        plt.title('Risk-Return Scatter Plot')
        plt.scatter(max_sharpe_stddev, max_sharpe_return, c='red', marker='*', s=100)
        plt.show()

    def plot_efficient_frontier(self, daily_returns, log_mean, cov):
        def portfolio_return(weights):
            return np.sum(weights * log_mean) * 100

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * 100

        def minimize_volatility(weights):
            return portfolio_volatility(weights)

        def efficient_return(target_return):
            cons = (
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                {'type': 'eq', 'fun': lambda w: portfolio_return(w) - target_return}
            )
            result = optimize.minimize(minimize_volatility, [1. / daily_returns.shape[1]] * daily_returns.shape[1],
                                       method='SLSQP', constraints=cons, bounds=[(0, 1)] * daily_returns.shape[1])
            return result.x

if __name__ == "__main__":
    pass
