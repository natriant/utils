import matplotlib.pyplot as plt
import numpy as np
from CC_transverse_kick import *

# Plotting parameters
params = {'legend.fontsize': 20,
          'figure.figsize': (9.5, 8.5),
          'axes.labelsize': 27,
          'axes.titlesize': 23,
          'xtick.labelsize': 27,
          'ytick.labelsize': 27,
          'image.cmap': 'jet',
          'lines.linewidth': 2,
          'lines.markersize': 5,
          'font.family': 'sans-serif'}

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
plt.rcParams.update(params)

initial_sigmas = np.linspace(-0.155 * 3, 0.155 * 3, 100)  # m

# momentum kick from phase noise
dpy_pn = CC_phaseNoise_y_kick(1e-8, 400e6, initial_sigmas)
# momentum kick from amplitude noise
dpy_an = CC_amplitudeNoise_y_kick(1e-8, 400e6, initial_sigmas)

plt.plot(initial_sigmas, dpy_pn, c='b', label='Phase noise')
plt.plot(initial_sigmas, dpy_an, c='r', label='Amplitude noise')
plt.grid(linestyle='dashed')
plt.xlabel('z [m]')
plt.ylabel(r'$\mathrm{y^\prime} \ [a.u.]}$')
plt.legend()

savefig = True
if savefig:
    plt.savefig('CC_yp_kick_AN_PN.png', bbox_inches='tight')
plt.show()
plt.close()

# CO distortion from the kick
cc_co_pn = CC_transverse_y_kick(73.82, 73.82, dpy_pn, 0, 26.18)
cc_co_an = CC_transverse_y_kick(73.82, 73.82, dpy_an, 0, 26.18)

plt.plot(initial_sigmas, cc_co_pn, c='b', label='Phase noise')
plt.plot(initial_sigmas, cc_co_an, c='r', label='Amplitude noise')
plt.grid(linestyle='dashed')
plt.xlabel('z [m]')
plt.ylabel('y [m]')
plt.legend()

savefig = True
if savefig:
    plt.savefig('CC_AN_PN_kick_CO_distortion.png', bbox_inches='tight')
plt.show()
plt.close()