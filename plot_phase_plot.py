import matplotlib 
matplotlib.use('Agg')
import matplotlib.pylab as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.colorbar as cb
import numpy as np

import seaborn as sns
sns.set_style("ticks", {'font.family':'serif'})
#sns.set_style("white",{'font.family':'serif', 'axes.grid': True, "ytick.major.size": 0.1,
 #               "ytick.minor.size": 0.05,
  #              'grid.linestyle': '--'})

import yt
from yt.visualization.base_plot_types import get_multi_plot
import h5py as h5
import ion_plot_definitions as ipd

def plot_box(ax, xmin, xmax, ymin, ymax, color = 'black', linestyle = 'dashed'):
    ax.plot([xmin, xmax], [ymin, ymin], color = color, linestyle = linestyle)
    ax.plot([xmin, xmax], [ymax, ymax], color = color, linestyle = linestyle)
    ax.plot([xmin, xmin], [ymin, ymax], color = color, linestyle = linestyle)
    ax.plot([xmax, xmax], [ymin, ymax], color = color, linestyle = linestyle)


def plot_phase(xfield, yfield, zfield, profile = False, xlabel = None, ylabel = None, \
               xlim = None, ylim = None, zlim = None, cmap = 'viridis', xscale = 'log',\
               yscale = 'log', cbar_label = None, fig = None, ax = None):
    output = 3035
    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_phase_data_%s_%s_%s.h5'\
                    %(output, xfield, yfield, zfield), 'r')
    
    x = plot_data[xfield].value
    y = plot_data[yfield].value
    z = plot_data[zfield].value

    res = 256
    px, py = np.mgrid[x.min():x.max():res*1j, y.min():y.max():res*1j]
    zravel = z.T.ravel()
    xravel = px.ravel()

    print(z.min(), z.max())
    
    if fig == None:
        fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize=(6, 5))

    if xlabel == None:
        ax.set_xlabel(xfield)
    else:
        ax.set_xlabel(xlabel)

    if ylabel == None:
        ax.set_ylabel(yfield)
    else:
        ax.set_ylabel(ylabel)

    if xlim:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim:
        ax.set_ylim(ylim[0], ylim[1])
    
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)


    #cbax = inset_axes(ax, width = "90%", height = "3%", loc = 'lower center')
    
    im = ax.pcolormesh(x, y, z.T, norm = LogNorm(), cmap = cmap, vmin = zlim[0], vmax = zlim[1])
    if profile:
        xbins, med, avg, lowlim, uplim = ipd.phase_median_frequency_profile(x, y, z)

        ax.plot(xbins, med, color = 'black', linestyle= 'dashed')
        ax.fill_between(xbins, lowlim, uplim, color = 'black', alpha = 0.5)

#        ax.plot(xbins, med + std)
 #       ax.plot(xbins, med - std)

    cbar = fig.colorbar(im, ax = ax, orientation = 'vertical', pad = 0)
    if cbar_label == None:
        cbar.set_label(zfield)
    else:
        cbar.set_label(cbar_label)
    #cbax.xaxis.set_ticks_position('top')          
    #cbax.xaxis.set_label_position('top')  
    if zlim == None:
        zlim = (z.min(), z.max())
    fig.tight_layout()
    return fig, ax, im, cbar
    




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
cmap = 'bone_r'
xscale = 'linear'
profile = True



fig, ax, im, cbar = plot_phase(xfield, yfield, zfield, profile = profile, xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
                     ylim = ylim, zlim = zlim, cbar_label = cbar_label, xscale = xscale, cmap = cmap)
plt.savefig('metallicity_radius.png', dpi = 300)




# metalliciyt distribution 
xfield = 'particle_H_nuclei_density'
yfield = 'temperature'
zfield = 'metallicity'
xlabel = '$\mathrm{n}_{\mathrm{H}}\ (\mathrm{cm}^{-3})$'
ylabel = '$\mathrm{Temperature\ (K)}$'
cbar_label = '$\mathrm{Metallicity}\ (Z_{\odot})$'
xlim = (1e-8, 1e2)
ylim = (1e3, 5e9)
zlim = (1e-3, 5)
cmap = 'BrBG_r'
cmap = 'cubehelix'
cmap = 'gist_earth'
#cmap = 'cividis'
#fig, ax, im, cbar = plot_phase(xfield, yfield, zfield, xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
 #                    ylim = ylim, zlim = zlim, cbar_label = cbar_label,  cmap = cmap)

plot_box(ax, 1e-6, 1e-2, 1e4, 1e6)
plot_box(ax, 1e-4, .8, 2e6, 7e7) 

fs = 13
ax.annotate('$\mathrm{Probed\ by\ UV}$\n $\mathrm{\ Absorption}$', xy = (3e-6, 5e4), fontsize = fs)
#ax.annotate('Probed by X-ray \n \ \ Emission', xy = (2e-4, 8e6), fontsize = fs)
ax.annotate('$\mathrm{Probed\ by\ X}$-$\mathrm{ray}$\n $\mathrm{\ \ \ Emission}$', xy = (2e-4, 8e6), fontsize = fs)                                    

#plt.savefig('metallicity_phase.png', dpi = 300)


