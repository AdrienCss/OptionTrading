import numpy as np
import matplotlib.pyplot as plt

S0=100.0 # spot stock price
K=115.0 # strike
T=0.25 # maturity
r=0.02  # risk free rate
sigma=0.3  # annualized volatility
Ndraws = 10_000


dS = np.random.normal((r - sigma**2/2)*T , sigma*np.sqrt(T), size=Ndraws)
ST = S0 * np.exp(dS)


n, bins, patches = plt.hist(dS,bins=250)
plt.xlabel('$St$')
#plt.xlim([(r - sigma**2/2)*T , ,170])
plt.ylabel('Frequency')
plt.title('Stock Simulation')
plt.show()