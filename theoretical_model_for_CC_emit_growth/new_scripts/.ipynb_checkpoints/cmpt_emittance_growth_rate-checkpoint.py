import numpy as  np
from my_functions import *


# Machine and beam parameters
betay = 73  # m in CC2, ~76 in CC1 (MAD-X)
Vcc = 1e6  # V
frev = 43.45e3  # Hz
Eb = 270e9 # eV
sigma_z = 0.155 # rms bunch length, m
beta_0 = 0.999999 # cmpt it from the rest
gamma_0 = 287.7 # cmt it
clight = 299792458  # light speed in meters/second
f_RF = 400.789e6  # CC frequency in Hz
phase_noise = True

# compute correction factor due to bunch length
sigma_phi = bunch_length_m_to_rad(sigma_z, clight, f_RF) # rms bunch length in rad
my_C = cmpt_bunch_length_correction_factor(sigma_phi, phase_noise)
print('correction factor due to bunch length = {}'.format(my_C))
PSD_phi_list = [-123, -115, -112, -111, -107, -102, -102]
#PSD_AN_list = [-128, -124, -115, -117, -113, -115, -107] # dBc/Hz
PSD_list = [ssb_2_dsb(x) for x in PSD_phi_list] # rad^2/Hz

#PSD_phi_list = [-117]
#PSD_list = [ssb_2_dsb(x) for x in PSD_phi_list] # rad^2/Hz
print('PSD initial {}'.format(PSD_list))
'''
dey_list = [] # m/s, geometric emittance

for PSD in PSD_list:
    if phase_noise:
        dey_list.append(emit_growth_phase_noise(betay, Vcc, frev, Eb, my_C, PSD, True))
    else:
        dey_list.append(emit_growth_amplitude_noise(betay, Vcc, frev, Eb, my_C, PSD, True))
print('dey/dt geometric in nm/s: {}'.format(np.array(dey_list)*1e9))
print(('dey/dt normalised in nm/s: {}'.format(np.array(dey_list)*1e9*beta_0*gamma_0)))
print(('dey/dt normalised in um/h: {}'.format(np.array(dey_list)*1e9*beta_0*gamma_0*1e-3*3600)))

'''


dey_list_an = [7.23815933e-05, 1.81814342e-04, 1.44420265e-03, 9.11230271e-04,
 2.28890695e-03, 1.44420265e-03 ,9.11230271e-03]
dey_list_pn = [0.00024485, 0.00154493, 0.00308254, 0.00388068, 0.00974784 ,0.03082537
 ,0.03082537]
dey_total = np.array(dey_list_an)+np.array(dey_list_pn)
print('dey total in um/h {}'.format(dey_total*beta_0*gamma_0*1e-3*3600))
psd_list_2 = cmpt_phase_noise_from_growth_rate(betay, Vcc, frev, Eb, my_C, np.array(dey_total)*1e-9, True)
psd_list_2 = [dsb_2_ssb(x) for x in psd_list_2]
print(psd_list_2)


'''
dey_list = [7.74298189e-05, 1.94494911e-04, 1.54492800e-03, 9.74783666e-04,
 2.44854586e-03 ,1.54492800e-03 ,9.74783666e-03]

psd_list_2 = cmpt_phase_noise_from_growth_rate(betay, Vcc, frev, Eb, my_C, np.array(dey_list)*1e-9, True)
psd_list_2 = [dsb_2_ssb(x) for x in psd_list_2]
print(psd_list_2)
'''
