import sys
import numpy as np
import time

import matplotlib
matplotlib.use('Agg')

sys.path.append("../pyBSE/")
import pybse
import dart_board
from dart_board import sf_history


LMC_metallicity = 0.008

# Values for Swift J0513.4-6547 from Coe et al. 2015, MNRAS, 447, 1630
system_kwargs = {"P_orb" : 27.405, "P_orb_err" : 0.5, "ecc_max" : 0.17, 
                 "ra" : 78.36775, "dec" : -65.7885278}
pub = dart_board.DartBoard("NSHMXB", evolve_binary=pybse.evolve, metallicity=LMC_metallicity,
                           ln_prior_pos=sf_history.lmc.prior_lmc,
                           nwalkers=320, threads=20, thin=1000,
                           system_kwargs=system_kwargs)

pub.aim_darts(N_iterations=100000, a_set='low')


start_time = time.time()
pub.throw_darts(nburn=2, nsteps=500000)
print("Simulation took",time.time()-start_time,"seconds.")



# Acceptance fraction
print("Acceptance fractions:",pub.sampler.acceptance_fraction)

# Autocorrelation length
try:
    print("Autocorrelation length:", pub.sample.acor)
except:
    print("Acceptance fraction is too low.")



# Save outputs
np.save("../data/J0513_mf_low_chain.npy", pub.chains)
np.save("../data/J0513_mf_low_derived.npy", pub.derived)
np.save("../data/J0513_mf_low_lnprobability.npy", pub.lnprobability)
