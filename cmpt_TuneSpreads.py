def chromatic_tune_spread(dpp_rms, order, Qp):
    if order == 1:
        print('1st chromaticity')
        dqy = Qp * dpp_rms
    if order == 2:
        print('2nd order chromaticity')
        dqy = Qp * (dpp_rms ** 2)
    return dqy


def amplitude_detuning_x(Jx, Jy, a_xx, a_xy):
        return a_xx * 2 * Jx + a_xy * 2 * Jy


def amplitude_detuning_y(Jx, Jy, a_yy, a_xy):
    return a_yy * 2 * Jy + a_xy * 2 * Jx

