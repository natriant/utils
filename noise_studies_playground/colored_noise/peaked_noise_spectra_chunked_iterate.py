'''
Iterate over the requested number of chunks.
'''

import numpy as np
import matplotlib.pyplot as plt

############## Parameters #################
# Define the characteristics of the chunks
n_chunks_list = [1, 2, 5, 10, 20, 70]
n = 1000  # how many elements in each chunk should have

# Noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.18  # the peak of the spectrum

# parameters for the width of the noise spectrum, ksi
mean = 0.0  # mean of the distribution
std = 0.08

############## Create the noise signal i.e. fixed list of noise kicks #################
averaged_fft_list = []  # Keep the averaged FFT spectrum for the different n values

for j in n_chunks_list:
    # Sampling 1, which corresponds to turn by turn signal
    turns = np.arange(j * n)
    psi_t_list = []
    psi_t = 0

    for turn in turns:
        psi_t_list.append(psi_t)
        ksi = np.random.normal(mean, std)  # different seed on each turn
        psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

    phi_noise = phi_0 * np.cos(psi_t_list)

    ############## Chunk analysis #################
    # chunk the signal using list comprehension
    phi_noise_list = list(phi_noise)
    my_chunks = [phi_noise_list[i:i + n] for i in range(0, len(phi_noise), n)]

    my_sum = 0
    # Noise spectrum
    for i in range(j):
        signal = my_chunks[i]
        my_fft = np.fft.fft(signal)  # type: numpy.array
        my_sum = my_sum + my_fft

    averaged_fft_list.append(my_sum / j)


'''
We plot only half of the spectrum, because that is the only 
half giving us real information.
'''
T = turns[1] - turns[0]  # sampling interval = 1
f = np.linspace(0, 1 / T, n)  # 1/T = frequency

for j in range(len(n_chunks_list)):
    plt.plot(f[:n // 2], averaged_fft_list[j][:n // 2] * 1 / n, label='average FFT over {} chunks'.format(n_chunks_list[j]))

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")
plt.legend()

save_fig = True
if save_fig:
    plt.savefig('FFT_chunks_iterate.png')
plt.show()
plt.close()
