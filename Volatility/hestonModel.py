import numpy as np
import matplotlib.pyplot as plt
from DataRequest import  y_finane_option_data , y_finane_stock_data
import pandas as pd

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





# Parameters
# simulation dependent
S0 =  float(currentPrice)           # asset price
T = 1.0                # time in years
r = 0.02               # risk-free rate
N = 252                # number of time steps in simulation

# Heston dependent parameters
kappa = 3          #rate of mean reversion of variance under risk-neutral dynamics
theta = 0.20**2    #avg_variance_3M  #0.20**2   # long-term mean of variance under risk-neutral dynamics
v0 = 0.25**2       #avg_variance_3M**2    # # initial variance under risk-neutral dynamics
rho = 0.7          #rhoHisto          # 0.7 # correlation between returns and variances under risk-neutral dynamics
sigma = 0.6        # volatility of volatility


def heston_model_sim(S0, v0, rho, kappa, theta, sigma, T, N, M=10):

    dt = T / N
    mu = np.array([0, 0])
    cov = np.array([[1, rho], [rho, 1]])

    S = np.full(shape=(N + 1, M), fill_value=S0)
    v = np.full(shape=(N + 1, M), fill_value=v0)

    W = np.random.multivariate_normal(mu, cov, (N, M))

    for i in range(1, N + 1):
        S[i] = S[i - 1] * np.exp((r - 0.5 * v[i - 1]) * dt + np.sqrt(v[i - 1] * dt) * W[i - 1, :, 0])
        v[i] = np.maximum(v[i - 1] + kappa * (theta - v[i - 1]) * dt + sigma * np.sqrt(v[i - 1] * dt) * W[i - 1, :, 1] , 0)

    return S, v


## Ploting hypothetical price with heston Model

rho_p = 0.98
rho_n = -0.98

stockPrices_['returns'] = np.full(100 , 100)
s_sim , vol_sim =  heston_model_sim(S0, v0, rho_p, kappa, theta, sigma,T, N, 10)

new_df = pd.concat([stockPrices_['returns'], pd.DataFrame(s_sim)],ignore_index=True)
new_df = new_df.fillna(method='ffill', axis=1)

size_pred = len(s_sim)
size_realized = len(new_df) - size_pred


plt.plot(new_df.iloc[:size_pred , :], color='blue', label='Heston Prediction')
plt.plot(new_df.iloc[size_realized:,:], color='red',label='realized')
plt.legend()
# Show the plot
plt.show()

# Maybe the good chose would be to request the price of underlying stock
