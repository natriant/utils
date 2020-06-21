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
plt.plot(f_hz[:n_turns // 2]/1000, averaged_fft[:n_turns // 2], color='k')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Noise amplitude (arbitraty units)')
plt.show()

# Compute energy, total power and PSD
energy = np.abs(averaged_fft)**2
print('total energy ={}'.format(np.sum(energy)/frev))
Sx = energy/len(energy) # total power
PSD = Sx/frev # as we are looking over a band from 0 to frev

plt.plot(f_hz[:n_turns // 2], PSD[:n_turns // 2], color='k')
plt.xlabel('Frequency (kHz)')
plt.ylabel('PSD (rad^2/Hz)')
plt.show()

energy_2 = (np.abs(averaged_fft)/frev)**2
print('new try{}'.format(energy_2[800]))

# print PSD
print('PSD at vb from FFT = {} rad^2/Hz'.format(PSD[800]))
print('Sx {}'.format(np.sum(Sx)))
#Sx = energy/len(energy) # total power
# PSD as expected from theory
print('Theoretical computations')
print('PSD should be {} rad^2/Hz'.format(stdPhaseNoise**2/frev))
print('Total noise power {}'.format(stdPhaseNoise**2))

