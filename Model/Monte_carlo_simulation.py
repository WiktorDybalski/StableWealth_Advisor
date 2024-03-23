import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import Data as data

def run_monte_carlo_simulation(daily_returns):
    number_of_companies = daily_returns.shape[1]
    print(number_of_companies)
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
    np.random.seed(1)
    # Weight each security
    weights = np.random.random((number_of_companies, 1))
    # normalize it, so that some is one
    weights /= np.sum(weights)
    print(f'Normalized Weights : {weights.flatten()}')

    # We generally do log return instead of return
    log_ret = np.log(daily_returns / daily_returns.shift(1))
    # log_ret

    n = 100
    # n = 10

    port_weights = np.zeros(shape=(n, len(daily_returns.columns)))
    port_volatility = np.zeros(n)
    port_sr = np.zeros(n)
    port_return = np.zeros(n)

    num_securities = len(daily_returns.columns)
    # num_securities
    for i in range(n):
        # Weight each security
        weights = np.random.random(number_of_companies)
        # normalize it, so that some is one
        weights /= np.sum(weights)
        port_weights[i, :] = weights
        #     print(f'Normalized Weights : {weights.flatten()}')

        # Expected return (weighted sum of mean returns). Mult by 252 as we always do annual calculation and year has 252 business days
        exp_ret = log_ret.mean().dot(weights) * 252
        port_return[i] = exp_ret
        #     print(f'\nExpected return is : {exp_ret[0]}')

        # Exp Volatility (Risk)
        exp_vol = np.sqrt(weights.T.dot(252 * log_ret.cov().dot(weights)))
        port_volatility[i] = exp_vol
        #     print(f'\nVolatility : {exp_vol[0][0]}')

        # Sharpe ratio
        sr = exp_ret / exp_vol
        port_sr[i] = sr
    #     print(f'\nSharpe ratio : {sr[0][0]}')

    # Index of max Sharpe Ratio
    max_sr = port_sr.max()
    ind = port_sr.argmax()
    # Return and Volatility at Max SR
    max_sr_ret = port_return[ind]
    max_sr_vol = port_volatility[ind]
    plt.figure(figsize=(15, 10))
    plt.scatter(port_volatility, port_return, c=port_sr, cmap='plasma')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility', fontsize=15)
    plt.ylabel('Return', fontsize=15)
    plt.title('Efficient Frontier (Bullet Plot)', fontsize=15)
    plt.scatter(max_sr_vol, max_sr_ret, c='blue', s=100, edgecolors='red', marker='o', label='Max \
    Sharpe ratio Portfolio')
    plt.legend()
    plt.show()

    for weight, stock in zip(port_weights[ind], data.get_ticker_symbols()):
        print(f'{round(weight * 100, 2)} % of {stock} should be bought.')

    # best portfolio return
    print(f'\nMarkowitz optimal portfolio return is : {round(max_sr_ret * 100, 2)}% with volatility \
    {max_sr_vol}')

if __name__ == "__main__":
    run_monte_carlo_simulation()
