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

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import ion_plot_definitions as ipd
    
def plot_multipanel(ion_list, plot_type, output, nrows = 2, rmax = 3000):

    ncols = int((len(ion_list)+1)/2)
    fig, figax = plt.subplots(nrows = nrows, ncols =ncols , figsize = (4.2*ncols, 4*nrows),sharex = True, sharey = False)

#    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)
    sim = 'romulusC'
    fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
    for i, ion in enumerate(ion_list):
        row = int(i/ncols)
        col = int(i - ncols*row)
        if nrows == 1:
            if ncols == 1:
                ax = figax
            else:
                ax = figax[col]
        elif nrows == 2:
            ax = figax[row][col]            

        ylims = ipd.return_ylims(ion)
        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore = True, space = False)
        if plot_type == 'cdens':
          im =  ipd.plot_hist2d(ax, r_arr, cdens_arr, rmax,  ylims, vmin = 1e-4, vmax_factor = 0.1,  nbins = 800)
            

        # annotate ion labels for plot
        log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
        ax.annotate(ion, xy=(0.75*rmax, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=20)
    
        if row == 1:
            ax.set_xlabel('Impact Parameter (kpc)')
   
        fig.tight_layout()
        plt.savefig('/nobackupp2/ibutsky/plots/YalePaper/romulusC.%06d_ion_column_density.png'%(output))


ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']

plot_type = 'cdens'
output = int(sys.argv[1])

plot_multipanel(ion_list, plot_type, output)
