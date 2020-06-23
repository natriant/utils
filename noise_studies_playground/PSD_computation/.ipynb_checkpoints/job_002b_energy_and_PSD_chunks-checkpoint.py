import numpy as np
import matplotlib.pyplot as plt


# Find closest value in a list
def closest(lst, K):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

# Flags
white_noise = True
colored_noise = False
savefig = False

# Parameters
# Define the characteristics of the chunks
n_chunks = int(1e4)
n = 1000  # how many elements in each chunk should have

# Sampling 1, which corresponds to turn by turn signal
turns = np.arange(n_chunks * n)


f_rev = 43.35e3  # Hz, compute it exactly
vb = 0.18 * f_rev
print('vb = {} Hz'.format(vb))
# sampling
time = turns / f_rev
T = time[1] - time[0]  # sampling interval = 1
fs = 1 / T  # sampling frequency
f = np.linspace(0, 1 / T, n)  # 1/T = frequency

if white_noise:
    # Defined as a sequence of uncorrelated random values
    mu, sigma = 0, 1e-8
    # Signal
    y = []
    for i in time:
        y.append(np.random.normal(mu, sigma))

if colored_noise:
    phi_0 = 1e-8  # amplitude of noise
    Delta_psi = 0.18  # the peak of the spectrum

    psi_t_list = []
    psi_t = 0

    # parameters for ksi
    mean = 0.0
    std = 0.08
    for i in time:
        psi_t_list.append(psi_t)
        ksi = np.random.normal(mean, std)  # different seed on each turn
        psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

    # Construct the noise signal
    y = phi_0 * np.cos(psi_t_list)

############## Chunk analysis #################
# chunk the signal using list comprehension
y_list = list(y)
my_chunks = [y_list[i:i + n] for i in range(0, len(y), n)]

fft_array = np.ones((n_chunks, n))  # keep the fft of each chunk

# Averaged FFT computation
for i in range(n_chunks):
    signal = my_chunks[i]
    my_fft = np.fft.fft(signal)  # type: numpy.array
    fft_array[i] = np.abs(my_fft)

averaged_fft = np.mean(fft_array, axis=0)



# Plot the averaged FFT
plt.plot(f[:n // 2], averaged_fft[:n // 2] * 1 / n, color='k',
         label='averaged FFT over {} chunks'.format(n_chunks))

plt.title('Averaged FFT of noise, {} chunks'.format(n_chunks))
plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")
plt.legend()
if savefig:
    plt.savefig('averaged_fft_{}chunks.png'.format(n_chunks))
plt.show()
plt.close()

# Total energy of the signal
E_s_total = np.sum(np.abs(averaged_fft) ** 2)
print('total energy of the signal = ', E_s_total)

# Energy spectral density
E_s = np.abs(averaged_fft) ** 2
plt.plot(f[:n // 2], E_s[:n // 2] * 1 / n)  # 1 / N is a normalization factor
plt.ylabel("Energy")
plt.xlabel("Frequency (Hz^2)")
if savefig:
    plt.savefig('energy_spectral_density.png')
plt.show()
plt.close()

# power spectral density
print(time[1000])

S_x = E_s/(n**2) #/(time[1000])  #len(time)
plt.plot(f[:n // 2] / 1000, S_x[:n // 2] * 1 / n)  # 1 / N is a normalization factor
plt.ylabel("Power")
plt.xlabel("Frequency (kHz)")
if savefig:
    plt.savefig('power_spectral_density.png')
plt.show()
plt.close()

# power spectral density - log scale
plt.plot(f[:n // 2] / 1000, S_x[:n // 2] * 1 / n)  # 1 / N is a normalization factor
plt.ylabel("Power")
plt.yscale('log')
plt.xlabel("Frequency (kHz)")
if savefig:
    plt.savefig('power_spectral_density_LogScale.png')
plt.show()
plt.close()

# The vb value doesn't exist exactly in f array. Therefore we need to find
# the closest to that value.
closest_vb_in_f = closest(list(f), vb)
print('The closest value to vb in the frequency list is {} Hz'.format(closest_vb_in_f))
PSD_vb_index = [i for i in range(len(f)) if f[i] == closest_vb_in_f]
PSD_vb = S_x[PSD_vb_index]
print('energy at vb = {}'.format(E_s[PSD_vb_index]))
print('PSD at vb = {}'.format(PSD_vb))
