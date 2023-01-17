from Volatility import ImpliedVolatiliy
from Option.OptionStrategies import OptionStrategies
from Option.Option import Option , Stock
from Enum.OptionType import OpionType
from Enum.BuySellSide import BuySellSide
from DataRequest import  y_finane_option_data , y_finane_stock_data
from Volatility.ImpliedVolatiliy import compute_theorical_IV, plot_ImpliedVolatility

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


## Compute & plot Implied Volatility
option_df['calculated_IV'] = option_df.apply(lambda x: compute_theorical_IV(x['lastPrice'],
                                                                               x['underlying_LastPrice'],
                                                                               x['strike'],
                                                                               x['T_days'] / 365 ,
                                                                               currentRiskFreeRate,
                                                                               x['Type']), axis=1)


## Compute & plot Implied Volatility
plot_ImpliedVolatility(option_df , 'CALL', 60 , 244)
plot_ImpliedVolatility(option_df , 'PUT', 60 , 244)


option_df = option_df[option_df['Type'] == "CALL"]   # and  df_options['T_days'] >1]
option_df = option_df[option_df['T_days'] == 6]  # and  df_options['T_days'] >1]

import matplotlib.pyplot as plt
option_df.plot(x='strike', y=['impliedVolatility' ,'calculated_IV' ])
plt.axvline(x =last_price , color = 'r', label = 'CurrentPrice')
plt.title(f"{ticker}'s Option Implied volatility")
plt.show()



#Underlying pricen quote
currentprice = last_price
r=0.01
vol = 0.05
T =1

callOption = Option(price= 3 , K=15 , type= OpionType.CALL)
callOption2 = Option(price= 1 , K=25 , type= OpionType.CALL)
#stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Bear Spread" ,St = currentprice)

strategy.add_Option(option= callOption ,buySell= BuySellSide.BUY , option_number=1 )
strategy.add_Option(option= callOption2 ,buySell= BuySellSide.SELL , option_number=1 )

strategy.compute_greek_profile(T ,r , vol)

strategy.plot()
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')




