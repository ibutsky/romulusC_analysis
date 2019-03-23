import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

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
cmap = 'bone_r'
profile_color = matplotlib.cm.get_cmap(cmap)(0.75)
xscale = 'linear'
profile = True



fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, profile = profile, profile_color = profile_color, \
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, \
                               cbar_label = cbar_label, xscale = xscale, cmap = cmap)
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

#fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
 #                    ylim = ylim, zlim = zlim, cbar_label = cbar_label,  cmap = cmap)

#ipd.plot_box(ax, 1e-6, 1e-2, 1e4, 1e6)
#ipd.plot_box(ax, 1e-4, .8, 2e6, 7e7) 

fs = 13
#ax.annotate('$\mathrm{Probed\ by\ UV}$\n $\mathrm{\ Absorption}$', xy = (3e-6, 5e4), fontsize = fs)
#ax.annotate('Probed by X-ray \n \ \ Emission', xy = (2e-4, 8e6), fontsize = fs)
#ax.annotate('$\mathrm{Probed\ by\ X}$-$\mathrm{ray}$\n $\mathrm{\ \ \ Emission}$', xy = (2e-4, 8e6), fontsize = fs)                                    

#plt.savefig('metallicity_phase.png', dpi = 300)


