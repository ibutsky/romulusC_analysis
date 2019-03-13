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



def multipanel_ion_plot(ion_list, plot_type, bin_type):

    romC_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data_high_mass.h5'%('romulusC', 3035), 'r')
    rom25_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data_high_mass.h5'%('romulus25', 6069), 'r')
    
    if len(ion_list) <= 4:
        nrows = 1
        ncols = len(ion_list)
    else:
        nrows = 2
        ncols = int((len(ion_list) / nrows))

    if plot_type == 'cfrac':
        sharey = True
        ylabel = '$f_{c, \mathrm{cluster}} - f_{c, \mathrm{field}}$'
        yfield = 'covering_fraction'
        ylims = (1e-5)
        palette = sns.cubehelix_palette(5, start=.5, rot=-.75, reverse = True)
        colors = [palette[0], palette[1], palette[2], palette[3]]
        linewidth = 4
        
    elif plot_type == 'column':
        sharey = False
        ylabel = 'dex(N$_{\mathrm{cluster}}$) - dex(N$_{\mathrm{field}}$)'
        yfield = 'median_col'
        colors = ['black', 'black', 'black', 'black']
        linewidth = 2.5

        
    if bin_type == 'mass':
        plot_bins = ['high_mass', 'med_mass']#, 'low_mass']
        plot_labels = ['High Mass', 'Medium Mass']#, 'Low Mass']
        linestyles = ['solid', 'dashed']#, 'dashdot']
    elif bin_type == 'dist':
        plot_bins = ['dist_1', 'dist_2', 'dist_3', 'dist_4']
        plot_labels = ['$\mathrm{r} < 0.5 \mathrm{R}_{\mathrm{vir}}$', \
                       '$ 0.5 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < \mathrm{R}_{\mathrm{vir}}$', \
                       '$ \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 2 \mathrm{R}_{\mathrm{vir}}$' ,\
                       '$ 2 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 3 \mathrm{R}_{\mathrm{vir}}$']
        linestyles = ['solid', 'dashed', 'dashdot', 'dotted']
        
    fig, figax = plt.subplots(nrows = nrows, ncols = ncols, figsize=(3.4*ncols, 3*nrows), sharex = True, sharey = sharey)
    
    for i, ion_name in enumerate(ion_list):
        ion = ion_name.replace(" ", "")
        row = int(i/ncols)
        col = int(i - ncols*row)
        if nrows > 1:
            ax = figax[row][col]
        else:
            ax = figax[col]
        if row == nrows-1:
            ax.set_xlabel('Impact Parameter (kpc)')
        if col == 0:
            ax.set_ylabel(ylabel)
        ax.set_xlim(0, 299)
        
        counts = np.zeros(799**2)
        for pbin, pline, plabel, color in zip(plot_bins, linestyles, plot_labels, colors):
            romC_bins = romC_data['%s_%s_rbins'%(ion, pbin)][:]
            romC_profile = romC_data['%s_%s_%s'%(ion, pbin, yfield)][:]

            # rom25 doesn't have distance bins; 
            # distance bins in romC only have high mass galaxies
            rom25_bins = rom25_data['%s_%s_rbins'%(ion, 'high_mass')][:]
            rom25_profile = rom25_data['%s_%s_%s'%(ion, 'high_mass', yfield)][:]

            if plot_type == 'column':
                diff_profile = np.log10(romC_profile) - np.log10(rom25_profile)
            else:
                diff_profile = romC_profile - rom25_profile
            ax.plot(romC_bins, diff_profile, color = color, linestyle = pline, linewidth = linewidth, label = plabel)
            
 #       if plot_type == 'column':
#            ax.set_yscale('symlog')
            #ylims = ipd.column_plot_ylims(ion)
            #log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
            #ax.annotate(ion_name, xy=(220, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=18)

           # ax.set_ylim(ipd.column_plot_ylims(ion))
           
        if plot_type == 'cfrac':
            ax.annotate(ion_name, xy=(220, 0.05), fontsize=18)
            ax.set_ylim(-0.8, 0.15)
        if row == 0 and col == 1:
            ax.legend()
        fig.tight_layout()
        plt.savefig('romulus_compare_ion_%s.png'%(plot_type), dpi = 300)
        
        



ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']
ion_list = ['H I', 'C IV', 'O VI']

plot_type = 'cfrac'
bin_type = 'dist'
multipanel_ion_plot(ion_list, plot_type, bin_type)


        
