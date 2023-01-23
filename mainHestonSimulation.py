import numpy as np
import matplotlib.pyplot as plt
from DataRequest import  y_finane_option_data , y_finane_stock_data
from scipy.stats import kurtosis, skew , norm,stats
from Volatility.hestonModel import  heston_model_sim
from Volatility.ImpliedVolatiliy import compute_theorical_IV
import pandas as pd
import warnings
warnings.simplefilter("ignore", category=FutureWarning)


ticker ='TSLA'

#Requesting stock price
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
optionPrice_ = y_finane_option_data.get_option_data(ticker)

stockPrices_['returns_1D'] = np.log(stockPrices_['Adj Close'] / stockPrices_['Adj Close'].shift(1))
returns = stockPrices_['returns_1D'].dropna(axis=0)

# details
kurt = kurtosis(returns.values)
sk = skew( returns.values)

# Plot chart
plt.hist(returns, bins=100, density=True, color='blue', alpha=0.6)
plt.text(0.6, 0.8, f'Kurtosis: {kurt:.2f}', transform=plt.gca().transAxes)
plt.text(0.6, 0.7, f'Skewness: {sk:.2f}', transform=plt.gca().transAxes)
plt.xlabel('Returns')
plt.ylabel('Frequency')
plt.title('Histogram of TSLA\'s Daily Returns')
plt.show()

# Compute & plot volatility
stockPrices_['realised_volatility_3M'] =stockPrices_['returns_1D'].rolling(60).std() * np.sqrt(252)
stockPrices_['realised_volatility_6M'] =stockPrices_['returns_1D'].rolling(120).std()* np.sqrt(252)

stockPrices_.plot( y=['realised_volatility_3M','realised_volatility_6M'])
plt.title(f'{ticker} stock Realized volatilities')
plt.show()

# Parameters
timeSeries = stockPrices_.tail(300)
currentPrice = stockPrices_.tail(1)['Adj Close'].values[0]

timeSeries['variance_6M'] =  timeSeries['realised_volatility_6M'] **2

S0 =  currentPrice    # asset price
r = 0.02               # risk-free rate
T = 1.0                # time in years intil maturity , let's say 1year

# Heston dependent parameters
kappa = 3          #rate of mean reversion of variance under risk-neutral dynamics
theta = timeSeries['realised_volatility_6M'].mean() **2  # long-term mean of variance under risk-neutral dynamics
v0 = timeSeries['realised_volatility_6M'].tail(1).values[0] **2   # # initial variance under risk-neutral dynamics
rho =  0.055604   # correlation between returns and variances under risk-neutral dynamics
sigma = 0.6    # volatility of volatility


s_sim , vol_sim =  heston_model_sim(S0, v0, rho, kappa, theta, sigma, T, r,10)

timeSeries = timeSeries['Adj Close']

startDate = timeSeries.tail(1).index.values
startDate = startDate.astype(str)[0][:10]

new_index = pd.date_range(start=startDate, end='2030-01-25', freq='B')
s_sim = pd.DataFrame(s_sim)
s_sim.index = new_index[:len(s_sim)]
new_df = pd.concat([timeSeries,s_sim])
new_df = new_df.fillna(method='ffill', axis=1)


#Ploting volatilitty
plt.plot(new_df.head(len(timeSeries)), color='blue')
plt.plot(new_df.tail(len(s_sim)), color='red')
plt.xticks(rotation=45)
plt.ylabel('Price')
plt.legend()
plt.title(f'{ticker} Heston Price Paths simulation' )
plt.show()

#Ploting volatilitty
vol_sim = pd.DataFrame(vol_sim)
vol_sim.index = new_index[:len(vol_sim)]
vol_sim.plot()
plt.ylabel('Volatility')
plt.title('Heston Stochatic Vol Simulation')
plt.show()



strikes =np.arange(currentPrice - 100, currentPrice  + 100,1)

calls = []
test_s = s_sim[:,-1]


for K in strikes:
    C = np.mean(np.maximum(K-test_s,0))*np.exp(-r*T)
    calls.append(C)


ivs = [compute_theorical_IV(C, currentPrice, K, T, r,type_='CALL') for C, K in zip(calls,strikes)]

plt.plot(strikes, ivs)
plt.ylabel('Implied Volatility')
plt.xlabel('Strike')
plt.axvline(currentPrice, color='black',linestyle='--',label='Spot Price')
plt.title('Implied Volatility Smile from Heston Model')
plt.legend()
plt.show()



