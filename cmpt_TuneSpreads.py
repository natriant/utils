import numpy as np


def chromatic_tune_spread(dpp_rms, order, Qp):
    if order == 1:
        print('1st chromaticity')
        dqy = Qp * dpp_rms
    if order == 2:
        print('2nd order chromaticity')
        dqy = Qp * (dpp_rms ** 2)
    return dqy


def detuning_with_amplitude_x(Jx, Jy, app_x, app_xy):
    # valid for pyheadtail, to be check for sixtracklib
    # check that this applies also for sixtracklib and not only for
    return (app_x*2*Jx+app_xy*2*Jy)


def detuning_with_amplitude_y(Jx, Jy, app_y, app_xy):
    return (app_y*2*Jy+app_xy*2*Jx)
