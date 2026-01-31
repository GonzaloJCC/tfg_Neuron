NEURON {
    POINT_PROCESS LinskerCustom
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

PARAMETER {
    gmax = 0.001 (uS)
    eta = 0.001
    xo = -60.0 (mV)
    yo = -60.0 (mV)
    k1 = 0.0
}

ASSIGNED {
    v (mV)
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
    if (vpre > 0) {
        i = - (w * gmax) * vpre
    } else {
        i = 0
    }
}

DERIVATIVE state {
    w' = eta * ((vpre - xo) * (v - yo) + k1)

    if (w > 1.0) { w = 1.0 }
    if (w < 0.0) { w = 0.0 }
}
