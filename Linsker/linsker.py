from neuron import h
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')

n1 = h.Section(name='n1')
n2 = h.Section(name='n2')
n3 = h.Section(name='n3')

n1.insert('hh')
n2.insert('hh')
n3.insert('hh')

syn1 = h.LinskerCustom(n2(0.5))
h.setpointer(n1(0.5)._ref_v, 'vpre', syn1)

syn2 = h.LinskerCustom(n2(0.5))
h.setpointer(n3(0.5)._ref_v, 'vpre', syn2)

syn1.eta = 0.00001
syn1.xo = -65
syn1.yo = -63
syn1.k1 = -50.0
syn1.w = 0.3

syn2.eta = 0.00001
syn2.xo = -65
syn2.yo = -63
syn2.k1 = -50.0 
syn2.w = 0.3

stim1 = h.IClamp(n1(0.5))
stim1.delay = 10
stim1.dur = 40
stim1.amp = 20

stim2 = h.IClamp(n2(0.5))
stim2.delay = 10
stim2.dur = 40
stim2.amp = 20

stim3 = h.IClamp(n3(0.5))
stim3.delay = 60
stim3.dur = 40
stim3.amp = 20

t_vec = h.Vector().record(h._ref_t)
w1_vec = h.Vector().record(syn1._ref_w)
w2_vec = h.Vector().record(syn2._ref_w)
i1_vec = h.Vector().record(syn1._ref_i)
i2_vec = h.Vector().record(syn2._ref_i)

h.finitialize(-65)
h.continuerun(2000)

fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Plot 1: W
axs[0].plot(t_vec, w1_vec, label='w1 (N1->N2)', linewidth=2)
axs[0].plot(t_vec, w2_vec, label='w2 (N3->N2)', linewidth=2)
axs[0].set_ylabel('Weight (w)')
axs[0].set_title('Evolución de Pesos Sinápticos')
axs[0].legend()
axs[0].grid(True)

# Plot 2: I
axs[1].plot(t_vec, i1_vec, label='i1 (N1->N2)')
axs[1].plot(t_vec, i2_vec, label='i2 (N3->N2)')
axs[1].set_ylabel('Current (nA)')
axs[1].set_xlabel('Time (ms)')
axs[1].set_title('Corrientes Sinápticas')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.savefig('linsker_results.png')
