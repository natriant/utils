'''
1) Create a signal with length, N=1000. 
2) Obtaing the spectrum by performing a FFT.
(numpy.fft.fft is a DFT)
3) Compute the average of 10+ FFT spectrums. 

The goal of this is to obtain a more clear spectrum. 
'''
import numpy as np
import matplotlib.pyplot as plt

params = {'axes.labelsize': 17,
          'xtick.labelsize': 17,
          'ytick.labelsize': 17}

plt.rc('text', usetex=False)
plt.rcParams.update(params)

def create_noise(N, std, colored=False):
    if colored:  # A.Wolski's method
        phi_0 = 1e-8  # amplitude of noise, aka stdPhaseNoise
        Delta_psi = 0.18  # the peak of the spectrum

        psi_t_list = []
        psi_t = 0

        # parameters for ksi
        mean = 0.0
        for i in range(N):
            psi_t_list.append(psi_t)
            ksi = np.random.normal(mean, std)  # different seed on each turn
            psi_t = psi_t + 2 * np.pi * Delta_psi + 2 * np.pi * ksi

        # Construct the noise signal
        y = phi_0 * np.cos(psi_t_list)

    else:
        mu, stdPhaseNoise = 0, 1e-8
        y = np.random.normal(mu, stdPhaseNoise, N)

    return y


N = 1000
turns = np.arange(N)
T = turns[1] - turns[0]  # sampling interval

f = np.linspace(0, 1 / T, N)  # 1/T = frequency

fft_list = []
std = 0.04
for i in range(10): # Define how many FFTs you will average
        y_noise = create_noise(N, std, True)
        fft = np.fft.fft(y_noise)
        fft_list.append(np.abs(fft))

mean_fft = np.mean(fft_list, axis=0)

# Plot vertical lines at 1 std
plt.axvline(0.18+std, 0, 0.2, c='grey', linestyle='--')
plt.axvline(0.18-std, 0, 0.2, c='grey', linestyle='--')

plt.plot(f[:N // 2], np.abs(mean_fft[:N // 2] * 1 / N), c='k')

plt.ylabel("Noise amplitude (arbitrary units)")
plt.xlabel("Frequency (tune units)")
plt.grid(linestyle='--')
plt.tight_layout()
#plt.savefig('colored_noise_rmsKsi1e-1_v2.png')
plt.show()