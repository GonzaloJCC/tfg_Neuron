from neuron import h
import numpy as np
import matplotlib.pyplot as plt

# LaTeX config
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

TIME = 10000 
SLICE = 10

h.load_file('stdrun.hoc')
h.dt = 0.005 # Equivalente a step del cpp

n1 = h.Section(name='n1')
n2 = h.Section(name='n2')
n3 = h.Section(name='n3')

n1.insert('hh')
n2.insert('hh')
n3.insert('hh')

for n in [n1, n2, n3]:
    n.L = 500     # Longitud en micrómetros -> sacado del cpp al definir las neuronas 1 * 7.854e-3; <- diametro
    n.diam = 500  # Diámetro en micrómetros

syn1 = h.STDP(n2(0.5))
h.setpointer(n1(0.5)._ref_v, 'vpre', syn1)

syn2 = h.STDP(n2(0.5))
h.setpointer(n3(0.5)._ref_v, 'vpre', syn2)

stim1 = h.IClamp(n1(0.5))
stim1.delay = 0 
stim1.dur = TIME
stim1.amp = 600 # h1.add_synaptic_input(0.6);

stim3 = h.IClamp(n3(0.5)) 
stim3.delay = 0 
stim3.dur = TIME
stim3.amp = 500

stim2 = h.IClamp(n2(0.5))
stim2.delay = 0 
stim2.dur = TIME
stim2.amp = 500

t_vec = h.Vector().record(h._ref_t)
g1_vec = h.Vector().record(syn1._ref_g)
g2_vec = h.Vector().record(syn2._ref_g)
s1_vec = h.Vector().record(syn1._ref_s)
s2_vec = h.Vector().record(syn2._ref_s)
i1_vec = h.Vector().record(syn1._ref_i)
i2_vec = h.Vector().record(syn2._ref_i)

h.finitialize(-65)

n1(0.5).v = -75
n3(0.5).v = -85
n2(0.5).v = -70

h.finitialize() 

syn1.g = 0.0052
syn2.g = 0.005

h.continuerun(TIME)

t_np = np.array(t_vec)[SLICE:]
g1_np = np.array(g1_vec)[SLICE:]
g2_np = np.array(g2_vec)[SLICE:]

i1_np = -np.array(i1_vec)[SLICE:]
i2_np = -np.array(i2_vec)[SLICE:]

fig, axs = plt.subplots(2, 1, figsize=(6, 5), sharex=True)

# Corriente
axs[0].plot(t_np, i1_np, label=r'i1', color='red')
axs[0].plot(t_np, i2_np, label=r'i2', color='blue')
axs[0].set_ylabel(r'Corriente ($pA$)')
axs[0].legend(loc='upper right')
axs[0].grid(True, alpha=0.3)

# Conductancia
axs[1].plot(t_np, g1_np, label=r'g1', color='red')
axs[1].plot(t_np, g2_np, label=r'g2', color='blue')
axs[1].set_ylabel(r'Conductancia ($pS$)')
axs[1].set_xlabel(r'Tiempo (ms)')
axs[1].legend(loc='upper right')
axs[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('stdp_results.pdf')
