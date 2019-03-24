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
    
def plot_multipanel(ion_list, output, region, rmax = 3000):

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6, 5))
    #    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)
    sim = 'romulusC'
    if region == 'romulusC':
        fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
    else:
        fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data_region_%s.h5'%(sim, sim, output, region)
#        rmax = 1200 # TEMPORARY HARD-CODE
    palette = sns.color_palette("cubehelix", len(ion_list))

    for i, ion in enumerate(ion_list):
        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore=True, space=False, rname = 'px')
        if region != 'romulusC':
            r_arr = np.add(r_arr, 600)
        xbins, cfrac = ipd.covering_fraction_profile(ion, r_arr, cdens_arr, r_max = rmax)

        ax.plot(xbins, cfrac, linewidth = 4, label = ion)
        ax.legend()
        #ax.annotate(ion, xy=(0.8*rmax, 0.8), fontsize=20)

        ax.set_xlabel('Impact Parameter (kpc)')
        ax.set_ylabel('Ion Covering Fraction')

        fig.tight_layout()
        if region == 'romulusC':
            plt.savefig('romulusC.%06d_ion_covering_fraction.png'%(output))
        else:
            plt.savefig('romulusC.%06d_ion_covering_fraction_region_%s.png'%(output, region))


ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']

ion_list = ['H I', 'C IV', 'O VI']

region = sys.argv[1]
output = int(sys.argv[2])

plot_multipanel(ion_list, output, region)
