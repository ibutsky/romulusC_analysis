import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

import numpy as np
import h5py as h5
import sys
from matplotlib.colors import LogNorm

import seaborn as sns
#sns.set_style("white",{'font.family':'serif', 'axes.grid': True, "ytick.major.size": 0.1,
 #               "ytick.minor.size": 0.05,
  #              'grid.linestyle': '--'})
sns.set_style("ticks",{'axes.grid': True, 'grid.linestyle': '--'})

import ion_plot_definitions as ipd

def load_combined_counts(ion, output_list, plot_bin, sim = 'romulusC'):
    counts = np.zeros(799*799)
    for output in output_list:
        plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_histogram_data.h5'%(sim, output), 'r')
        counts += plot_data['%s_%s_counts'%(ion, plot_bin)][:]
    return counts.reshape(799, 799)


def multipanel_ion_plot(sim, output, ion_list, plot_type, bin_type, do_colormesh = False, \
                        combine = False, combined_output_list = []):

    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_histogram_data.h5'%(sim, output), 'r')
    profile_data = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data.h5'%(sim, output), 'r')
    
    if len(ion_list) < 4:
        nrows = 1
        ncols = len(ion_list)
    else:
        nrows = 2
        ncols = int((len(ion_list) / nrows))

    if plot_type == 'cfrac':
        sharey = True
        ylabel = '$\mathrm{Ion\ Covering\ Fraction}$'
        yfield = 'covering_fraction'
        ylims = (1e-5)
        palette = sns.cubehelix_palette(5, start=.5, rot=-.75, reverse = True)
        colors = [palette[0], palette[1], palette[2], palette[3]]
        linewidth = 4
        
    elif plot_type == 'column':
        sharey = False
        ylabel = '$\mathrm{Ion\ Column\ Density\ (cm}^{-2}$)'
        yfield = 'median_col'
        colors = ['black', 'black', 'black', 'black']
        palette = sns.cubehelix_palette(5, start=.5, rot=-.75, reverse = True)
        colors = [palette[0], palette[1], palette[2], palette[3]]
        linewidth = 2.5

        
    if bin_type == 'mass':
        plot_bins = ['high_mass', 'med_mass', 'low_mass']
        plot_labels = ['High Mass', 'Medium Mass', 'Low Mass']
        linestyles = ['solid', 'dashed', 'dashdot']
    elif bin_type == 'dist':
        plot_bins = ['dist_1', 'dist_2', 'dist_3', 'dist_4']
#        plot_bins = ['dist_5', 'dist_3', 'dist_4']
        plot_labels = ['$\mathrm{r} < 0.5 \mathrm{R}_{\mathrm{vir}}$', \
                       '$ 0.5 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < \mathrm{R}_{\mathrm{vir}}$', \
                       '$ \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 2 \mathrm{R}_{\mathrm{vir}}$' ,\
                       '$ 2 \mathrm{R}_{\mathrm{vir}} < \mathrm{r} < 3 \mathrm{R}_{\mathrm{vir}}$']
 #       plot_labels = ['$\mathrm{r} < \mathrm{R}_{200}$', \
  #                     '$\mathrm{R}_{200} < \mathrm{r} < 2 \mathrm{R}_{200}$', \
   #                    '$\mathrm{r} > 2 \mathrm{R}_{200}$']

        linestyles = ['solid', 'dashed', 'dashdot', 'dotted']
    #    linestyles = ['solid', 'dashed', 'dotted']
    fig, figax = plt.subplots(nrows = nrows, ncols = ncols, figsize=(3.5*ncols, 3.2*nrows), sharex = True, sharey = sharey)
    
    for i, ion_name in enumerate(ion_list):
        ion = ion_name.replace(" ", "")
        row = int(i/ncols)
        col = int(i - ncols*row)
        if nrows > 1:
            ax = figax[row][col]
        else:
            ax = figax[col]
        if row == nrows-1:
            ax.set_xlabel('$\mathrm{Impact\ Parameter\ (kpc)}$')
        if col == 0:
            ax.set_ylabel(ylabel)
        ax.set_xlim(2, 299)
        
        counts = np.zeros(799**2)
        for pbin, pline, plabel, color in zip(plot_bins, linestyles, plot_labels, colors):
            profile_bins = profile_data['%s_%s_rbins'%(ion, pbin)][:]
            profile = profile_data['%s_%s_%s'%(ion, pbin, yfield)][:]
            if plot_type == 'cfrac':
                ax.plot(profile_bins, profile, color = color, linestyle = pline, linewidth = linewidth, label = plabel)
                
            if plot_type == 'column':
                xbins = plot_data['%s_%s_xbins'%(ion, pbin)][:]
                ybins = plot_data['%s_%s_ybins'%(ion, pbin)][:]
                ion_counts = plot_data['%s_%s_counts'%(ion, pbin)][:]
                counts += ion_counts
                ion_counts = ion_counts.reshape(799, 799)
                ion_counts = load_combined_counts(ion, np.append(combined_output_list, output), pbin)
