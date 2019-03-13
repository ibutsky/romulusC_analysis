import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import h5py as h5
import sys

import numpy as np
import romulus_analysis_helper as rom_help
import seaborn as sns

output = int(sys.argv[1])
rvir = rom_help.get_romulus_rvir('romulusC', output)

dset_list = ['rbins_cold', 'rbins_warm', 'rbins_hot', 'mass_cold', 'mass_warm', 'mass_hot']
plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC_%i_gas_temperature_profile_data'%(output), 'r')

x_cool = np.array(plot_data['rbins_cold'][:])
x_warm = np.array(plot_data['rbins_warm'][:])
x_hot  = np.array(plot_data['rbins_hot' ][:])

y_cool = np.array(plot_data['mass_cold'][:])
y_warm = np.array(plot_data['mass_warm'][:])
y_hot  = np.array(plot_data['mass_hot' ][:])

print(x_cool, x_warm, x_hot)

total = np.sum([y_cool, y_warm, y_hot], axis =0)

fig, ax = plt.subplots(1, 1, figsize=(4, 4))
ax.plot(x_hot / rvir, y_hot / total, color = 'firebrick', label = 'Hot')
ax.plot(x_warm / rvir, y_warm / total, color = 'goldenrod', linestyle = 'dashed', label = 'Warm')
ax.plot(x_cool / rvir, y_cool / total, color = 'steelblue', linestyle = 'dotted', label = 'Cold')
ax.legend()

#plt.xlabel('Spherical Radius (kpc)')
ax.set_xlim(0.1, 3)
ax.set_ylim(0, 1.1)
ax.set_xlabel('R / R$_{200}$')
ax.set_ylabel('Gas Mass Fraction')
fig.tight_layout()
plt.savefig('temperature_mass_profile_%i.png'%(output), dpi = 300)
