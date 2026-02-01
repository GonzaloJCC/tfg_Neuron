NEURON {
    POINT_PROCESS Linsker
    POINTER vpre
    RANGE w, gmax, i
    RANGE eta, xo, yo, k1
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

CONSTANT {
    W_MAX = 2.0
}

PARAMETER {
    gmax = 1 (uS)
    eta = 0.00000001
    xo = -65.0 (mV)
    yo = -63.0 (mV)
    k1 = -50.0
}

ASSIGNED {
    v (mV)
    vpost (mV)
    vpre (mV)
    i (nA)
}

STATE {
    w
}

INITIAL {
    w = 0.5
}

BREAKPOINT {
    SOLVE state METHOD cnexp
    vpost = v
    if (vpre > 0) {
        i = -w * vpre
    } else {
        i = 0
    }
}

DERIVATIVE state {
    vpost = v
    w' = eta * ((vpre - xo) * (vpost - yo) + k1)

    if (w > W_MAX) { w = W_MAX }
    if (w < -W_MAX) { w = -W_MAX }
}
