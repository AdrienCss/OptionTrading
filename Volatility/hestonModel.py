import numpy as np
import matplotlib.pyplot as plt


# first Generating Correlated Random Variable


correl = -0.70
mu = np.array([0,0])
cov_Matrix = np.array([[1,correl] ,[correl,1]  ])

W = np.random.multivariate_normal(mu , cov_Matrix , size= 1000)
plt.plot(W.cumsum(axis=0));
plt.title('Correlated Random Variables')
plt.show()

print(np.corrcoef(W.T))

def generate_heston_paths(S, T, r, kappa, theta, v_0, rho, xi, steps, Npaths, return_vol=False):
    dt =T/steps
   # size =(Npath , )

# Maybe the good chose would be to request the price of underlying stock