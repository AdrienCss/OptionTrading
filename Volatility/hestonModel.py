import numpy as np
import matplotlib.pyplot as plt
from DataRequest import  y_finane_option_data , y_finane_stock_data
import pandas as pd



def heston_model_sim(S0, v0, rho, kappa, theta, sigma, T, r, M=10, ):
    N = 252
    dt = T / N
    mu = np.array([0, 0])
    cov = np.array([[1, rho], [rho, 1]])

    S = np.full(shape=(N + 1, M), fill_value=S0)
    v = np.full(shape=(N + 1, M), fill_value=v0)

    W = np.random.multivariate_normal(mu, cov, (N, M))

    for i in range(1, N + 1):
        S[i] = S[i - 1] * np.exp((r - 0.5 * v[i - 1]) * dt + np.sqrt(v[i - 1] * dt) * W[i - 1, :, 0])
        v[i] = np.maximum(v[i - 1] + kappa * (theta - v[i - 1]) * dt + sigma * np.sqrt(v[i - 1] * dt) * W[i - 1, :, 1] , 0)

    return S, v


