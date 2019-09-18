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

def return_histogram_data(r_arr, cdens_arr, nbins = 800, rmax = 200, ylims=(1e10, 1e17)):
    # turns the really long 1-d combined arrays of projected radius and column density                                                         
    # into a 2d histogram. Returns xbinx, ybins, and counts.T values in 1d                                                                     
    xbins = np.linspace(0, rmax, nbins)
    ybins = 10**np.linspace(np.log10(ylims[0]), np.log10(ylims[1]), nbins)
    counts, x_edge, y_edge = np.histogram2d(r_arr, cdens_arr, bins=(xbins, ybins))
    x_bin_center = ((x_edge[1:] + x_edge[:-1]) / 2).reshape(nbins-1,1)
    # normalize counts in x-space to remove out linear increase in counts with                                                                 
    # radius due to circles of constant impact parameter                                                                                       
    counts /= x_bin_center

    return xbins, ybins, counts.T.ravel()
    
def plot_multipanel(ion_list, rmin = 0, rmax = 200, res = 1600, \
                    nrows = 1, ncols = 3, plot_type = 'cdens', rname = 'radius', ionization_table = 'hm2012'):

    fig, figax = plt.subplots(nrows = nrows, ncols =ncols , figsize = (4*ncols, 3.8*nrows),sharex = True, sharey = False)
    for col, ion in enumerate(ion_list):
        ax = figax[col]
        ylims = ylim_list[col]
        ax.set_yscale('log')
        ax.set_ylim(ylims[0], ylims[1])
        for model, color, linestyle in zip(model_list, color_list, linestyle_list):
            fn = '/nobackupp2/ibutsky/data/charlotte/%s_column_data.h5'%(model)
            r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore = True, space = False, rname = rname)
            
            if len(model_list) == 1:
                im =  ipd.plot_hist2d(ax, r_arr, cdens_arr, rmax,  ylims, vmin = 1e-4, \
                                      vmax_factor = 0.9,  nbins = 800, rmin = rmin)

            res = 400
            xbins, ybins, ion_counts = return_histogram_data(r_arr, cdens_arr, nbins=res, rmax=rmax, ylims = ylims)
            ion_counts = ion_counts.reshape(res-1, res-1)
        
#            ax.set_yscale('log')
            ipd.append_median_profile(ax, xbins[:-1], ybins[:-1], ion_counts.T, color = color, linestyle = linestyle, \
                                          label = model, alpha = 0.3, xmin = 0, xmax = 200, centered = True)            

        # annotate ion labels for plot
        log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
        ax.annotate(ion, xy=(0.75*rmax, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=20)

        ax.set_xlabel('Impact Parameter (kpc)')
        if col == 0:
            if len(model_list) > 1:
                ax.legend(loc = 'center right')
            ax.set_ylabel('Ion Column Density ($\mathrm{cm}^{-2}$)')
        fig.tight_layout()

        if len(model_list) == 1:
            plt.savefig('charlotte_column_density_%s.png'%(model_list[0]), dpi = 300)
        else:
            plt.savefig('charlotte_column_density_compare.png', dpi = 300)



ion_list = ['H I', 'C IV', 'O VI']
ylim_list = [(1e13, 1e21), (3e10, 1e15), (1e12, 1e15)]

model_list = ['cosmo', 'metal', 'H2']
linestyle_list = ['dashed', 'dashdot', 'dotted']
palette = sns.cubehelix_palette(4, start=.5, rot=-.75, reverse = True)
color_list = [palette[0], palette[1], palette[2]]

#model_list = ['H2']
#linestyle_list = ['dashed']
#color_list = ['black']

plot_multipanel(ion_list)
