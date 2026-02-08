NEURON {
    POINT_PROCESS STDP
    POINTER vpre
    RANGE g, i
    RANGE A_plus, A_minus, tau_plus, tau_minus, g_max, E_syn
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}


PARAMETER {
    A_plus = 0.01
    A_minus = 0.01
    tau_plus = 20 (ms)
    tau_minus = 20 (ms)
    g_max = 1 (uS)
    E_syn = 0 (mV)
}

ASSIGNED {
    v (mV)
    vpost (mV)
    vpre (mV)
    i (nA)
}

STATE {
    g
}

INITIAL {
    g = 0.05
}

BREAKPOINT {
    vpost = v
    i = g * (vpost - E_syn)
}

DERIVATIVE state {
    vpost = v
}
