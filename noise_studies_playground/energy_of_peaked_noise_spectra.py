import numpy as np
import matplotlib.pyplot as plt

# noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.18  # the peak of the spectrum

psi_t_list = []
psi_t = 0

time = np.arange(1000)  # np.arange() gives sampling 1 which corresponds to turn by turn signal, time==turns

# parameters for ksi
mean = 0.0
std = 0.08

for i in time:
    psi_t_list.append(psi_t)
    ksi = np.random.normal(mean, std)  # different seed on each turn
    psi_t = psi_t + 2*np.pi*Delta_psi + 2*np.pi*ksi

# Construct the noise signal
phi_noise = phi_0*np.cos(psi_t_list)

plt.ylabel("Amplitude")
plt.xlabel("Time [s]")
plt.plot(time, phi_noise, '.-')
plt.show()

# Noise spectrum
fft = np.fft.fft(phi_noise)  # type: numpy.array

'''
We plot only half of the spectrum, because that is the only 
half giving us real information.
'''
T = time[1] - time[0]  # sampling interval
N = phi_noise.size

frev=43.45e3
f = np.linspace(0, 1 / T, N)  # 1/T = frequency
f_hz = f*frev  # 1/T = frequency

plt.ylabel("Noise amplitude (arbitrary units) ")
plt.xlabel("Frequency (tune units)")
plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N, c='k') # 1 / N is a normalization factor
plt.show()

# Compute the energy of the signal
#E_s = np.sum(np.abs(phi_noise)**2)
#print(E_s)

# spectral energy density
E_s_f = np.abs(fft)**2
plt.plot(f_hz[:N // 2], E_s_f[:N // 2] * 1 / N) # 1 / N is a normalization factor
#plt.vlines(Delta_psi, 0, 1e-15, colors='r')
plt.ylabel("Energy")
plt.xlabel("Frequency (Hz)")
plt.show()

# power spectral density
frev = 43.45e3
S_x = E_s_f/time
plt.plot(f_hz[:N // 2], S_x[:N // 2] * 1 / N) # 1 / N is a normalization factor
plt.ylabel("PSD")
plt.xlabel("Frequency (Hz)")
plt.show()