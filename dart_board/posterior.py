# -*- coding: utf-8 -*-

import sys
import numpy as np



def P_to_A(M1, M2, P):
    """
    Orbital period (days) to separation (Rsun).

    """

    mu = c.G * (M1 + M2) * c.Msun_to_g
    n = 2.0*np.pi / P / c.day_to_sec
    a = np.power(mu/(n*n), 1.0/3.0) / c.Rsun_to_cm

    return a


def A_to_P(M1, M2, a):
    """
    Orbital separation (Rsun) to period (days).

    """

    mu = c.G * (M1 + M2) * c.Msun_to_g
    n = np.sqrt(mu/(a**3 * c.Rsun_to_cm**3))
    P = 2.0*np.pi / n

    return P / c.day_to_sec


def ln_posterior(x, dart):
    """ Calculate the natural log of the posterior probability

    Parameters
    ----------
    x : floats
        Model parameters

    dart : DartBoard
        Positions of the dart

    Returns
    -------
    lp : float
        Natural log of the posterior probability

    """

    if dart.second_SN:
        if ln_prior_pos is None:
            M1, M2, a, ecc, v_kick1, theta1, phi1, v_kick2, theta2, phi2, t_b = x
        else:
            M1, M2, a, ecc, v_kick1, theta1, phi1, v_kick2, theta2, phi2, ra_b, dec_b, t_b = x
    else:
        if ln_prior_pos is None:
            M1, M2, a, ecc, v_kick1, theta1, phi1, t_b = x
        else:
            M1, M2, a, ecc, v_kick1, theta1, phi1, ra_b, dec_b, t_b = x


    # Empty array for emcee blobs
    empty_arr = np.zeros(9)


    # Calculate prior probabilities
    lp = 0.0
    lp += dart.prior_M1(M1)
    lp += dart.prior_M2(M2, M1)
    lp += dart.prior_ecc(ecc)
    lp += dart.prior_a(a, ecc)
    lp += dart.prior_v_kick1(v_kick1)
    lp += dart.prior_theta_kick1(theta1)
    lp += dart.prior_phi_kick1(phi1)

    if dart.second_SN:
        lp += dart.prior_v_kick2(v_kick2)
        lp += dart.prior_theta_kick2(theta2)
        lp += dart.prior_phi_kick2(phi2)

    if ln_prior_pos is None:
        lp += dart.prior_t(t_b)
    else:
        lp += dart.prior_pos(ra_b, dec_b, t_b)

    if np.isinf(lp): return -np.inf, empty_arr


    # Get initial orbital period
    orbital_period = A_to_P(M1, M2, a)


    # Run rapid binary evolution code
    output = dart.evolve_binary(1, M1, M2, orbital_period, ecc, v_kick1, theta1,
                                phi1, v_kick2, theta2, phi2, t_b, dart.metallicity)


    m1_out, m2_out, a_out, ecc_out, v_sys, L_x, t_SN1, k1, k2 = output


    binary_evolved = [m1_out, m2_out, a_out, ecc_out, v_sys, L_x, t_SN1, k1, k2]


    # Return posterior probability and blobs
    if check_output(output, dart.binary_type):
        return lp, np.array(binary_evolved)
    else:
        return -np.inf, empty_arr


def check_output(output, binary_type):
    """ Determine if the resulting binary from binary population synthesis
    is of the type desired.

    Parameters
    ----------
    M1_out, M2_out : float
        Masses of each object returned

    a_out, ecc_out : float
        Orbital separation and eccentricity

    v_sys : float
        Systemic velocity of the system

    L_x : float
        X-ray luminosity of the system

    k1, k2 : int
        K-types for each star

    Returns
    -------
    binary_type : bool
        Is the binary of the requested type?

    """

    m1_out, m2_out, a_out, ecc_out, v_sys, L_x, t_SN1, k1, k2 = output

    type_options = np.array(["HMXB", "BHBH", "NSNS", "BHNS"])

    if not np.any(binary_type == type_options):
        print("The code is not set up to detect the type of binary you are interested in")
        sys.exit(-1)

    if binary_type == "HMXB":
        if k1 != 13 and k1 != 14: return False
        if k2 > 9: return False
        if a_out <= 0.0: return False
        if ecc_out < 0.0 or ecc_out >= 1.0: return False
        if L_x <= 0.0: return False
        if m2_out < 4.0: return False

    elif binary_type == "BHBH":
        if k1 != 14 or k2 != 14: return False
        if a_out <= 0.0: return False
        if ecc_out < 0.0 or ecc_out >= 1.0: return False

    elif binary_type == "NSNS":
        if k1 != 13 or k2 != 13: return False
        if a_out <= 0.0: return False
        if ecc_out < 0.0 or ecc_out >= 1.0: return False

    elif binary_type == "BHNS":
        if (k1 != 14 or k2 != 13) and (k1 != 13 or k2 != 14): return False
        if a_out <= 0.0: return False
        if ecc_out < 0.0 or ecc_out >= 1.0: return False

    return True