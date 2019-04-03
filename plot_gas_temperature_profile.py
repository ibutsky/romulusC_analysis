import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import h5py as h5
import sys

import numpy as np
import romulus_analysis_helper as rom_help
import ion_plot_definitions as ipd
import seaborn as sns

sns.set_style("ticks",{'axes.grid': True, 'grid.linestyle': '--'})

output = int(sys.argv[1])
rvir = rom_help.get_romulus_rvir('romulusC', output)
rvir = rom_help.get_romulusC_r200(output)
#rvir = 1.0
xmax = 3000
xmax /= rvir
xmax = 4.
dset_list = ['rbins_cold', 'rbins_warm', 'rbins_hot', 'mass_cold', 'mass_warm', 'mass_hot']
plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC_%i_gas_temperature_profile_data'%(output), 'r')



x_cold = np.array(plot_data['rbins_cold'][:]) / rvir
x_cool = np.array(plot_data['rbins_cool'][:]) / rvir
x_warm = np.array(plot_data['rbins_warm'][:]) / rvir
x_hot  = np.array(plot_data['rbins_hot' ][:]) / rvir

y_cold = np.array(plot_data['mass_cold'][:])
y_cool = np.array(plot_data['mass_cool'][:])
y_warm = np.array(plot_data['mass_warm'][:])
y_hot  = np.array(plot_data['mass_hot' ][:])


x_cold_bins, y_cold_bins = ipd.digitize(x_cold, y_cold, xmax = xmax)
x_cool_bins, y_cool_bins = ipd.digitize(x_cool, y_cool, xmax = xmax)
x_warm_bins, y_warm_bins = ipd.digitize(x_warm, y_warm, xmax = xmax)
x_hot_bins,  y_hot_bins  = ipd.digitize(x_hot,  y_hot,  xmax = xmax)

ipd.normalize_digitized_arrays([y_cold_bins, y_cool_bins, y_warm_bins, y_hot_bins])

fig, ax = plt.subplots(1, 1, figsize=(4.6, 3.8))
lw = 3
ax.plot(ipd.interleave(x_hot_bins,  1), ipd.interleave(y_hot_bins,  0), color = 'firebrick',\
        linewidth = lw,                        label = 'Hot Gas')
ax.plot(ipd.interleave(x_warm_bins, 1), ipd.interleave(y_warm_bins, 0), color = 'goldenrod',\
        linewidth = lw, linestyle = 'dashed',  label = 'Warm Gas')
ax.plot(ipd.interleave(x_cool_bins, 1), ipd.interleave(y_cool_bins, 0), color = 'seagreen', \
        linewidth = lw, linestyle = 'dashdot', label = 'Cool Gas')
ax.plot(ipd.interleave(x_cold_bins, 1), ipd.interleave(y_cold_bins, 0), color = 'steelblue',\
        linewidth = lw, linestyle = 'dotted',  label = 'Cold Gas') 
ax.legend(loc = 6)

#plt.xlabel('Spherical Radius (kpc)')
ax.set_xlim(0.05, xmax)
#ax.set_ylim(0, 1.1)
ax.set_yscale('log')
ax.set_ylim(1e-2, 2)
fs = 16
ax.set_xlabel('$\mathrm{R\ /\ R}_{200}$')#, fontsize = fs)
#ax.set_xlabel('$\mathrm{Radius\ (kpc)}$')#, fontsize = fs)
ax.set_ylabel('$\mathrm{Gas\ Mass\ Fraction}$')#, fontsize = fs)
fig.tight_layout()
plt.savefig('temperature_mass_profile_%i.png'%(output), dpi = 300)
