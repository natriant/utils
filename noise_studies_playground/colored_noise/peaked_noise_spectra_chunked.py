import numpy as np
import matplotlib.pyplot as plt

# noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.18  # the peak of the spectrum

psi_t_list = []
psi_t = 0

n_chunks = 70 # how many chunks
n = 1000  # how many elements in each chunk should have
turns = np.arange(n_chunks*n)  # np.arange() gives sampling 1 which corresponds to turn by turn signal

# parameters for ksi
mean = 0.0
std = 0.08
for i in turns:
    psi_t_list.append(psi_t)
    ksi = np.random.normal(mean, std)  # different seed on each turn
    psi_t = psi_t + 2*np.pi*Delta_psi + 2*np.pi*ksi

# Construct the noise signal, fixed list of noise kicks
phi_noise = phi_0*np.cos(psi_t_list)

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Time [s]")
plt.plot(turns, phi_noise, '.-')
plt.show()

# chunk the signal
# using list comprehension
phi_noise_list = list(phi_noise)
my_chunks = [phi_noise_list[i:i + n] for i in range(0, len(phi_noise), n)]

fft_list = []  # keep all the fft of each chunk
my_sum = 0
# Noise spectrum
for i in range(n_chunks):
    signal = my_chunks[i]
    my_fft = np.fft.fft(signal)  # type: numpy.array
    my_sum = my_sum + my_fft
    fft_list.append(my_fft)

average_fft = my_sum / n_chunks


'''
We plot only half of the spectrum, because that is the only 
half giving us real information.
'''
T = turns[1] - turns[0]  # sampling interval

f = np.linspace(0, 1 / T, n)  # 1/T = frequency

#plt.plot(f[:n // 2], np.abs(my_sum)[:n // 2] * 1 / n)  # 1 / N is a normalization factor

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")
#for i in range(n_chunks):
#    plt.plot(f[:n // 2], np.abs(fft_list[i])[:n // 2] * 1 / n)  # 1 / N is a normalization factor
#plt.show()
#plt.close()

plt.plot(f[:n // 2], np.abs(fft_list[1])[:n // 2] * 1 / n)  # 1 / N is a normalization factor

plt.plot(f[:n // 2], np.abs(average_fft)[:n // 2] * 1 / n)  # 1 / N is a normalization factor
plt.show()
plt.close()

