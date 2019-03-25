import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sys
import seaborn as sns
sns.set_style("ticks", {'font.family':'serif'})

import yt
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom


def plot_metallicity_radius(append_temperature_profiles = False, output = 3035, append_observations = False):
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
    cmap = 'binary'

    profile_color = matplotlib.cm.get_cmap(cmap)(0.75)
    xscale = 'linear'
    profile = True

    fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output = output, profile = profile, profile_color = profile_color, \
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, \
                               cbar_label = cbar_label, xscale = xscale, cmap = cmap)

    if append_observations:
        rvir = rom.get_romulus_rvir('romulusC', output)
        ipd.add_cluster_metallicity_observations(ax, color = 'orange', rvir = rvir)

    if append_temperature_profiles:
        data_list = ['_hot', '_warm', '_cool', '_cold']
        #data_list = ['', '', '', '']                                                                                                                                        
        cmap_list = ['firebrick', 'goldenrod', 'seagreen', 'steelblue']
        title_list = ['$\mathrm{Hot\ Gas}$', '$\mathrm{Warm\ Gas}$', '$\mathrm{Cool\ Gas}$', '$\mathrm{Cold\ Gas}$']
        linestyle_list = ['solid', 'dashed', 'dashdot', 'dotted']
        nbins = [50, 25, 25, 25]

#        data_list = ['_xray', '_uv']
#        cmap_list = ['firebrick', 'seagreen']
#        title_list = ['$\mathrm{X}$-$\mathrm{ray}$', '$\mathrm{UV}$']
#        linestyle_list = ['dashed', 'dotted']
#        nbins = [25, 25]
        for i, data_cut in enumerate(data_list):
            cmap = sns.dark_palette(cmap_list[i], as_cmap = True)
            ffig, aax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output = output, \
                                                 fig = fig, ax = ax,do_pcolormesh = False, \
                                                 profile = True, profile_linestyle = linestyle_list[i], \
                                                 profile_color = cmap_list[i], profile_label = title_list[i],\
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, nbins = nbins[i],\
                                   cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = data_cut)
        ax.legend(loc = 'lower left')
    fig.tight_layout()
    plt.savefig('metallicity_radius_%06d.png'%(output), dpi = 300)



def plot_metallicity_density(output = 3035):
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

    fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output =  output, xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
                     ylim = ylim, zlim = zlim, cbar_label = cbar_label,  cmap = cmap)

    ipd.plot_box(ax, 1e-6, 1e-2, 1e4, 1e6)
    ipd.plot_box(ax, 1e-4, .8, 2e6, 7e7) 

    fs = 13
    ax.annotate('$\mathrm{Probed\ by\ UV}$\n $\mathrm{\ Absorption}$', xy = (3e-6, 5e4), fontsize = fs)
#    ax.annotate('Probed by X-ray \n \ \ Emission', xy = (2e-4, 8e6), fontsize = fs)
    ax.annotate('$\mathrm{Probed\ by\ X}$-$\mathrm{ray}$\n $\mathrm{\ \ \ Emission}$', xy = (2e-4, 8e6), fontsize = fs)                                    

    plt.savefig('metallicity_phase_%06d.png'%(output), dpi = 300)



output = int(sys.argv[1])
plot_metallicity_radius(append_temperature_profiles = True, output = output, append_observations = True)
#plot_metallicity_density(output = output)
