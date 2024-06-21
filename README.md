# StableWealth_Advisor

StableWealth_Advisor is a desktop application developed in Python, designed to provide comprehensive tools for managing and analyzing investments. This application integrates several libraries, including pandas for data manipulation, scipy for advanced calculations, matplotlib for data visualization, and pyside6 for creating a graphical user interface (GUI). The application consists of three main modules: the Stock Market Assistant, Stock Information, and the Treasury Bond Calculator.

## Technologies

 - Python (pandas, scipy, matplotlib, pyside6)
## Features

### 1. Stock Market Assistant
The Stock Market Assistant helps users determine the optimal allocation of capital among selected companies based on historical data from 1970 onwards. This module leverages the yfinance API to retrieve real-time and historical stock data. It uses the Markowitz model for portfolio optimization, combined with the optimize.minimize function from the scipy library, to calculate the best distribution of stocks.

#### Key Features:

 - Optimal capital distribution among selected stocks using the Markowitz model.
 - Analysis based on historical data starting from 1970.
 - Real-time data retrieval through the yfinance API.
 - Advanced calculations using scipy.optimize.minimize.

### 2. Stock Information
The Stock Information module provides detailed insights into stock performance. Users can view daily, monthly, and annual price changes, and access comprehensive information about each company by clicking on the stock name.

#### Key Features:

 - Visualization of daily, monthly, and annual price growth.
 - Detailed company information accessible with a simple click.
 - Interactive and user-friendly interface.

### 3. Treasury Bond Calculator
The Treasury Bond Calculator assists users in calculating various metrics for specific treasury bonds over a chosen period. The algorithm used for bond calculations is quite complex yet flexible, allowing for easy modifications. This means that adding new bonds does not require changes to the entire program, ensuring adaptability and ease of maintenance.

#### Key Features:

 - Accurate calculations for different treasury bonds.
 - Customizable time periods for analysis.
 - Clear tabular presentation of results.
 - Flexible algorithm design, facilitating the addition of new bonds without extensive code changes.

## Screenshots

### Home
![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/home.png)

### Stock Market Assistant
![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/1.png)

![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/2.png)

![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/3.png)

### Stock Information
![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/4.png)

![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/5.png)

### Treasury Bond Calculator
![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/6.png)

![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/7.png)

![Home](https://github.com/WiktorDybalski/StableWealth_Advisor/blob/main/Images/8.png)


### To install all necessary libraries try this: 

```sh
pip install -r requirements.txt
```

## Author

- [Wiktor Dybalski](https://github.com/WiktorDybalski)

- [Maksymilian Katolik](https://github.com/Maksymilian-Katolik)
