import numpy as np
import matplotlib.pyplot as plt

n_chunks = int(1e4)
n_turns = 1000
turns = np.arange(n_turns*n_chunks)

T = turns[1] - turns[0]  # sampling interval = 1
fs = 1 / T  # sampling frequency
f = np.linspace(0, 1 / T, n_turns)  # 1/T = frequency

# Create colored noise
phi_0 = 1e-8  # amplitude of noise, stdPhaseNoise
Delta_psi = 0.18  # the peak of the spectrum

psi_t_list = []
psi_t = 0

# parameters for ksi
mean, std = 0.0, 0.08
for i in turns:
    psi_t_list.append(psi_t)
    ksi = np.random.normal(mean, std)  # different seed on each turn
    psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

# Construct the noise signal
y = phi_0 * np.cos(psi_t_list)


# chunk the signal using list comprehension
y_list = list(y)
my_chunks = [y_list[i:i + n_turns] for i in range(0, len(y), n_turns)]

fft_array = np.ones((n_chunks, n_turns))  # keep the fft of each chunk

# Averaged FFT computation
for i in range(n_chunks):
    signal = my_chunks[i]
    my_fft = np.fft.fft(signal)  # type: numpy.array
    fft_array[i] = np.abs(my_fft)

averaged_fft = np.mean(fft_array, axis=0)

# convert the f in tune units in Hz
frev = 43.45e3  # Hz
f_hz = f*frev

# Plot the averaged FFT
plt.plot(f_hz[:n_turns // 2], averaged_fft[:n_turns // 2], color='k')
plt.show()


# Compute and plot the power of the spectrum
Sx = np.abs(averaged_fft)**2 # energy/total power
plt.plot(f_hz[:n_turns // 2], Sx[:n_turns // 2], color='k')
plt.show()

# print PSD
print(Sx[800]/(len(Sx)*frev))

# PSD as expected from theory
print('Theoretical computations')
print('PSD should be {} 1/Hz'.format(stdPhaseNoise**2/frev))
print('Total noise power {}'.format(stdPhaseNoise**2))

