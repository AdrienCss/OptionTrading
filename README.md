# Option Trading. For educational purposes
- Only Data Managmeent ( data_request ) 

Analysis : 

- Option trading strategies 
- Black & Scholes pricing model
- Implied Volatility surface / Local Volatility & Stochastic Volatility
- Greek 



**Data Retrieval**

The code first uses the y_finane_option_data and y_finane_stock_data internal modules to retrieve option and stock data for a
specific ticker (TSLA will be used in this case). The underlying stock's last price
is then calculated from the retrieved stock data.

# **Implied Volatility Calculation and Plotting for Options**

source file : mainImpliedVolatility.py

# **Simulating heston Volatility**
The basic idea behind the Heston model is that the volatility of an asset's price is not constant over time, but rather follows a stochastic process. The model describes the dynamics of the asset's price and volatility using two state variables: the current price of the asset and its current volatility. The model then uses a set of parameters to describe how these state variables change over time.

source file : mainHestonSimulation.py

# **Creating Option trading stategies and plotting greeks profile of theses strategyies **

source file : mainOptionStrategies.py

