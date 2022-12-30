from Volatility import ImpliedVolatiliy
from Option.OptionStrategies import OptionStrategies
from Option.Option import Option , Stock
from Enum.OptionType import OpionType
from Enum.BuySellSide import BuySellSide


#Underlying pricen quote
currentprice = 20
K = 25


callOption = Option(price= 3 , K=K , type= OpionType.CALL)
putOption = Option(price= 2 , K=K , type= OpionType.PUT)
stock = Stock(price = currentprice)

strategy = OptionStrategies(name = "Bear Spread" ,St = currentprice)

strategy.add_Option(option = callOption ,buySell = BuySellSide.SELL , option_number=1 )
strategy.add_Option(option = putOption ,buySell = BuySellSide.BUY , option_number=5 )
strategy.add_deltaOne(stock = stock,buySell = BuySellSide.BUY ,stock_number=2 )

strategy.plot()