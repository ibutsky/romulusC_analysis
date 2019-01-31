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
    
def plot_multipanel(ion_list, plot_type, output):

    nrows = 2
    ncols = int((len(ion_list)+1)/2)
    fig, ax = plt.subplots(nrows = nrows, ncols =ncols , figsize = (4.2*ncols, 4*nrows),sharex = True, sharey = False)

    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)

    for i, ion in enumerate(ion_list):
        row = int(i/ncols)
        col = int(i - ncols*row)

        ylims = ipd.return_ylims(ion)
        rmax = 2500

        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion)

        if plot_type == 'cdens':
          im =  ipd.plot_hist2d(ax[row][col], r_arr, cdens_arr, rmax,  ylims, vmin = 1e-3)
            

        # annotate ion labels for plot
        log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
        ax[row][col].annotate(ion, xy=(780, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=20)
    
        if row == 1:
            ax[row][col].set_xlabel('Impact Parameter (kpc)')
   
        fig.tight_layout()
        plt.savefig('/nobackupp2/ibutsky/plots/YalePaper/romulusC_multipanel_column_density_%i.png'%(output))


ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']

plot_type = 'cdens'
output = int(sys.argv[1])

plot_multipanel(ion_list, plot_type, output)
