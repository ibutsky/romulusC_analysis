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
    
def plot_multipanel(output,ion, threshold_list, label_list = None, rmax = 3000):

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6, 5))
    #    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)
    sim = 'romulusC'
    fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
    
    palette = sns.cubehelix_palette(len(threshold_list)+2, start=.5, rot=-.75, reverse=True)
    palette = palette[1:-1]

    if label_list == None:
        label_list = threshold_list
    for i, threshold in enumerate(threshold_list):
        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore=True, space=False, rname = 'px')
        xbins, cfrac = ipd.covering_fraction_profile(ion, r_arr, cdens_arr, r_max = rmax, threshold=threshold)
        ax.plot(xbins, cfrac, linewidth = 4, color = palette[i], label = "N$_{\mathrm{thres}}$ = %.0e"%threshold)

    ax.set_xlabel('Impact Parameter (kpc)')
    ax.set_ylabel('%s Covering Fraction'%(ion))
    ax.legend()

    ax.set_xlim(0, rmax)
    ax.set_ylim(0, 1.1)

    fig.tight_layout()
    plt.savefig('/nobackupp2/ibutsky/plots/YalePaper/romulusC.%06d_%s_covering_fraction.png'%(output, ion.replace(" ", "")))
      


ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']
threshold_list = [1e9, 1e10, 1e11, 1e12, 1e13, 3e13] 
output = int(sys.argv[1])
ion = 'O VI'
plot_multipanel(output, ion, threshold_list)
