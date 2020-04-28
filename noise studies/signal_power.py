import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

'''
Generate a test signal, a 2 Vrms sine wave at 1234 Hz, 
corrupted by 0.001 V**2/Hz of white noise sampled at 10 kHz.
'''
fs = 10e3
N = 1e5
amp = 2*np.sqrt(2)
freq = 1234.0
noise_power = 0.001 * fs / 2
print(noise_power)
quit()
time = np.arange(N) / fs
x = amp*np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

'''
Compute and plot the PSD
'''
f, Pxx_den = signal.periodogram(x, fs, scaling='density') # density is the default
plt.semilogy(f, Pxx_den)
plt.ylim([1e-7, 1e2])
plt.title('Power Spectral Density')
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()

'''
If we average the last half of the spectral density, 
to exclude the peak, we can recover the noise power on the signal.
'''
print('The noise power of the signal is {}'.format(np.mean(Pxx_den[2566:])))

'''
Now we compute and plot the power spectrum
'''
f, Pxx_spec = signal.periodogram(x, fs, 'flattop', scaling='spectrum')
plt.figure()
plt.semilogy(f, np.sqrt(Pxx_spec))
plt.ylim([1e-4, 1e1])
plt.title('Power spectrum')
plt.xlabel('frequency [Hz]')
plt.ylabel('Linear spectrum [V RMS]')
plt.show()

'''
The peak height in the power spectrum is an estimate of the RMS amplitude.
'''
print('the RMS amplitude of the power spectrum is {} '.format(np.sqrt(Pxx_spec.max())))
