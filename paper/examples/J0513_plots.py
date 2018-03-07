import numpy as np


import matplotlib
matplotlib.use('Agg')
import corner
import matplotlib.pyplot as plt
from matplotlib import font_manager


delay = 0

# Load chains
chains = np.load("../data/J0513_chain.npy")
if chains.ndim == 4: chains = chains[0]
chains = chains[:,delay:,:]
n_chains, length, n_var = chains.shape
chains = chains.reshape((n_chains*length, n_var))
print(chains.shape)


# Move from ln parameters to parameters in chains
chains[:,0] = np.exp(chains[:,0])
chains[:,1] = np.exp(chains[:,1])
chains[:,2] = np.exp(chains[:,2])
chains[:,9] = np.exp(chains[:,9])


# Create a corner plot to show the posterior distribution

fontProperties = {'family':'serif', 'serif':['Times New Roman'], 'weight':'normal', 'size':12}
ticks_font = font_manager.FontProperties(family='Times New Roman', style='normal', \
                                         weight='normal', stretch='normal', size=10)
plt.rc('font', **fontProperties)

# Corner plot

labels = [r"$M_{\rm 1, i}\ (M_{\odot})$",
          r"$M_{\rm 2, i}\ (M_{\odot})$",
          r"$a_{\rm i}\ (R_{\odot})$",
          r"$e_{\rm i}$",
          r"$v_{\rm k, i}\ ({\rm km}\ {\rm s}^{-1})$",
          r"$\theta_{\rm k}\ ({\rm rad.})$",
          r"$\phi_{\rm k}\ ({\rm rad.})$",
          r"$\alpha_{\rm i}\ ({\rm deg.}) $",
          r"$\delta_{\rm i}\ ({\rm deg.}) $",
          r"$t_{\rm i}\ ({\rm Myr})$"]
plt_range = ([8,25], [2.5,12], [0,100], [0,1], [0,650], [0.0,2.0], [1.5,np.pi],
             [78.0, 78.7], [-66.0, -65.5], [0,50])
hist2d_kwargs = {"plot_datapoints" : False}
corner.corner(chains, labels=labels, range=plt_range, bins=20, max_n_ticks=4, **hist2d_kwargs)

plt.savefig("../figures/J0513_corner.pdf")