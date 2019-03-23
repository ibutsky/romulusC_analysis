import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
from  matplotlib.colors import ListedColormap
import seaborn as sns
sns.set_style("ticks", {'font.family':'serif'})

import yt
import ion_plot_definitions as ipd



# metallicity vs spherical radius plot
xfield = 'spherical_position_radius'
yfield = 'metallicity'
zfield = 'mass'
xlabel = '$\mathrm{Radius\ (kpc)}$'
ylabel = '$\mathrm{Metallicity}\ (Z_{\odot})$'
cbar_label = '$\mathrm{Relative\ Frequency}$'
xlim = (0, 3000)
ylim = (5e-4, 6)
zlim = (3e-6, 1e-3)
cmap = "Reds"
#cmap = sns.color_palette("OrRd", 10, as_cmap = True)

#profile_color = matplotlib.cm.get_cmap(cmap)(0.75)
profile_color = 'black'
xscale = 'linear'
profile = True

data_cut = ''


fig, ax = plt.subplots(ncols = 2, nrows = 2, figsize = (12, 10), sharex = True, sharey = True)


data_list = ['_hot', '_warm', '_cool', '_cold']
#data_list = ['', '', '', '']
cmap_list = ['firebrick', 'goldenrod', 'seagreen', 'steelblue']
title_list = ['$\mathrm{Hot\ Gas}$', '$\mathrm{Warm\ Gas}$', '$\mathrm{Cool\ Gas}$', '$\mathrm{Cold\ Gas}$'] 
nbins = [50, 50, 50, 25]
zlim = (1e-7, 1e-3)
for i, data_cut in enumerate(data_list):
    row = int(i/2)
    col = i - 2*row
   # ax = axes[row][col]
    cmap = sns.light_palette(cmap_list[i], as_cmap = True)
    ffig, aax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, fig = fig, ax = ax[row][col], \
                                         profile = profile, profile_color = profile_color, \
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, nbins = nbins[i],\
                                   cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = data_cut)
    if row == 0:
        ax[row][col].set_xlabel('')
        ax[row][col].xaxis.set_ticks_position('none')
    ax[row][col].annotate(title_list[i], xy = (300, 1.5e-3), fontsize = 14)
fig.tight_layout()
plt.savefig('multipanel_metallicity.png', dpi = 300)




