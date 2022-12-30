import numpy as np
from Option import Option
import matplotlib as plt



class OptionStrategies:
    """
        the purpose of this class is to implement option trading strategies on one and the same underlying
    """
    def __init__(self, name, St):
        self.name = name
        self.St = St
        self.STs = np.arange(0, St * 2, 1)
        self.payoffs = np.zeros_like(self.STs)
        self.instruments = []

    def add_Option(self ,  option : Option , buySell ,  option_number = 1) -> None:

        for nb in option_number:
            self.instruments.append(option)

        self.payoffs = self.payoffs  + self._payoff(option,buySell,option_number)

        print(f"{str(option_number)} option(s) added ")

    def add_deltaOne(self, stockPrice, buySell, stock_number=1) -> None:

        for nb in stock_number:
            self.instruments.append(stockPrice) ## add later stockPrice


        # to implement in private method
        if(buySell==1 ):
            payoff = np.array([ S - stockPrice  for S in self.STs])
        if (buySell == -1):
            payoff = np.array([ stockPrice - S for S in self.STs])


        self.payoffs = self.payoffs + payoff

        print(f"{str(stock_number)} option(s) added ")

    def _payoff(self , option : Option , buySell , option_number):

        K = option.K

        long_put = np.array([max(K- S, 0) - option.price for S in self.STs]) * option_number
        short_put = np.array([-max(K-S, 0) - option.price for S in self.STs]) * option_number

        short_call = np.array([max(S - K, 0) - option.price for S in self.STs]) * option_number
        long_call = np.array([max(S - K, 0) - option.price for S in self.STs]) * option_number



    def plot(self, **params):
        plt.plot(self.STs, self.payoffs, **params)
        plt.title(f"Payoff Diagram for {self.name}")
        plt.fill_between(self.STs, self.payoffs,
                         where=(self.payoffs > 0), facecolor='g', alpha=0.4)
        plt.fill_between(self.STs, self.payoffs,
                         where=(self.payoffs < 0), facecolor='r', alpha=0.4)

        plt.xlabel(r'$S_T$')
        plt.ylabel('Profit in $')
        plt.show()

    def describe(self):
        max_profit = self.payoffs.max()
        max_loss = self.payoffs.min()
        print(f"Max Profit: ${round(max_profit, 3)}")
        print(f"Max loss: ${round(max_loss, 3)}")
        c = 0
        for o in self.instruments:
            print(o)
            if o.type == 'call' and o.side == 1:
                c += o.price
            elif o.type == 'call' and o.side == -1:
                c -= o.price
            elif o.type == 'put' and o.side == 1:
                c += o.price
            elif o.type == 'put' and o.side == -1:
                c - + o.price

        print(f"Cost of entering position ${c}")