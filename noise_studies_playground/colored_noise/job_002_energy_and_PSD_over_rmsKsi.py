import numpy as np
import matplotlib.pyplot as plt


# Find closest value in a list
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


turns = np.arange(1000)  # sampling 1
f_rev = 43.35e3  # Hz, compute it exactly
vb = 0.18 * f_rev
print('vb = {} Hz'.format(vb))
time = turns / f_rev

# turns
T = time[1] - time[0]  # sampling interval = 1
fs = 1 / T  # sampling frequency

# Parameters of the color noise
phi_0 = 1e-8  # amplitude/strength of noise
Delta_psi = 0.18  # the peak of the spectrum
psi_t = 0

# parameters for ksi
mean, std = 0.0, 0.08

n_repeat = 5  # How many times the simulations is repeated to decrease the uncertainty.

PSD_vb_list = []
for repeat in range(n_repeat):
    psi_t_list = []
    for i in time:
        psi_t_list.append(psi_t)
        ksi = np.random.normal(mean, std)  # different seed on each turn
        psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

    # Construct the noise signal
    y = phi_0 * np.cos(psi_t_list)


    # Noise spectrum
    fft = np.fft.fft(y)  # type: numpy.array
    N = len(y)
    f = np.linspace(0, 1 / T, N)  # 1/T = frequency
    # energy spectral density
    E_s = np.abs(fft) ** 2
    # power spectral density
    S_x = E_s / time

    # The vb value doesn't exist exactly in f array. Therefore we need to find
    # the closest to that value.
    closest_vb_in_f = closest(list(f), vb)
    #print('The closest value to vb in the frequency list is {} Hz'.format(closest_vb_in_f))
    PSD_vb_index = [i for i in range(len(f)) if f[i] == closest_vb_in_f]
    PSD_vb = S_x[PSD_vb_index]
    PSD_vb_list.append(PSD_vb)

print('PSD values over {} runs : {}'.format(n_repeat, PSD_vb_list))
print('mean PSD value  = {} rad^2/Hz'.format(np.mean(PSD_vb_list)))
print('std PSD value  = {} rad^2/Hz'.format(np.std(PSD_vb_list)))
