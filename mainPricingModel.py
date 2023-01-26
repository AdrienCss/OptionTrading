from  BinomialModel.BinomialPricing  import  binom_EU1
from BlackAndScholes.BSPricing import priceBS
from DataRequest import y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV

df = y_finane_option_data.get_option_data('TSLA')
stockPrices_ = y_finane_stock_data.get_stock_price('TSLA')

df['Underlying_Price'] = stockPrices_['Adj Close'].tail(1).values[0]

prices_Bi = []

for row in df.itertuples():
    price = binom_EU1(row.Underlying_Price, row.strike, row.T_days / 252, 0.01, 0.5, 200, row.Type)
    prices_Bi.append(price)

df['Binomial_Prices'] = prices_Bi
df['mid_Price'] = (df['bid'] + df['ask']) /2

prices_BS = []
for row in df.itertuples():
    price = priceBS(row.Underlying_Price, row.strike, row.T_days / 252, 0.01 ,row.impliedVolatility , row.Type)
    prices_BS.append(price)


df['Black_And_Scholes_Prices'] = prices_BS

IV = []
for row in df.itertuples():
    price = compute_theorical_IV(row.mid_Price , row.Underlying_Price ,row.strike, row.T_days / 252, 0.01 , row.Type)
    IV.append(price)
df['IV_Calculated'] = IV



# Chose Expiration
exp1 = df[(df.T_days == df.T_days.unique()[2]) & (df.Type=='CALL')]

import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.mid_Price, label='Mid Price')
plt.plot(exp1.strike, exp1.Black_And_Scholes_Prices, label='B&S Prices')
plt.plot(exp1.strike, exp1.Binomial_Prices, label='Binomial Prices')

plt.xlabel('Strike')
plt.ylabel('Call Values')
plt.legend()
plt.show()

# plotIV
import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.impliedVolatility, label='IV market')
plt.plot(exp1.strike, exp1.IV_Calculated, label='IV calculated')

plt.xlabel('Strike')
plt.ylabel('Implied Volatility Values')
plt.legend()
plt.show()


#static Parameters
import numpy as np

K = 100
r = 0.1
T = 1
St =  stockPrices_['Adj Close'].tail(1).values[0]

from BlackAndScholes.BSPricing import BS_CALL ,BS_PUT
import matplotlib.pyplot as plt

S = np.arange(0 ,St + 60,1)

#Using != volatility
callsPrice2 = [BS_CALL(s, K, T, r, 0.2) for s in S]
callsPrice3 = [BS_CALL(s, K, T, r, 0.3) for s in S]
callsPrice4 = [BS_CALL(s, K, T, r, 0.4) for s in S]
callsPrice5 = [BS_CALL(s, K, T, r, 0.5) for s in S]

IntrinsicValue = [max(s - K ,0)for s in S]

plt.plot(S, callsPrice2, label='Call Value sig = 0.20')
plt.plot(S, callsPrice3, label='Call Value sig = 0.30')
plt.plot(S, callsPrice4, label='Call Value sig = 0.40')
plt.plot(S, callsPrice5, label='Call Value sig = 0.50')
plt.plot(S, IntrinsicValue, label='IntrinsicValue')
plt.xlabel('$S_t$')
plt.ylabel(' Value')
plt.title('Implied volatility impact on call value')
plt.legend()
plt.show()




#static Parameters
import numpy as np

K = 100
r = 0.1
T = 1
sig = 0.2
St =  stockPrices_['Adj Close'].tail(1).values[0]

from BlackAndScholes.BSPricing import BS_CALL ,BS_PUT
import matplotlib.pyplot as plt

S = np.arange(0 ,St + 60,1)

#Using != volatility
callsPrice2 = [BS_CALL(s, K, 3, r, sig) for s in S]
callsPrice3 = [BS_CALL(s, K,2, r, sig) for s in S]
callsPrice4 = [BS_CALL(s, K, 1, r, sig) for s in S]
callsPrice5 = [BS_CALL(s, K, 0.50, r,sig) for s in S]

IntrinsicValue = [max(s - K ,0)for s in S]

plt.plot(S, callsPrice2, label='Call Value T = 3')
plt.plot(S, callsPrice3, label='Call Value T = 2')
plt.plot(S, callsPrice4, label='Call Value T = 1')
plt.plot(S, callsPrice5, label='Call Value T = 0.5')
plt.plot(S, IntrinsicValue, label='IntrinsicValue')
plt.xlabel('$S_t$')
plt.ylabel(' Value')
plt.title('Time impact on call value')
plt.legend()
plt.show()


