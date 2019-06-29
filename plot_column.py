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
    
def plot_multipanel(ion_list, output, region, rmax = 3000, ionization_table = 'hm2012'):
    
    if len(ion_list) <= 4:
        nrows = 1
        ncols = len(ion_list)
    else: 
        nrows = 2
        ncols = int((len(ion_list)+1)/2)

    fig, figax = plt.subplots(nrows = nrows, ncols =ncols , figsize = (4.2*ncols, 4*nrows),sharex = True, sharey = False)

#    fn = '/nobackup/ibutsky/data/romulusC/column_%i.h5'%(output)
    sim = 'romulusC'
    if region == 'romulusC':
        fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
        if ionization_table == 'fg2009':
            fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_fg2009_column_data.h5'%(sim, sim, output)
        test = h5.File(fn, 'r')
        print(list(test.keys()))
        rmin = 0
        rname = 'radius'
    else: 
        fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data_region_%s.h5'%(sim, sim, int(output), region)
        rmin = 0
        rmax = 1200 ###### HARD-CODED FOR NOW
        rname = 'px'

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
        r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore = True, space = False, rname = rname)

        if region != 'romulusC':
            r_arr = np.add(r_arr, 600)
        print(min(r_arr), max(r_arr))
        im =  ipd.plot_hist2d(ax, r_arr, cdens_arr, rmax,  ylims, vmin = 1e-4, vmax_factor = 0.1,  nbins = 800, rmin = rmin)
            

        # annotate ion labels for plot
        log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
        ax.annotate(ion, xy=(0.75*rmax, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=20)
    
        if row == 1:
            ax.set_xlabel('Impact Parameter (kpc)')
        if col == 0:
            ax.set_ylabel('Ion Column Density ($\mathrm{cm}^{-2}$)')
        fig.tight_layout()
        if region == 'romulusC':
            if ionization_table == 'fg2009':
                plt.savefig('romulusC.%06d_ion_column_density_fg2009.png'%(output))
            else:
                plt.savefig('romulusC.%06d_ion_column_density.png'%(output))
        else:
            plt.savefig('romulusC.%06d_ion_column_density_region_%s.png'%(output, region))


ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']

ion_list = ['H I', 'C IV', 'O VI']
plot_type = 'cdens'
region = sys.argv[1]
output = int(sys.argv[2])
print(output)
plot_multipanel(ion_list, output, region)#, ionization_table = 'fg2009')
