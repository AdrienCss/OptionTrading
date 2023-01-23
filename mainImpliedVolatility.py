
from DataRequest import  y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV, plot_ImpliedVolatility , implied_volatility_Raphton
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

# Requesting data
ticker = 'TSLA'

## Get Option/underlying stock Prices
option_df = y_finane_option_data.get_option_data(ticker)
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)

last_price = stockPrices_.tail(1)['Adj Close'].values[0]
option_df['underlying_LastPrice'] = last_price
currentRiskFreeRate = 0.015

## Get all Option at +/- 50 strike from underlyinng
option_df = option_df[(option_df['strike'] < option_df['underlying_LastPrice'] + 50) & (option_df['strike'] > option_df['underlying_LastPrice'] - 50)]
option_df['mid_Price'] = (option_df['bid'] + option_df['ask']) /2

## Compute & plot Implied Volatility



IV = []
for row in option_df.itertuples():
    price = compute_theorical_IV(row.mid_Price , row.underlying_LastPrice ,row.strike, row.T_days / 365, 0.06)
    IV.append(price)

option_df['IV_Calculated'] = IV


IV = []
for row in option_df.itertuples():
    price = implied_volatility_Raphton(row.mid_Price , row.underlying_LastPrice ,row.strike, row.T_days / 365, 0.06 )
    IV.append(price)

option_df['IV_Calculated'] = IV

## Compute & plot Implied Volatility
#plot_ImpliedVolatility(option_df , 'CALL', 60 , 244)
#plot_ImpliedVolatility(option_df , 'PUT', 60 , 244)



# plotIV
exp1 = option_df[(option_df.T_days == option_df.T_days.unique()[2]) & (option_df.Type=='CALL')]

import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.impliedVolatility, label='IV market')
plt.plot(exp1.strike, exp1.IV_Calculated, label='IV calculated')

plt.xlabel('Strike')
plt.ylabel('Implied Volatility Values')
plt.legend()
plt.show()



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

test =  option_df[(option_df.Type=='CALL')]
test =  test[(test.strike <= last_price+100)]
test =  test[(test.strike >= last_price-100)]
test =  test[(test.T_days <=200)]
test['MoneyNess'] = test['underlying_LastPrice'] / test['strike']
df = test[['MoneyNess' , 'T_days','IV_Calculated']]
pivot = df.pivot(index='MoneyNess' ,columns='T_days' ,values='IV_Calculated')

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X, Y = np.meshgrid(pivot.columns, pivot.index)
ax.plot_surface(X, Y, pivot.to_numpy(), cmap=cm.gist_rainbow)
ax.set_xlabel('Maturity')
ax.set_ylabel('MoneyNess')
ax.set_zlabel('Implied Volatility')
plt.show()