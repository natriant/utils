import numpy as np
import matplotlib.pyplot as plt


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

# noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.18  # the peak of the spectrum

psi_t_list = []
psi_t = 0

n_chunks = 5
turns = np.arange(n_chunks*1000)  # np.arange() gives sampling 1 which corresponds to turn by turn signal

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
chunked_signal = chunker_list(np.array(phi_noise), int(turns/n_chunks))
print(len(chunked_signal))
quit()

fft_list = [] # save the fft of each chunk
# Noise spectrum
for chunk in range(n_chunks):
    signal = phi_noise
    fft = np.fft.fft(phi_noise)  # type: numpy.array
    fft_list.append()

'''
We plot only half of the spectrum, because that is the only 
half giving us real information.
'''
T = turns[1] - turns[0]  # sampling interval
N = phi_noise.size


f = np.linspace(0, 1 / T, N)  # 1/T = frequency

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")
plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.show()
plt.close()
