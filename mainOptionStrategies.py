from Option.OptionStrategies import OptionStrategies
from Option.Option import Option , Stock
from Enum.OptionType import OpionType
from Enum.BuySellSide import BuySellSide
from DataRequest import  y_finane_option_data , y_finane_stock_data
import numpy as np

ticker = 'TSLA'

## Get Option/underlying stock Prices
option_df = y_finane_option_data.get_option_data(ticker)
stockPrices_ = y_finane_stock_data.get_stock_price(ticker)
currentprice = stockPrices_.tail(1)['Adj Close'].values[0]

#chose options
# We take the 5th closest maturity
maturity =option_df['T_days'].unique()[5]

options_df = option_df[option_df['T_days'] ==maturity]
call_df = options_df[options_df['Type'] =='CALL']
put_df = options_df[options_df['Type'] =='PUT']



#Getting real Quotes options
call_90_df = call_df.iloc[(call_df['strike']-(currentprice * 0.90)).abs().argsort()[:1]]
call_80_df = call_df.iloc[(call_df['strike']-(currentprice * 0.80)).abs().argsort()[:1]]

put_90_df = put_df.iloc[(put_df['strike']-(currentprice * 0.90)).abs().argsort()[:1]]
put_80_df = put_df.iloc[(put_df['strike']-(currentprice * 0.80)).abs().argsort()[:1]]


# Creating Call spread  80 / 90
call90 = Option(price=call_90_df['lastPrice'].values[0], K=call_90_df['strike'].values[0] , type= OpionType.CALL)
call80 = Option(price=call_80_df['lastPrice'].values[0], K=call_80_df['strike'].values[0] , type= OpionType.CALL)


strategy = OptionStrategies(name = "Call spread 90/80" ,St = currentprice)
strategy.add_Option(option= call90 ,buySell= BuySellSide.SELL , option_number=1 )
strategy.add_Option(option= call80 ,buySell= BuySellSide.BUY , option_number=1 )
strategy.plot()


# Creating put spread  80 / 90
put90 = Option(price=put_90_df['lastPrice'].values[0], K=put_90_df['strike'].values[0] , type= OpionType.PUT)
put80 = Option(price=put_80_df['lastPrice'].values[0], K=put_80_df['strike'].values[0] , type= OpionType.PUT)


strategy = OptionStrategies(name = "PUT Spread 90/ 80" ,St = currentprice)
strategy.add_Option(option= put90 ,buySell= BuySellSide.BUY , option_number=1 )
strategy.add_Option(option= put80,buySell= BuySellSide.SELL , option_number=1 )
strategy.plot()


T = maturity /252
r = 0.015
vol = np.average(call_90_df['impliedVolatility'].values[0] + call_80_df['impliedVolatility'].values[0])

strategy.compute_greek_profile(T ,r , vol)
strategy.plotGreek(greekStr='gamma')
strategy.plotGreek(greekStr='theta')
strategy.plotGreek(greekStr='delta')
strategy.plotGreek(greekStr='vega')




# Creating Straddle

call_dfs= call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_dfs = put_df[(put_df['strike'] == call_df['strike'].values[0])]

put = Option(price=put_dfs['lastPrice'].values[0], K=put_dfs['strike'].values[0] , type= OpionType.PUT)
call = Option(price=call_dfs['lastPrice'].values[0], K=call_dfs['strike'].values[0] , type= OpionType.CALL)


strategy = OptionStrategies(name = "Straddle" ,St = currentprice)
strategy.add_Option(option= put ,buySell= BuySellSide.BUY , option_number=1 )
strategy.add_Option(option= call,buySell= BuySellSide.BUY , option_number=1 )
strategy.plot()


# Creating Strangle

call_df= call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]
put_df= put_df.iloc[(put_df['strike']-(currentprice - 70)).abs().argsort()[:1]]


put = Option(price=put_df['lastPrice'].values[0], K=put_df['strike'].values[0] , type= OpionType.PUT)
call = Option(price=call_df['lastPrice'].values[0], K=call_df['strike'].values[0] , type= OpionType.CALL)

strategy = OptionStrategies(name = "Strangle" ,St = currentprice)
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= put ,buySell= BuySellSide.BUY, option_number=1 )
strategy.plot()


#synthetic call

put_df1 = put_df.iloc[(put_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

put = Option(price=put_df1['lastPrice'].values[0], K=put_df1['strike'].values[0] , type= OpionType.PUT)
stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Synthetic call" ,St = currentprice)
strategy.add_Option(option= put ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_deltaOne(stock=stock,buySell= BuySellSide.BUY )
strategy.plot()


#synthetic PUT

call_df1 = call_df.iloc[(call_df['strike']-(currentprice - 15)).abs().argsort()[:1]]

call = Option(price=call_df1['lastPrice'].values[0], K=call_df1['strike'].values[0] , type= OpionType.CALL)
stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Synthetic PUT", St = currentprice)
strategy.add_Option(option= call ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_deltaOne(stock=stock,buySell= BuySellSide.SELL )

strategy.plot()

# Long Butterfly spread

call1 = Option(price=8, K=currentprice - 25 , type = OpionType.CALL)
call2 = Option(price=2, K=currentprice + 25, type = OpionType.CALL)
call3 = Option(price=4, K=currentprice, type = OpionType.CALL)


strategy = OptionStrategies('Butterfly Spread', St = currentprice )
strategy.add_Option(option= call1 ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= call2 ,buySell= BuySellSide.BUY, option_number=1 )
strategy.add_Option(option= call3 ,buySell= BuySellSide.SELL, option_number=2 )
strategy.plot()

# Short Butterfly spread

strategy = OptionStrategies('Butterfly Spread', St = currentprice )
strategy.add_Option(option= call1 ,buySell= BuySellSide.SELL, option_number=1 )
strategy.add_Option(option= call2 ,buySell= BuySellSide.SELL, option_number=1 )
strategy.add_Option(option= call3 ,buySell= BuySellSide.BUY, option_number=2 )
strategy.plot()
