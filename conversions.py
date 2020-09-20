import numpy as np


def SixtracklibNoiseRmsKick_2_PSD(A, Eb, Vcc , frev):
    ''' 
    Convert the rms noise kick applied to the Sixtracklib simulations to rad^2/Hz. 
    A: The rms noise kick applied in Sixtracklib
    Eb: The beam energy in eV
    Vcc: The CC voltage in V
    frev: The revolution frequency of the machine in Hz 
    '''
    scale_factor = Eb/Vcc # Introduced from the way the kick is applied to the phase and the amplitude of the CC in sixtracklib code. It is normalised with Eb/Vcc.
    PSD = (A*scale_factor)**2/frev

    return PSD


def PSD_2_SixtracklibNoiseRmsKick(PSD, Eb, Vcc , frev):
    '''
    Convert PSD in rad^2/Hz to the rms noise kick as it is applied to the Sixtracklib simulations.
    PSD: The power spectral density in rad^2/Hz
    Eb: The beam energy in eV
    Vcc: The CC voltage in V
    frev: The revolution frequency of the machine in Hz
    '''
    scale_factor = Eb/Vcc # Introduced from the way the kick is applied to the phase and the amplitude of the CC in sixtracklib code. It is normalised with Eb/Vcc.
    A = np.sqrt(PSD*frev)/scale_factor

    return A
