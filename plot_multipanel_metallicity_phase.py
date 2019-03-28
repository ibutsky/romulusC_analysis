import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
from  matplotlib.colors import ListedColormap
import seaborn as sns
sns.set_style("ticks", {'font.family':'serif'})

import yt
import romulus_analysis_helper as rom
import ion_plot_definitions as ipd
import sys


output = int(sys.argv[1])

fig, axes = plt.subplots(ncols = 2, nrows = 2, figsize = (9, 7.5), sharex = True, sharey = True)


# metallicity vs spherical radius plot
xfield = 'spherical_position_radius'
yfield = 'metallicity'
zfield = 'mass'
xlabel = '$\mathrm{Radius\ (kpc)}$'
ylabel = '$\mathrm{Metallicity}\ (Z_{\odot})$'
cbar_label = '$\mathrm{Relative\ Frequency}$'
xlim = (0, 3000)
ylim = (5e-4, 6)
zlim = (3e-6, 9e-2)
cmap = "Reds"

profile_color = 'black'
xscale = 'linear'
profile = True
profile_label ='mass-weighted'
profile_linestyle = 'dashed'

data_list = ['hot', 'warm', 'cool', 'cold']
cmap_list = ['firebrick', 'goldenrod', 'seagreen', 'steelblue']
title_list = ['$\mathrm{Hot\ Gas}$', '$\mathrm{Warm\ Gas}$', '$\mathrm{Cool\ Gas}$', '$\mathrm{Cold\ Gas}$'] 
nbins = [20, 20, 20, 20]

for i, data_cut in enumerate(data_list):
    row = int(i/2)
    col = i - 2*row
    ax = axes[row][col]
    cmap = sns.light_palette(cmap_list[i], as_cmap = True)
    ffig, aax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, fig = fig, ax = ax, \
                                         profile = profile, profile_label = profile_label, \
                                         profile_color = profile_color, \
                                         output = output, xlabel = xlabel, ylabel = ylabel, \
                                         xlim = xlim, ylim = ylim, zlim = zlim, nbins = nbins[i],\
                                   cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = data_cut)
    if row == 0:
        ax.set_xlabel('')
        ax.xaxis.set_ticks_position('none')
    if col == 0:
#        cbar = fig.colorbar(im, ax = ax)
        cbar.set_label('')
        cbar.set_ticklabels('')
        cbar.set_ticks(None)
        cbar.update_ticks()
    elif col == 1:
        ax.set_ylabel('')
        ax.yaxis.set_ticks_position('none')
    ax.annotate(title_list[i], xy = (300, 1.5e-3), fontsize = 14)
    rvir = rom.get_romulus_rvir('romulusC', output)
    ipd.add_cluster_metallicity_observations(ax, color = 'white', rvir = rvir)


ffig, aax, im, cbar = ipd.plot_phase(xfield, yfield, 'xray_emissivity', fig = fig, ax = axes[0][0], \
                                         profile = profile, profile_linestyle = 'dotted', \
                                         profile_label = 'X-ray weighted', \
                                         profile_color = profile_color, do_pcolormesh = False,\
                                         output = output, xlabel = xlabel, ylabel = ylabel, \
                                         xlim = xlim, ylim = ylim, zlim = zlim, nbins = nbins[i],\
                                     cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = 'hot_icm2')


axes[0][0].legend()
fig.tight_layout()
plt.savefig('multipanel_metallicity_%06d.png'%(output), dpi = 300)




