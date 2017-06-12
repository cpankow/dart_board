# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import maxwell

from . import constants as c


def prior_probability(x, dart):
    """
    Calculate all the prior probabilities.

    """


    if dart.second_SN:
        if dart.prior_pos is None:
            ln_M1, ln_M2, ln_a, ecc, v_kick1, theta_kick1, phi_kick1, v_kick2, theta_kick2, phi_kick2, ln_t_b = x
        else:
            ln_M1, ln_M2, ln_a, ecc, v_kick1, theta_kick1, phi_kick1, v_kick2, theta_kick2, phi_kick2, ra_b, dec_b, ln_t_b = x
    else:
        if dart.prior_pos is None:
            ln_M1, ln_M2, ln_a, ecc, v_kick1, theta_kick1, phi_kick1, ln_t_b = x
        else:
            ln_M1, ln_M2, ln_a, ecc, v_kick1, theta_kick1, phi_kick1, ra_b, dec_b, ln_t_b = x


    # Calculate prior probabilities
    lp = 0.0
    lp += dart.prior_ln_M1(ln_M1)
    lp += dart.prior_ln_M2(ln_M2, ln_M1)
    lp += dart.prior_ecc(ecc)
    lp += dart.prior_ln_a(ln_a, ecc)
    lp += dart.prior_v_kick1(v_kick1)
    lp += dart.prior_theta_kick1(theta_kick1)
    lp += dart.prior_phi_kick1(phi_kick1)


    if dart.second_SN:
        lp += dart.prior_v_kick2(v_kick2)
        lp += dart.prior_theta_kick2(theta_kick2)
        lp += dart.prior_phi_kick2(phi_kick2)

    if dart.prior_pos is None:
        lp += dart.prior_t(ln_t_b)
    else:
        lp += dart.prior_pos(ra_b, dec_b, ln_t_b)

    return lp



def ln_prior_M1(M1):
    """
    Return the prior probability on M1: P(M1).

    """

    if M1 < c.min_mass_M1 or M1 > c.max_mass_M1: return -np.inf
    norm_const = (c.alpha+1.0) / (np.power(c.max_mass_M1, c.alpha+1.0) - np.power(c.min_mass_M1, c.alpha+1.0))
    return np.log( norm_const * np.power(M1, c.alpha) )

def ln_prior_ln_M1(ln_M1):
    """
    Return the prior probability on the natural log of M1: P(ln_M1).

    """

    M1 = np.exp(ln_M1)

    if M1 < c.min_mass_M1 or M1 > c.max_mass_M1: return -np.inf
    norm_const = (c.alpha+1.0) / (np.power(c.max_mass_M1, c.alpha+1.0) - np.power(c.min_mass_M1, c.alpha+1.0))
    return np.log( norm_const * np.power(M1, c.alpha+1.0) )

def ln_prior_M2(M2, M1):
    """
    Return the prior probability on M2: P(M2 | M1).

    """

    if M2 < c.min_mass_M2 or M2 > M1: return -np.inf
    return np.log(1.0 / M1)

def ln_prior_ln_M2(ln_M2, ln_M1):
    """
    Return the prior probability on the natural log of M2: P(ln_M2 | M1).

    """

    M1 = np.exp(ln_M1)
    M2 = np.exp(ln_M2)

    if M2 < c.min_mass_M2 or M2 > M1: return -np.inf
    return np.log(M2 / M1)

def ln_prior_a(a, ecc):
    """
    Return the prior probability on a: P(a).

    """

    if a*(1.0-ecc) < c.min_a or a*(1.0+ecc) > c.max_a: return -np.inf
    norm_const = 1.0 / (np.log(c.max_a) - np.log(c.min_a))

    return np.log( norm_const / a )

def ln_prior_ln_a(ln_a, ecc):
    """
    Return the prior probability on the natural log of a: P(ln_a).

    """

    a = np.exp(ln_a)

    if a*(1.0-ecc) < c.min_a or a*(1.0+ecc) > c.max_a: return -np.inf
    norm_const = 1.0 / (np.log(c.max_a) - np.log(c.min_a))

    return np.log( norm_const )

def ln_prior_ecc(ecc):
    """
    Return the prior probability on ecc: P(ecc).

    """

    if ecc < 0.0 or ecc > 1.0: return -np.inf
    return np.log(2.0 * ecc)


def ln_prior_v_kick(v_kick):
    """
    Return the prior probability on v_kick: P(v_kick).

    """

    if v_kick < 0.0: return -np.inf
    return np.log(maxwell.pdf(v_kick, scale=c.v_kick_sigma))


def ln_prior_theta_kick(theta_kick):
    """
    Return the prior probability on the SN kick theta: P(theta).

    """

    if theta_kick <= 0.0 or theta_kick >= np.pi: return -np.inf
    return np.log(np.sin(theta_kick) / 2.0)


def ln_prior_phi_kick(phi_kick):
    """
    Return the prior probability on the SN kick phi: P(phi).

    """

    if phi_kick < 0.0 or phi_kick > np.pi: return -np.inf
    return -np.log(np.pi)


def ln_prior_t(t_b):
    """
    Return the prior probability on the binary's birth time (age).

    """

    if t_b < c.min_t or t_b > c.max_t: return -np.inf
    norm_const = 1.0 / (c.max_t - c.min_t)

    return np.log(norm_const)

def ln_prior_ln_t(ln_t_b):
    """
    Return the prior probability on the natural log of the binary's birth time (age).

    """

    t_b = np.exp(ln_t_b)

    if t_b < c.min_t or t_b > c.max_t: return -np.inf
    norm_const = 1.0 / (c.max_t - c.min_t)
    return np.log(norm_const * t_b)
