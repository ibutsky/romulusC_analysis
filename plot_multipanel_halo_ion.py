import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

import numpy as np
import h5py as h5
import sys
from matplotlib.colors import LogNorm

import seaborn as sns
sns.set_style("white",{'font.family':'serif', 'axes.grid': True, "ytick.major.size": 0.1,
                "ytick.minor.size": 0.05,
                'grid.linestyle': '--'})

import ion_plot_definitions as ipd



def multipanel_ion_plot(sim, output, ion_list, plot_type, bin_type):

    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_histogram_data.h5'%(sim, output), 'r')
    profile_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data2.h5'%(sim, output), 'r')
    
    nrows = 2
    ncols = int(len(ion_list) / 2)
    if plot_type == 'cfrac':
        sharey = True
        ylabel = 'Ion Covering Fraction'
        yfield = 'covering_fraction'
        ylims = (1e-5)
        palette = sns.cubehelix_palette(5, start=.5, rot=-.75, reverse = True)
        colors = [palette[0], palette[1], palette[2], palette[3]]
        linewidth = 4
        
    elif plot_type == 'column':
        sharey = False
        ylabel = 'Ion Column Density ($\mathrm{cm}^{-2}$)'
        yfield = 'median_col'
        colors = ['black', 'black', 'black', 'black']
        linewidth = 2.5

        
    if bin_type == 'mass':
        plot_bins = ['high_mass', 'med_mass', 'low_mass']
        plot_labels = ['High Mass', 'Medium Mass', 'Low Mass']
        linestyles = ['solid', 'dashed', 'dashdot']
    elif bin_type == 'dist':
        plot_bins = ['dist_1', 'dist_2', 'dist_3', 'dist_4']
        plot_labels = ['$\mathrm{r} < 0.5 \mathrm{R}_{\mathrm{vir}}$', \
                       '$ 0.5 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < \mathrm{R}_{\mathrm{vir}}$', \
                       '$ \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 2 \mathrm{R}_{\mathrm{vir}}$' ,\
                       '$ 2 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 3 \mathrm{R}_{\mathrm{vir}}$']
        linestyles = ['solid', 'dashed', 'dashdot', 'dotted']
        
    fig, figax = plt.subplots(nrows = 2, ncols = 4, figsize=(3.4*ncols, 3*nrows), sharex = True, sharey = sharey)
    
    for i, ion_name in enumerate(ion_list):
        ion = ion_name.replace(" ", "")
        row = int(i/ncols)
        col = int(i - ncols*row)
        ax = figax[row][col]
        if row == 1:
            ax.set_xlabel('Impact Parameter (kpc)')
        if col == 0:
            ax.set_ylabel(ylabel)
        ax.set_xlim(0, 299)
        
        counts = np.zeros(799**2)
        for pbin, pline, plabel, color in zip(plot_bins, linestyles, plot_labels, colors):
            profile_bins = profile_data['%s_%s_rbins'%(ion, pbin)][:]
            profile = profile_data['%s_%s_%s'%(ion, pbin, yfield)][:]

            ax.plot(profile_bins, profile, color = color, linestyle = pline, linewidth = linewidth, label = plabel)
            
            if plot_type == 'column':
                xbins = plot_data['%s_%s_xbins'%(ion, pbin)][:]
                ybins = plot_data['%s_%s_ybins'%(ion, pbin)][:]
                counts += plot_data['%s_%s_counts'%(ion, pbin)][:]
            
        if plot_type == 'column':
            ax.set_yscale('log')
            ylims = ipd.column_plot_ylims(ion)
            log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
            ax.annotate(ion_name, xy=(220, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=18)

            ax.set_ylim(ipd.column_plot_ylims(ion))
            max_counts = counts.max()
            counts = counts.reshape(799, 799)
            ax.pcolormesh(xbins, ybins, counts, vmin=1e-3, vmax = 0.9*max_counts, cmap='GnBu', norm=LogNorm())
        elif plot_type == 'cfrac':
            if row == 0 and col == 0:
                ax.legend()
            ax.annotate(ion_name, xy=(220, 0.9), fontsize=18)

        fig.tight_layout()
        plt.savefig('../../plots/YalePaper/%s.%06d_multipanel_%s_halo_%s.png'%(sim, output, plot_type, bin_type), dpi = 300)
        
        


sim = sys.argv[1]
output = int(sys.argv[2])

ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']


for plot_type in ['cfrac', 'column']:
    for bin_type in ['mass', 'dist']:
        multipanel_ion_plot(sim, output, ion_list, plot_type, bin_type)
