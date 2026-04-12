from brian2 import *
import numpy as np
import matplotlib.pyplot as plt

# Configuración LaTeX
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "font.size": 11,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9
})

defaultclock.dt = 0.005 * ms
TIME = 10000 * ms
SLICE = 10

Area = 7.854e-3 * cm**2
Cm = 1 * uF/cm**2 * Area
E_Na = 50 * mV
E_K = -77 * mV
E_L = -54.387 * mV

gNa_max = 120 * msiemens/cm**2 * Area
gK_max = 36 * msiemens/cm**2 * Area
gL_max = 0.3 * msiemens/cm**2 * Area

tau_plus = 20 * ms
tau_minus = 20 * ms
A_plus = 0.005
A_minus = 0.00525
g_max = 1.0
g_min = 0.0
E_syn = 0 * mV
tau_syn = 5 * ms
v_thresh = -54 * mV

I_scale = 100 * nA / mV 

eqs_neurons = '''
dv/dt = (I_ext + I_syn - I_Na - I_K - I_L) / Cm : volt
I_Na = gNa_max * m**3 * h * (v - E_Na) : amp
I_K = gK_max * n**4 * (v - E_K) : amp
I_L = gL_max * (v - E_L) : amp

I_syn : amp  
I_ext : amp  

dm/dt = alpha_m * (1 - m) - beta_m * m : 1
dh/dt = alpha_h * (1 - h) - beta_h * h : 1
dn/dt = alpha_n * (1 - n) - beta_n * n : 1

alpha_m = 0.1 * (v/mV + 40) / (1 - exp(-(v/mV + 40) / 10)) / ms : Hz
beta_m = 4.0 * exp(-(v/mV + 65) / 18) / ms : Hz
alpha_h = 0.07 * exp(-(v/mV + 65) / 20) / ms : Hz
beta_h = 1.0 / (1 + exp(-(v/mV + 35) / 10)) / ms : Hz
alpha_n = 0.01 * (v/mV + 55) / (1 - exp(-(v/mV + 55) / 10)) / ms : Hz
beta_n = 0.125 * exp(-(v/mV + 65) / 80) / ms : Hz
'''

neurons = NeuronGroup(3, eqs_neurons, threshold='v > v_thresh', reset='', refractory=3*ms, method='rk4')

neurons.v = [-75, -85, -70] * mV
neurons.I_ext = [510, 500, 500] * nA 

neurons.m = '0.1 * (v/mV + 40) / (1 - exp(-(v/mV + 40) / 10)) / (0.1 * (v/mV + 40) / (1 - exp(-(v/mV + 40) / 10)) + 4.0 * exp(-(v/mV + 65) / 18))'
neurons.h = '0.07 * exp(-(v/mV + 65) / 20) / (0.07 * exp(-(v/mV + 65) / 20) + 1.0 / (1 + exp(-(v/mV + 35) / 10)))'
neurons.n = '0.01 * (v/mV + 55) / (1 - exp(-(v/mV + 55) / 10)) / (0.01 * (v/mV + 55) / (1 - exp(-(v/mV + 55) / 10)) + 0.125 * exp(-(v/mV + 65) / 80))'

eqs_syn = '''
g_weight : 1
ds/dt = -s / tau_syn : 1 (clock-driven)
dApre/dt = -Apre / tau_plus : 1 (event-driven)
dApost/dt = -Apost / tau_minus : 1 (event-driven)

I_syn_post = -g_weight * s * (v_post - E_syn) * I_scale : amp (summed)
'''

S = Synapses(neurons, neurons, model=eqs_syn,
             on_pre='''
             s = 1.0
             Apre += A_plus
             g_weight = clip(g_weight - Apost, g_min, g_max)
             ''',
             on_post='''
             Apost += A_minus
             g_weight = clip(g_weight + Apre, g_min, g_max)
             ''', method='rk4')

S.connect(i=np.array([0, 1]), j=np.array([2, 2]))

S.g_weight[0] = 0.0052
S.g_weight[1] = 0.005

t_mon = StateMonitor(neurons, 'v', record=True)
s_mon = StateMonitor(S, ['g_weight', 's'], record=True)

print("Simulando STDP en Brian2...")
run(TIME, report='text')

t_np = t_mon.t / ms
t_np = t_np[SLICE:]

g1_np = s_mon.g_weight[0][SLICE:]
g2_np = s_mon.g_weight[1][SLICE:]

s1_np = s_mon.s[0][SLICE:]
s2_np = s_mon.s[1][SLICE:]
v_post_np = t_mon.v[2][SLICE:] / mV  
E_syn_mV = 0.0

i1_np = -g1_np * s1_np * (v_post_np - E_syn_mV)
i2_np = -g2_np * s2_np * (v_post_np - E_syn_mV)

fig, axs = plt.subplots(2, 1, figsize=(6, 5), sharex=True)

axs[0].plot(t_np, i1_np, label=r'i1', color='red')
axs[0].plot(t_np, i2_np, label=r'i2', color='blue')
axs[0].set_ylabel(r'Corriente ($pA$)')
axs[0].legend(loc='upper right')
axs[0].grid(True, alpha=0.3)

axs[1].plot(t_np, g1_np, label=r'g1', color='red')
axs[1].plot(t_np, g2_np, label=r'g2', color='blue')
axs[1].set_ylabel(r'Conductancia ($pS$)')
axs[1].set_xlabel(r'Tiempo (ms)')
axs[1].legend(loc='upper right')
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('brian2_stdp_2_synapses.pdf')
print("¡Gráfica guardada en brian2_stdp_2_synapses.pdf!")
