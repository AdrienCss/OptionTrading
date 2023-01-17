import numpy as np
import matplotlib.pyplot as plt
from DataRequest import  y_finane_option_data , y_finane_stock_data


# first Generating Correlated Random Variable


correl = -0.70
mu = np.array([0,0])
cov_Matrix = np.array([[1,correl] ,[correl,1]  ])

W = np.random.multivariate_normal(mu , cov_Matrix , size= 1000)
plt.plot(W.cumsum(axis=0));
plt.title('Correlated Random Variables')
plt.show()

print(np.corrcoef(W.T))

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




def generate_heston_paths(S, T, r, kappa, theta, v_0, rho, xi, steps, Npaths, return_vol=False):
    dt =T/steps
   # size =(Npath , )

# Maybe the good chose would be to request the price of underlying stock