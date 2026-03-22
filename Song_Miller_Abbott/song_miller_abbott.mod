NEURON {
    POINT_PROCESS STDP
    POINTER vpre
    RANGE g, i, s, time_left_pre, time_left_post
    RANGE A_plus, A_minus, tau_plus, tau_minus, g_max, g_min, E_syn, tau_syn, v_thresh
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
}

PARAMETER {
    A_plus = 0.005
    A_minus = 0.00525
    tau_plus = 20 (ms)
    tau_minus = 20 (ms)
    g_max = 1.0
    g_min = 0.0
    E_syn = 0 (mV)
    tau_syn = 5 (ms)
    v_thresh = -54 (mV)
}

ASSIGNED {
    v (mV)
    vpre (mV)
    i (nA)
    g
    s
    time_left_pre (ms)
    time_left_post (ms)
    last_t (ms)
    delta_t (ms)
}

INITIAL {
    s = 0
    g = 0.005
    time_left_pre = 0
    time_left_post = 0
    last_t = -1
}

BREAKPOINT {
    if (t > last_t) {
        s = s * exp(-dt / tau_syn)

        if (time_left_pre > 0) { time_left_pre = time_left_pre - dt } else { time_left_pre = 0 }
        if (time_left_post > 0) { time_left_post = time_left_post - dt } else { time_left_post = 0 }

        if (vpre >= v_thresh && time_left_pre <= 0) {
            time_left_pre = tau_plus
            s = 1.0
            if (time_left_post > 0) {
                delta_t = time_left_pre - time_left_post
                g = g - A_minus * exp(-delta_t / tau_minus)
            }
        }

        if (v >= v_thresh && time_left_post <= 0) {
            time_left_post = tau_minus
            if (time_left_pre > 0) {
                delta_t = time_left_pre - time_left_post
                g = g + A_plus * exp(delta_t / tau_plus)
            }
        }

        if (g > g_max) { g = g_max }
        if (g < g_min) { g = g_min }

        last_t = t
    }

    i = g * s * (v - E_syn)
}