#                if pbin == 'dist_4':
 #                   bin_max = 250
  #              else: 
                bin_max = 300
                ipd.append_median_profile(ax, xbins[:-1], ybins[:-1], ion_counts.T, color = color, linestyle = pline, \
                                          label = plabel, alpha = 0.3, xmin = 0, xmax = bin_max, centered = True)

            
        if plot_type == 'column':
            ax.set_yscale('log')
            ylims = ipd.column_plot_ylims(ion)
            log_yrange = np.log10(ylims[1]) - np.log10(ylims[0])
 #           ax.annotate(ion_name, xy=(220, np.power(10, np.log10(ylims[0]) + 0.85*log_yrange)), fontsize=18)

            ax.set_ylim(ipd.column_plot_ylims(ion))
            if do_colormesh:
                max_counts = counts.max()
                #### warning: reshape counts are hard-coded
                counts = counts.reshape(799, 799)
                print(len(xbins), len(ybins))
                ax.pcolormesh(xbins, ybins, counts, vmin=1e-1, vmax = 0.9*max_counts, cmap='binary', norm=LogNorm())
            elif col == 0 and row == 0:
                ax.legend(loc = 'upper center')
            if sim == 'romulusC':
                if ion == 'HI' or ion == 'OVI':
                    ipd.add_cluster_observations(ax, ion, color = 'orange')
            elif sim == 'romulus25':
                ipd.plot_cos_data(ax, ion_name, color = 'orange')
                ylims = ipd.column_romulus25_ylims(ion)
                ax.set_ylim(ylims)

        elif plot_type == 'cfrac':
            ax.set_ylim(0, 1.05)
            if row == 0 and col == 0:
                ax.legend()

        # location of annotataed ion name in units of width of plot
        x_factor= 0.85
        y_factor = 0.85
        if plot_type == 'cfrac' and ion == 'HI':
            y_factor = 0.15
        ipd.annotate_ion_name(ax, ion_name, x_factor = x_factor, y_factor = y_factor)
        fig.tight_layout()
        plt.savefig('%s_%06d_multipanel_%s_halo_%s.png'%(sim, output, plot_type, bin_type), dpi = 300)
        
        


#sim = sys.argv[1]
#output = int(sys.argv[2])

plot_type_list = ['cfrac', 'column']
#plot_type_list = ['column']
#plot_type_list = ['cfrac']

ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']
ion_list = ['H I', 'C IV', 'O VI']
ion_list = ['H I', 'C IV', 'O VI']


#for plot_type in plot_type_list:
 #   multipanel_ion_plot(sim, output, ion_list, plot_type, 'mass')
  #  if sim == 'romulusC':
   #     multipanel_ion_plot(sim, output, ion_list, plot_type, 'dist', combine = False, combined_output_list = [3360, 3697])

sim = 'romulusC'
output = 3035
plot_type = 'cfrac'
multipanel_ion_plot(sim, output, ion_list, plot_type, 'dist', combine = False)

output = 3360
plot_type = 'column'
multipanel_ion_plot(sim, output, ion_list, plot_type, 'dist', combine = True, combined_output_list = [3697])
