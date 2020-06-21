import numpy as np
import matplotlib.pyplot as plt


# Find closest value in a list
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


n_chunks = int(1e4)
n_turns = 1000
turns = np.arange(n_turns * n_chunks)

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
vb = 0.18 # betatron tune
f_hz = f * frev

# Plot the averaged FFT, normalised with the signal's length, such as the amplitude is not affected by the length of
# the signal
plt.plot(f_hz[:n_turns // 2] / 1000, averaged_fft[:n_turns // 2] * 1 / len(averaged_fft), color='k')
plt.xlabel('Frequency (kHz)')
plt.ylabel('Noise amplitude (arbitrary units)')
plt.show()

###### 1. MATHEMATICAL APPROACH - SIGNAL PROCESSSING #######
# Compute energy, total power and PSD
PSD = np.abs(averaged_fft / len(averaged_fft)) ** 2  # normalise with the length of the signal
total_power = np.sum(PSD)

plt.plot(f_hz[:n_turns // 2] / 1000, PSD[:n_turns // 2], color='k')
plt.title('PSD from signal processing')
plt.xlabel('Frequency (kHz)')
plt.ylabel('PSD (rad^2/Hz)')
plt.show()

# Find the PSD at vb. In the case of white noise the PSD should remain constant.
# Note that the vb value doesn't exist exactly in f array. Therefore we need to find its closest value.

closest_vb_in_f = closest(list(f_hz), vb*frev)
PSD_vb_index = [i for i in range(len(f_hz)) if f_hz[i] == closest_vb_in_f]

PSD_vb = PSD[PSD_vb_index]

print('Computation of total power and PSD from signal processing ')
print('PSD at vb is = {} rad^2/Hz'.format(PSD_vb))  # units: 1/Hz for amplitude noise
print('The total power of the signal is ={} rad^2'.format(total_power))  # units: 1 for amplitude noise


###### 2. MATHEMATICAL APPROACH - STATISTICS #######
# The total power is the variance of the statistical process
print('Computation of total power and PSD from statistics ')
print('PSD as the std of the process = {} rad^2/Hz'.format(stdPhaseNoise**2/frev))  # units: 1/Hz for amplitude noise
print('The total power of the signal is ={} rad^2'.format(stdPhaseNoise**2))  # units: 1 for amplitude noise