import numpy as np
from scipy.special import iv


def emit_growth_phase_noise(betay, Vcc, frev, Eb, CDeltaPhi, PSD_phi, one_sided_psd=False):
    ey_rate = betay*(Vcc*frev/(2*Eb))**2*CDeltaPhi*PSD_phi
    if one_sided_psd:
        return ey_rate
    else:
        return 2*ey_rate


def emit_growth_amplitude_noise(betay, Vcc, frev, Eb, CDeltaA, PSD_A, one_sided_psd=False):
    ey_rate = betay*(Vcc*frev/(2*Eb))**2*CDeltaA*PSD_A
    if one_sided_psd:
        return 2*ey_rate
    else:
        return 4*ey_rate


def cmpt_phase_noise_from_growth_rate(betay, Vcc, frev, Eb, CDeltaPhi, ey_rate, one_sided_psd = False):
    # ey_rate in m/s geometric emittance
    PSD_phi = ey_rate/(betay*(Vcc*frev/(2*Eb))**2*CDeltaPhi)
    if one_sided_psd:
        return PSD_phi
    else:
        return PSD_phi/2

def cmpt_amplitude_noise_from_growth_rate(betay, Vcc, frev, Eb, CDeltaA, ey_rate, one_sided_psd = False):
    # ey_rate in m/s geometric emittance
    PSD_A = ey_rate/(betay*(Vcc*frev/(2*Eb))**2*CDeltaA)
    if one_sided_psd:
        return PSD_A/2
    else:
        return PSD_A/4

def cmpt_bunch_length_correction_factor(sigma_phi, phase_noise=True):
    '''
    This function computes the correction factor, C, due to the bunch length, sigma_phi, assuming a 2D gaussian longitudinal distribution.
    - phase_noise = True (False): computes C for phase (amplitude) noise case
    - sigma_phi: bunch length in radians at the CC frequency

    - Io, I2l: Modified Bessel functions of the first kind.
    - I2l: It converges to zero for larger orders. Therefore, a summation up to a large integer, here 10000 is used,  gives us trustworthy resutls.

    Note: Possibility to compute the factors for a pillbox distribution which is the other extreme (email from Themis).
    '''

    if phase_noise:
        Io = iv(0, sigma_phi ** 2)  # The first argument is the order
        I2l_sum = 0
        for order in range(2, 10000, 2):
            I2l_sum = I2l_sum + iv(order, sigma_phi ** 2)

        C = np.exp(-sigma_phi ** 2) * (Io + 2 * I2l_sum)

    else:
        I2ll_sum = 0
        for order in range(0, 10000, 2):
            I2ll_sum = I2ll_sum + iv(order + 1, sigma_phi ** 2)

        C = np.exp(-sigma_phi ** 2) * I2ll_sum

    return C


# %%

def bunch_length_m_to_rad(L, clight, f_RF):
    phi = L * (2 * np.pi * f_RF) / clight
    return phi


def bunch_length_rad_to_m(phi, clight, f_RF):
    L = phi*clight/(2*np.pi*f_RF)
    return L


def ssb_2_dsb(L):
    """
    Convert the single sideband, SBB, measurement of the noise, L(f) in dBc/Hz, to the double
    sideband density, DSB,  S(f) in rad^2/Hz. According to the IEEE standards:
    S(f) = 2*10^(L(f)/10) in rad^2/Hz, where L(f) in dBc/Hz.
    IMPORTANT: In the definitions here, both L(f) and S(f) are one sided, ie only positive frequencies.
    """

    S = 2*10**(L/10)
    return S


def dsb_2_ssb(S):
    L_10 = np.log10(S/2)
    L = L_10*10
    return L
