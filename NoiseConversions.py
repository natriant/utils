import numpy as np

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
