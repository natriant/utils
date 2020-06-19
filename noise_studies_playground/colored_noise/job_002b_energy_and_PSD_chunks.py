import numpy as np
import matplotlib.pyplot as plt


# Find closest value in a list
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


white_noise = True
colored_noise = False
savefig = False

turns = np.arange(1000)  # sampling 1
f_rev = 43.35e3  # Hz, compute it exactly
vb = 0.18 * f_rev
print('vb = {} Hz'.format(vb))
time = turns / f_rev

# turns
T = time[1] - time[0]  # sampling interval = 1
fs = 1 / T  # sampling frequency

if white_noise:
    # Defined as a sequence of uncorrelated random values
    mu, sigma = 0, 1e-8
    # Signal
    y = []
    for i in time:
        y.append(np.random.normal(mu, sigma))

if colored_noise:
    phi_0 = 1e-8  # amplitude of noise
    Delta_psi = 0.18  # the peak of the spectrum

    psi_t_list = []
    psi_t = 0

    # parameters for ksi
    mean = 0.0
    std = 0.08
    for i in time:
        psi_t_list.append(psi_t)
        ksi = np.random.normal(mean, std)  # different seed on each turn
        psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

    # Construct the noise signal
    y = phi_0 * np.cos(psi_t_list)

plt.plot(time, y)
plt.xlabel('time (s)')
plt.ylabel('Noise amplitude')
if savefig:
    plt.savefig('noise_signal.png')
plt.show()
plt.close()

# Noise spectrum
fft = np.fft.fft(y)  # type: numpy.array
N = len(y)

f = np.linspace(0, 1 / T, N)  # 1/T = frequency

plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.ylabel("Amplitude (arbitrary units) ")
plt.xlabel("Frequency (Hz)")
if savefig:
    plt.savefig('noise_spectrum_FFT.png')
plt.show()
plt.close()

# Total energy of the signal
E_s_total = np.sum(np.abs(y) ** 2)
print('total energy of the signal = ', E_s_total)

# Energy spectral density
E_s = np.abs(fft) ** 2
plt.plot(f[:N // 2], E_s[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.ylabel("Energy")
plt.xlabel("Frequency (Hz^2)")
if savefig:
    plt.savefig('energy_spectral_density.png')
plt.show()
plt.close()

# power spectral density
S_x = E_s / time
plt.plot(f[:N // 2] / 1000, S_x[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.ylabel("Power")
plt.xlabel("Frequency (kHz)")
if savefig:
    plt.savefig('power_spectral_density.png')
plt.show()
plt.close()

# power spectral density - log scale
plt.plot(f[:N // 2] / 1000, S_x[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.ylabel("Power")
plt.yscale('log')
plt.xlabel("Frequency (kHz)")
if savefig:
    plt.savefig('power_spectral_density_LogScale.png')
plt.show()
plt.close()

# The vb value doesn't exist exactly in f array. Therefore we need to find
# the closest to that value.
closest_vb_in_f = closest(list(f), vb)
print('The closest value to vb in the frequency list is {} Hz'.format(closest_vb_in_f))
PSD_vb_index = [i for i in range(len(f)) if f[i] == closest_vb_in_f]
PSD_vb = S_x[PSD_vb_index]
print('PSD at vb = {}'.format(PSD_vb))
