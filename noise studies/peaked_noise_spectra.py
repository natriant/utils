import numpy as np
import matplotlib.pyplot as plt

# noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.32  # the peak of the spectrum

psi_t_list = []
psi_t = 0

turns = np.arange(1000)  # np.arange() gives sampling 1 which corresponds to turn by turn signal

# parameters for ksi
mean = 0.0
std = 0.02
for i in turns:
    psi_t_list.append(psi_t)
    ksi = np.random.normal(mean, std)  # different seed on each turn
    psi_t = psi_t + 2*np.pi*Delta_psi + 2*np.pi*ksi

# Construct the noise signal
phi_noise = phi_0*np.cos(psi_t_list)

plt.ylabel("Amplitude")
plt.xlabel("Time [s]")
plt.plot(turns, phi_noise, '.-')
plt.show()

# Noise spectrum
fft = np.fft.fft(phi_noise)  # type: numpy.array

'''
We plot only half of the spectrum, because that is the only 
half giving us real information.
'''
T = turns[1] - turns[0]  # sampling interval
N = phi_noise.size


f = np.linspace(0, 1 / T, N)  # 1/T = frequency

plt.ylabel("Amplitude")
plt.xlabel("Frequency (tune units)")
plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N) # 1 / N is a normalization factor
plt.show()