import numpy as np
import matplotlib.pyplot as plt
from DataRequest import  y_finane_option_data , y_finane_stock_data


ticker ='TSLA'
## Property of Volatility
#The Heston model treats the volatility as a random variable which follows an Ornstein–Uhlenbeck process
#let's observe volatility of certains stock
#  to compute long run average variance

stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
stockPrices_['returns_1D'] = np.log(stockPrices_['Adj Close'] / stockPrices_['Adj Close'].shift(1))

stockPrices_['realised_volatility_3M'] =stockPrices_['returns_1D'].rolling(60).std()
stockPrices_['realised_volatility_6M'] =stockPrices_['returns_1D'].rolling(120).std()

stockPrices_.plot( y=['realised_volatility_3M','realised_volatility_6M'])
plt.title(f'{ticker} stock Realized volatilities')
plt.show()

avg_vol_3M  =stockPrices_['realised_volatility_3M'].mean()
avg_vol_6M  =stockPrices_['realised_volatility_3M'].mean()

avg_variance_3M = np.square(avg_vol_3M)
avg_variance_6M = np.square(avg_vol_6M)


currentPrice = stockPrices_.tail(1)['Adj Close'].values[0]

#Kappa, theta, v_0, rho, xi, steps, Npaths, return_vol=False
#You have to define following


heston_path = generate_heston_paths(currentPrice , T , )
