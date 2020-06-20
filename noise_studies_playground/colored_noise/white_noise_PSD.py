import numpy as np
import matplotlib.pyplot as plt

n_chunks = int(1e4)
n_turns = 1000
turns = np.arange(n_turns*n_chunks)

T = turns[1] - turns[0]  # sampling interval = 1
fs = 1 / T  # sampling frequency
f = np.linspace(0, 1 / T, n_turns)  # 1/T = frequency

mu, stdPhaseNoise = 0, 1e-8
y = np.random.normal(mu, stdPhaseNoise, len(turns))

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
Sx = np.abs(averaged_fft)**2
plt.plot(f_hz[:n_turns // 2], Sx[:n_turns // 2], color='k')
plt.show()

print('PSD should be {} 1/Hz'.format(stdPhaseNoise**2/frev))
print(Sx[800]/(len(Sx)*frev))

