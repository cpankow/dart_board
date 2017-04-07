import numpy as np
from scipy.stats import maxwell, uniform

from . import constants as c
from . import darts
from .posterior import A_to_P

def generate_population(dart, N):
    """
    Generate initial conditions for a set of binaries.

    """

    # Binary masses
    M1 = dart.generate_M1(N)
    M2 = dart.generate_M2(M1, N)

    # Kick vector
    v_kick1 = dart.generate_v_kick1(N)
    theta_kick1 = dart.generate_theta_kick1(N)
    phi_kick1 = dart.generate_phi_kick1(N)

    v_kick2 = dart.generate_v_kick2(N)
    theta_kick2 = dart.generate_theta_kick2(N)
    phi_kick2 = dart.generate_phi_kick2(N)

    # Orbit parameters
    a = np.zeros(N)
    ecc = np.zeros(N)
    for i in range(N):
        ecc[i] = dart.generate_ecc(1)
        a[i] = dart.generate_a(1)
        while (a[i]*(1.0-ecc[i]) < c.min_a or a[i]*(1.0+ecc[i]) > c.max_a):
            ecc[i] = dart.generate_ecc(1)
            a[i] = dart.generate_a(1)

    # Calculate the orbital period
    orbital_period = A_to_P(M1, M2, a)


    # Generate (spatially-resolved?) star formation history
    if dart.generate_pos is None:
        ra = np.zeros(N)
        dec = np.zeros(N)
        t_b = dart.generate_t(N)
    else:
        ra, dec, t_b = dart.generate_pos(N)

    return M1, M2, orbital_period, ecc, v_kick1, theta_kick1, phi_kick1, \
            v_kick2, theta_kick2, phi_kick2, ra, dec, t_b



# Define random deviate functions
def get_v_kick(N):
    """
    Generate random kick velocities from a Maxwellian distribution

    Parameters
    ----------
    sigma : float
        Maxwellian dispersion velocity (km/s)
    N : int
        Number of random samples to generate

    Returns
    -------
    v_kick : ndarray
        Array of random kick velocities
    """

    return maxwell.rvs(scale = c.v_kick_sigma, size = N)

def get_theta(N):
    """
    Generate N random polar angles.

    """

    return np.arccos(1.0-2.0*uniform.rvs(size = N))

def get_phi(N):
    """
    Generate N random azimuthal angles.

    """

    return 2.0*np.pi*uniform.rvs(size = N)

def get_M1(N):
    """ Generate random primary masses

    Parameters
    ----------
    N : int
        Number of random samples to generate

    Returns
    -------
    M1 : ndarray
        Array of random primary masses
    """

    A = (c.alpha+1.0) / (np.power(c.max_mass, c.alpha+1.0) - np.power(c.min_mass, c.alpha+1.0))
    x = uniform.rvs(size = N)

    return np.power(x*(c.alpha+1.0)/A + np.power(c.min_mass, c.alpha+1.0), 1.0/(c.alpha+1.0))

def get_M2(M1, N):
    """
    Generate random secondary masses.

    Parameters
    ----------
    M1 : float
        Set of primary masses

    """

    # Flat in mass ratio
    return M1 * uniform.rvs(size = N)

def get_a(N):
    """ Generate random orbital separations

    Parameters
    ----------
    N : int
        Number of random samples to generate

    Returns
    -------
    a : ndarray
        Array of random orbital separations (Rsun)
    """

    C = 1.0 / (np.log(c.max_a) - np.log(c.min_a))
    x = uniform.rvs(size=N)

    return c.min_a * np.exp(x / C)


def get_ecc(N):
    """
    Generate N random eccentricities.

    """

    return np.sqrt(uniform.rvs(size=N))

def get_t(N):
    """
    Generate N random birth times.

    """

    return (c.max_t - c.min_t) * uniform.rvs(size=N) + c.min_t