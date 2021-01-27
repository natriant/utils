import numpy as np

clight = 299792458
gamma_0 = 287.8  # for SPS at 270GeV
beta_0 = np.sqrt(1 - 1/gamma_0**2)

def cavity_wavenumber(f_cc, clight):
    # f_cc the cavity frequency in [Hz], clight the speed of light in [m/s]
    k = 2 * np.pi * f_cc / clight  # wavenumber of the cavity
    return k


def CC_dpy_kick(Vcc, ps, k, initial_sigmas, E_0):
    #Vcc the CC votlage in [V], ps the cc phase in [deg], k the cavity wavenumber, initial_sigmas in [m], E_0 beam energy in [eV]
    delta_py_cc = Vcc * np.sin(ps + k * np.array(initial_sigmas))/E_0
    return delta_py_cc


def CC_transverse_y_kick(beta_y, beta_y_cc, delta_py_cc, muy, Qy):
    # beta_y the beta function at the location,s, where the closed orbit is computed in [m]
    # beta_y_cc the beta function at the location,s0, of the CC kick in [m]
    # muy the phase advance between s and s0 [deg?, rad?]
    # Qy the working point
    y_co_cc = (np.sqrt(beta_y * beta_y_cc)) * np.array(delta_py_cc) * np.cos(2 * np.pi * muy - np.pi * Qy) / (
                2 * np.sin(np.pi * Qy))
    return y_co_cc


def CC_phaseNoise_y_kick(A, f_cc, initial_sigmas):
    # A = Vo/Eb*sqrt(beta_CC/beta_x)*Delta_phi
    delta_py_pn = A*np.cos(2*np.pi*f_cc*initial_sigmas/(clight*beta_0))
    return delta_py_pn


def CC_amplitudeNoise_y_kick(A, f_cc, initial_sigmas):
    # A = Vo/Eb*sqrt(beta_CC/beta_x)*Delta_phi
    delta_py_an = A*np.sin(2*np.pi*f_cc*initial_sigmas/(clight*beta_0))
    return delta_py_an




