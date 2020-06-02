import numpy as np
import matplotlib.pyplot as plt

white_noise = True
colored_noise = False

time = np.arange(1000)
T = time[1] - time[0]  # sampling interval
fs = 1/T  # sampling frequency

if white_noise:
    # Defined as a sequence of uncorrelated random values
    mu, sigma = 0, 1e-8
    # Signal
    y = []
    for i in time:
        y.append(np.random.normal(mu, sigma))

# Noise spectrum
fft = np.fft.fft(y)  # type: numpy.array
N = len(y)

f = np.linspace(0, 1 / T, N)  # 1/T = frequency

plt.ylabel("Amplitude")
plt.xlabel("Frequency (tune units)")
plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.show()

frev=43.45e3
# Plot the frequency in Hz
f_hz = f*frev  # 1/T = frequency

plt.ylabel("Amplitude")
plt.xlabel("Frequency Hz")
plt.plot(f_hz[:N // 2], np.abs(fft)[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.show()
# Compute the energy of the signal
E_s = np.sum(np.abs(y)**2)
print('total energy of the signal = ', E_s)

# spectral energy density
E_s_f = np.abs(fft)**2
plt.plot(f_hz[:N // 2], E_s_f[:N // 2] * 1 / N) # 1 / N is a normalization factor
plt.ylabel("Energy")
plt.xlabel("Frequency Hz")
plt.show()

# power spectral density
S_x = E_s_f/time
plt.plot(f_hz[:N // 2], S_x[:N // 2] * 1 / N) # 1 / N is a normalization factor
plt.ylabel("PSD")
plt.xlabel("Frequency (tune units)")
plt.show()