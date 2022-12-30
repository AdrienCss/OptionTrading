import numpy as np


class ImpliedVolatility:

    def __init__(self, S, K, T, r) -> None:
        self.S = S
        self.K = K
        self.T = T
        self.r = r

    def iterative_way(self) -> float:

        volatility_candidates = np.arange(0.01, 4, 0.0001)
        price_differences = np.zeros_like(volatility_candidates)

        for i in range(len(volatility_candidates)):
            candidate = volatility_candidates[i]
            #    price_differences[i] = abs(observed_price - BS_CALL(self.S, self.K, self.T, self.r, candidate))
            idx = np.argmin(abs(price_differences))
            impliedVolatility = volatility_candidates[idx]
            return impliedVolatility

  #  def newton_raphson_algorithm(self) -> float:

        #     sigma = 0.3

            #   for i in range(max_iterations):

            ### calculate difference between blackscholes price and market price with
            ### iteratively updated volality estimate
            #        diff = black_scholes_call(S, K, T, r, sigma) - C

            ###break if difference is less than specified tolerance level
            #      if abs(diff) < tol:
            #         print(f'found on {i}th iteration')
            #        print(f'difference is equal to {diff}')
            #          break

            #     ### use newton rapshon to update the estimate
        #     sigma = sigma - diff / vega(S, K, T, r, sigma)

#   return sigma