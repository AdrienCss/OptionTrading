# Option trading and analysis

Designed for educational purposes. Here are some of the key topics:


- **Data request** : Recovery of Option & stock financial data via the yFinance API
- **Option Trading Strategies**: We'll explore various strategies for trading options, including both traditional and more exotics techniques.
- **Black & Scholes Pricing Model**: Implementation of the theoretical foundations of the Black & Scholes model: A comparison with the binomial model.
- **Implied Volatility Surface / Local Volatility**: Recovery and calculation of implied volatilities quoted on the market. Observing the long and short term skew/smile
- **Stochastic Volatility**: We'll explore the concept of stochastic volatility with Heston Model
- **Greeks**: We'll cover the key "Greeks" (Delta, Gamma, Theta, Vega, Rho) and their profiles with different options strategies.


----------------------



**Data Retrieval**

The initial step in this code utilizes the yahoofinance API to access financial quotes. This is achieved through the use of the internal modules *y_finane_option_data* and *y_finane_stock_data*, which are utilized to retrieve option and stock data for a specific ticker symbol.

During all the analysis of Read.me we will use as symbol *TSLA*


Here is the simplest code to retrieve data:

```ruby

from DataRequest import  y_finane_option_data , y_finane_stock_data

# Choose the instruments you want to recover
ticker = 'TSLA'

## Get Option & underlying stock price
option_df = y_finane_option_data.get_option_data(ticker)
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
```

Click here to access to dataFolder scprit [Data Request folder](https://github.com/AdrienCss/OptionTrading/blob/main/DataRequest)

# **Creating Option trading stategies**

In this script, we will construct a variety of strategies utilizing fictitious optional data.
We will establish  "Option"& "Stocks" data type and devise distinct strategies from it. 
Additionally, we will plot the corresponding Payoff profiles for these strategies. We will have the capability to display the Greek profiles of these strategies, projected over a range of underlying prices. This will allow us to analyze and evaluate the potential outcomes and risks associated with each strategies.


source file : mainOptionStrategies.py



# **Option Princing : comparison of two methods : Binomial & B&S**

source file : mainPricingModel.py


# **Implied Volatility Calculation and Plotting for Options**

=> Ploting observed implied volatility of real option's quotes.
=> Computing implied volatility using Newton-Raphson Model.
=> ploting skew/smile on short and long maturites ( short/long Smile)


source file : mainImpliedVolatility.py

# **Simulating heston Volatility**

The basic idea behind the Heston model is that the volatility of an asset's price is not constant over time, but rather follows a stochastic process. The model describes the dynamics of the asset's price and volatility using two state variables: the current price of the asset and its current volatility. The model then uses a set of parameters to describe how these state variables change over time.



source file : mainHestonSimulation.py

# **Does the market follow a normal law?**

source file : mainReturnsAnalysis.py

