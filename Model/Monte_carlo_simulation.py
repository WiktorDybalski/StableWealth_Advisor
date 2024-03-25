import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import Data as data

def run_monte_carlo_simulation(daily_returns):
    number_of_companies = daily_returns.shape[1]
    """
    Normalizujemy każdą komórke w DataFrame uzyskując w pierwszym wierszu DataFrame wartosc 100, a w kolejnych komórkach
    jej procentowy przyrost od wartosci 100 np 124 co oznacza wzrost na poziomie 24% od wartosci początkowej
    """
    fig = px.line(daily_returns * 100 / daily_returns.iloc[0])
    # fig.show()

    """
    Korzystamy z funkcji pct_change z biblioteki Pandas tworząc nowy DataFrame zmian cen akcji każdego dnia w stosunku
    do dnia poprzedniego

    df.pct_change() - (wartość bieżąca - poprzednia wartość) / poprzednia wartość
    """
    df_of_changes = daily_returns.pct_change()

    fig_of_changes = px.line(df_of_changes)
    # fig_of_changes.show()

    # -----------------------------------------------------
    # Monte Carlo Simulation
    np.random.seed()
    weights = np.random.random((number_of_companies, 1))
    weights /= np.sum(weights)
    # print(f'Normalized Weights : {weights.flatten()}')

    log_ret = np.log(daily_returns / daily_returns.shift(1))

    n = 50000

    port_weights = np.zeros(shape=(n, len(daily_returns.columns)))
    port_volatility = np.zeros(n)
    port_sr = np.zeros(n)
    port_return = np.zeros(n)

    for i in range(n):
        weights = np.random.random(number_of_companies)
        weights /= np.sum(weights)
        port_weights[i, :] = weights

        # Profit
        exp_ret = log_ret.mean().dot(weights) * 252
        port_return[i] = exp_ret

        # Exp Volatility (Risk)
        exp_vol = np.sqrt(weights.T.dot(252 * log_ret.cov().dot(weights)))
        port_volatility[i] = exp_vol

        # Sharpe ratio
        sr = exp_ret / exp_vol
        port_sr[i] = sr

    # Index of max Sharpe Ratio
    max_sr = port_sr.max()
    ind = port_sr.argmax()
    # Return and Volatility at Max SR
    max_sr_ret = port_return[ind]
    max_sr_vol = port_volatility[ind]
    # Visualization
    plt.figure(figsize=(15, 10))
    plt.scatter(port_volatility, port_return, c=port_sr, cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility', fontsize=15)
    plt.ylabel('Profit', fontsize=15)
    plt.title('Efficient Frontier (Bullet Plot)', fontsize=15)
    plt.scatter(max_sr_vol, max_sr_ret, c='white', s=100, edgecolors='red', marker='o', label='Max \
    Sharpe ratio Portfolio')
    plt.legend()
    plt.show()

    for weight, stock in zip(port_weights[ind], data.get_ticker_symbols()):
        print(f'{round(weight * 100, 2)} % of {stock} should be bought.')

    # best portfolio return
    print(f'\nMarkowitz optimal portfolio return is : {round(max_sr_ret * 100, 2)}% with volatility \
    {max_sr_vol}')

if __name__ == "__main__":
    pass
