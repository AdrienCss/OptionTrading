import numpy as np
from DataRequest import  y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV , implied_volatility_Raphton
import warnings
import matplotlib.pyplot as plt
from matplotlib import cm
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
option_df = option_df[(option_df['strike'] < option_df['underlying_LastPrice'] + 50) & (option_df['strike'] > option_df['underlying_LastPrice'] - 1000)]
option_df['mid_Price'] = (option_df['bid'] + option_df['ask']) /2

## Compute Implied Volatility with 2 methdods
IV = []
for row in option_df.itertuples():
    price = compute_theorical_IV(row.mid_Price , row.underlying_LastPrice ,row.strike, row.T_days / 365, currentRiskFreeRate)
    IV.append(price)

option_df['IV_Calculated_b'] = IV


IV = []
for row in option_df.itertuples():
    price = implied_volatility_Raphton(row.mid_Price , row.underlying_LastPrice ,row.strike, row.T_days / 365, currentRiskFreeRate )
    IV.append(price)

option_df['IV_Calculated_n'] = IV



# plot CALL Skew for each Maturities
for matu in option_df.T_days.unique():
    exp = option_df[(option_df.T_days == matu) & (option_df.Type=='CALL')]
    plt.plot(exp.strike, exp.impliedVolatility, label='IV market')
    plt.plot(exp.strike, exp.IV_Calculated_b, label='IV_Calculated_b')
    plt.xlabel('Strike')
    plt.ylabel(f'Volatility')
    plt.title(f'Implied Volatility Skew ,for T = {matu}')
    plt.legend()
    plt.show()


## Get Option/underlying stock Prices

opt =  option_df[(option_df.inTheMoney==False)]
opt =  opt[(opt.strike <= last_price+100)]
opt =  opt[(opt.strike >= last_price-100)]
opt =  opt[(opt.T_days <=200)]
opt['MoneyNess'] = opt['underlying_LastPrice'] / opt['strike']
opt = opt[['strike' , 'T_days','impliedVolatility']]

# Initiate figure
fig = plt.figure(figsize=(7, 7))
axs = plt.axes(projection="3d")
axs.plot_trisurf(opt.strike, opt.T_days , opt.impliedVolatility, cmap=cm.coolwarm)
axs.view_init(40, 65)
plt.xlabel("Strike")
plt.ylabel("Days to expire")
plt.title(f"Volatility Surface for OTM {ticker} - Implied Volatility as a Function of K and T")
plt.show()


## Computing Dupire Volality for call Option

from Volatility.DupireVolatility import ComputeDupireVolatility


Local_DupireIV = []
for row in option_df.itertuples():
    localIV = ComputeDupireVolatility(row.underlying_LastPrice , row.strike  , 0.0015 ,  row.T_days / 252,row.IV_Calculated_b ,row.Type,1.5)
    Local_DupireIV.append(localIV)

option_df['Local_DupireIV'] = Local_DupireIV


matu = np.unique(option_df.T_days)

for m in matu:
    opt =  option_df[(option_df.Type=='CALL')]
    opt = opt[(opt.T_days ==m)]
    opt =  opt[(opt.strike <= last_price+20)]

    plt.plot(opt.strike, opt.impliedVolatility, label='Black Implied volatility')
    plt.plot(opt.strike, opt.Local_DupireIV, label='Local volatility Dupire')
    plt.xlabel('Strike')
    plt.ylabel('volatility')
    plt.title(f'Black IV vs Dupire LV , T( days) ={m} ')
    plt.legend()
    plt.show()


opt['ratio'] =  opt.impliedVolatility /opt.Local_DupireIV
plt.plot(opt.strike, opt.ratio, label="ratio")
plt.xlabel('Strike')
plt.ylabel('volatility')
plt.title(f'ratio IV / LV')
plt.legend()
plt.show()