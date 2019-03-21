import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import h5py as h5
import sys
from matplotlib.colors import LogNorm

import seaborn as sns
sns.set_style("white",{'font.family':'serif', 'axes.grid': True, "ytick.major.size": 0.1,
                "ytick.minor.size": 0.05,
                'grid.linestyle': '--'})

import ion_plot_definitions as ipd
    
def plot_multipanel(output, ion_list, threshold_list, label_list = None, rmax = 3000):
    ncols = len(ion_list)
    fig, figax = plt.subplots(nrows = 1, ncols = ncols, figsize = (3.4*ncols, 3), sharex=True, sharey=True)
    #    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)
    sim = 'romulusC'
    fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
    
    palette = sns.cubehelix_palette(len(threshold_list)+2, start=.5, rot=-.75, reverse=True)
    palette = sns.cubehelix_palette(len(threshold_list)+2, reverse=True) #pink
    palette = sns.cubehelix_palette(len(threshold_list)+2, start=2, rot=0, dark=0, light = 0.95) #green
    palette = sns.cubehelix_palette(len(threshold_list)+2, start=2.8, rot=-.1) #blue

    palette = palette[1:-1]
    joe = h5.File('cfrac_threshold.h5', 'w')
    if label_list == None:
        label_list = threshold_list
    for j, ion in enumerate(ion_list):
        ax = figax[j]
        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore=True, space=False)
        for i, threshold in enumerate(threshold_list):
            xbins, cfrac = ipd.covering_fraction_profile(ion, r_arr, cdens_arr, r_max = rmax, threshold=threshold)
            ax.plot(xbins, cfrac, linewidth = 4, color = palette[i], label = label_list[i])
            base_name = '%s_N%s_'%(ion.replace(' ', ''), label_list[i])
            joe.create_dataset(base_name+'rbins', data = xbins)
            joe.create_dataset(base_name+'covering_fraction', data = cfrac)
            joe.flush()
            
        ax.annotate(ion, xy=(2350, 0.98), fontsize = 18)
        ax.set_xlabel('Impact Parameter (kpc)')
        if j == 0:
            ax.set_ylabel('Ion Covering Fraction')
        elif j == 1:
            ax.legend(loc = 2, ncol = 2, title = "N$_{\mathrm{thres}}$ ($\mathrm{cm}^{-2}$)", fontsize = 10)

    ax.set_xlim(0, rmax-10)
    ax.set_ylim(0, 1.15)

    fig.tight_layout()
    plt.savefig('romulusC_%06d_covering_fraction_threshold.png'%(output), dpi = 300)
      



threshold_list = [1e10, 1e11, 1e12, 3e12, 1e13, 3e13] 
label_list = ['1e10', '1e11', '1e12', '3e12', '1e13', '3e13']
output = int(sys.argv[1])
ion = 'O VI'
ion = 'H I'

ion_list = ['H I', 'C IV', 'O VI']
plot_multipanel(output, ion_list, threshold_list, label_list = label_list)
