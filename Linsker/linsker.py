from neuron import h
import matplotlib.pyplot as plt
import numpy as np

SLICE = 10 # ignore the first n values for image clarity
W_MAX = 2.0
TIME = 10000 # ms

h.load_file('stdrun.hoc')

n1 = h.Section(name='n1') # Neurona 1
n2 = h.Section(name='n2') # Neurona 2
n3 = h.Section(name='n3') # Neurona 3

n1.insert('hh') # Hodgkin-Huxley
n2.insert('hh')
n3.insert('hh')

syn1 = h.Linsker(n2(0.05)) # Sinapsis 1, se llama Linsker porque en el .mod se llama así
h.setpointer(n1(0.05)._ref_v, 'vpre', syn1)

syn2 = h.Linsker(n2(0.05))
h.setpointer(n3(0.05)._ref_v, 'vpre', syn2)

syn1.w = 0.0015 # Inicializar unos pesos
syn2.w = 0.001

weights = [syn1.w, syn2.w]

stim1 = h.IClamp(n1(0.05)) # Estímulo en la neurona 1
stim1.delay = 10 # Inicio del estímulo
stim1.dur = TIME # Duración del estímulo
stim1.amp = 20 # Amplitud del estímulo

stim2 = h.IClamp(n2(0.05)) # Estímulo en la neurona 2
stim2.delay = 10 # Inicio del estímulo
stim2.dur = TIME # Duración del estímulo
stim2.amp = 20 # Amplitud del estímulo

stim3 = h.IClamp(n3(0.05)) # Estímulo en la neurona 3
stim3.delay = 60 # Inicio del estímulo
stim3.dur = TIME # Duración del estímulo
stim3.amp = 20 # Amplitud del estímulo

t_vec = h.Vector().record(h._ref_t)
w1_vec = h.Vector().record(syn1._ref_w)
w2_vec = h.Vector().record(syn2._ref_w)
i1_vec = h.Vector().record(syn1._ref_i)
i2_vec = h.Vector().record(syn2._ref_i)

h.finitialize(-65)

t_stop = TIME
synapses = [syn1, syn2]

while h.t < t_stop:
    h.fadvance()
    
    # weights = np.clip(weights, -W_MAX, W_MAX)
    w_sum = sum([s.w for s in synapses])
    n = len(synapses)
    w_mean = w_sum / n
    
    for s in synapses:
        s.w = s.w - w_mean
        
        if s.w > W_MAX: s.w = W_MAX
        if s.w < -W_MAX: s.w = -W_MAX

fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

axs[0].plot(t_vec[SLICE:], w1_vec[SLICE:], label='w1')
axs[0].plot(t_vec[SLICE:], w2_vec[SLICE:], label='w2')
axs[0].set_ylabel('Pesos')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(t_vec[SLICE:], i1_vec[SLICE:], label='i1')
axs[1].plot(t_vec[SLICE:], i2_vec[SLICE:], label='i2')
axs[1].set_ylabel('Corriente (nA)')
axs[1].set_xlabel('Tiempo (ms)')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.savefig('linsker_results.png')