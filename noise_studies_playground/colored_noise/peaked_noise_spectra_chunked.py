import numpy as np
import matplotlib.pyplot as plt

############## Parameters #################
# Define the characteristics of the chunks
n_chunks = 10
n = 1000  # how many elements in each chunk should have

# Sampling 1, which corresponds to turn by turn signal
turns = np.arange(n_chunks * n)

# Noise parameters
phi_0 = 1e-8  # amplitude of noise
Delta_psi = 0.18  # the peak of the spectrum

psi_t_list = []
psi_t = 0

# parameters for the width of the noise spectrum, ksi
mean = 0.0  # mean of the distribution
std = 0.08

############## Create the noise signal i.e. fixed list of noise kicks #################
for i in turns:
    psi_t_list.append(psi_t)
    ksi = np.random.normal(mean, std)  # different seed on each turn
    psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

phi_noise = phi_0 * np.cos(psi_t_list)

plt.plot(turns, phi_noise, '.-')
plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Time [s]")
plt.show()

############## Chunk analysis #################
# chunk the signal using list comprehension
phi_noise_list = list(phi_noise)
my_chunks = [phi_noise_list[i:i + n] for i in range(0, len(phi_noise), n)]

fft_list = []  # keep the fft of each chunk
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
T = turns[1] - turns[0]  # sampling interval = 1
f = np.linspace(0, 1 / T, n)  # 1/T = frequency

# Plot the FFT spectrum of each/or selected chunk
plot_all = False
plot_one = True

if plot_all:
    for i in range(n_chunks):
        plt.plot(f[:n // 2], np.abs(fft_list[i])[:n // 2] * 1 / n,
                 label='example FFT of chunk {}'.format(i))  # 1 / N is a normalization factor

if plot_one:
    i = 1
    plt.plot(f[:n // 2], np.abs(fft_list[i])[:n // 2] * 1 / n, label='example FFT of chunk {}'.format(i))

# Plot the averaged FFT
plt.plot(f[:n // 2], np.abs(average_fft)[:n // 2] * 1 / n, color='k',
         label='averaged FFT over {} chunks'.format(n_chunks))

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")

plt.legend()

save_fig = True
if save_fig:
    plt.savefig('FFT_{}chunks.png'.format(n_chunks))
plt.show()
plt.close()
