import numpy as np


def CC_dpy_kick(Vcc, ps, k, initial_sigmas, E_0):
    delta_py_cc = Vcc * np.sin(ps + k * np.array(initial_sigmas))/E_0
    return delta_py_cc


def CC_transverse_y_kick(beta_y, beta_y_cc, delta_py_cc, muy, Qy):
    y_co_cc = (np.sqrt(beta_y * beta_y_cc)) * np.array(delta_py_cc) * np.cos(2 * np.pi * muy - np.pi * Qy) / (
                2 * np.sin(np.pi * Qy))
    return y_co_cc