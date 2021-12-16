import numpy as np

def bunch_length_m_to_rad(sigma_z, clight, f_RF):
    sigma_phi = sigma_z * (2 * np.pi * f_RF) / clight
    return sigma_phi


def bunch_length_rad_to_m(sigma_phi, clight, f_RF):
    sigma_z = sigma_phi*clight/(2*np.pi*f_RF)
    return sigma_z


def bunch_length_m_to_time(sigma_z, clight):
    # Arguments: L: bunch length in m, clight: in m/s
    # Return: the bunch length in seconds. the result corresponds to 1 sigma_t (usual units 4sigma_t)
    sigma_t = sigma_z/clight
    return sigma_t

def bunch_length_time_to_m(sigma_t, clight):
    # Arguments:  sigma_t in seconds,clight: in m/s
    # Return: the bunch length in seconds. the result corresponds to 1 sigma_t (usual units 4sigma_t)
    sigma_z = sigma_t*clight
    return sigma_z

