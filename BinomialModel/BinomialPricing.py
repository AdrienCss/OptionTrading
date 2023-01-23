import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
import math

import matplotlib.pyplot as plt


def combos(n, i):
    return math.factorial(n) / (math.factorial(n - i) * math.factorial(i))


def binom_EU1(S0, K, T, r, sigma, N, type_='call'):
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = np.exp(-sigma * np.sqrt(dt))
    p = (np.exp(r * dt) - d) / (u - d)
    value = 0
    for i in range(N + 1):
        node_prob = combos(N, i) * p ** i * (1 - p) ** (N - i)
        ST = S0 * (u) ** i * (d) ** (N - i)
        if type_ == 'CALL':
            value += max(ST - K, 0) * node_prob
        elif type_ == 'PUT':
            value += max(K - ST, 0) * node_prob
        else:
            raise ValueError("type_ must be 'call' or 'put'")

    return value * np.exp(-r * T)

