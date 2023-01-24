
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



# plot skew
exp1 = option_df[(option_df.T_days == option_df.T_days.unique()[2]) & (option_df.Type=='CALL')]

import matplotlib.pyplot as plt
plt.plot(exp1.strike, exp1.impliedVolatility, label='IV market')
plt.plot(exp1.strike, exp1.IV_Calculated, label='IV calculated')

plt.xlabel('Strike')
plt.ylabel('Implied Volatility Values')
plt.legend()
plt.show()



import matplotlib.pyplot as plt
from matplotlib import cm

## Get Option/underlying stock Prices
option_df = y_finane_option_data.get_option_data(ticker)
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
last_price = stockPrices_.tail(1)['Adj Close'].values[0]
option_df['underlying_LastPrice'] = last_price

type = 'CALL'
opt =  option_df[(option_df.Type==type)]
opt =  opt[(opt.strike <= last_price+100)]
opt =  opt[(opt.strike >= last_price-100)]
opt =  opt[(opt.T_days <=200)]
opt['MoneyNess'] = opt['underlying_LastPrice'] / opt['strike']
opt = opt[['strike' , 'T_days','impliedVolatility']]

# Initiate figure
fig = plt.figure(figsize=(7, 7))
axs = plt.axes(projection="3d")
axs.plot_trisurf(opt.MoneyNess, opt.T_days , opt.impliedVolatility, cmap=cm.coolwarm)
axs.view_init(40, 65)
plt.xlabel("Strike")
plt.ylabel("Days to expire")
plt.title(f"Volatility Surface for {type} {ticker} - Implied Volatility as a Function of K and T")
plt.show()
