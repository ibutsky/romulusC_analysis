import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sys
import seaborn as sns
sns.set_style("ticks", {'font.family':'serif'})

import yt
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom

def plot_metallicity_radius(append_profiles = False, output = 3035, append_observations = False, use_average_profile = False, \
                                weight_field = None, data_cut = None, profile = False, use_rvir = True):
    # metallicity vs spherical radius plot
    xfield = 'spherical_position_radius'
    yfield = 'metallicity'
    zfield = 'mass'
#    zfield = 'xray_emissivity'
    xlabel = '$\mathrm{Radius\ (kpc)}$'
    if use_rvir:
        xlabel = '$\mathrm{R\ /\ R}_{200}$'
    ylabel = '$\mathrm{Metallicity}\ (Z_{\odot})$'
    cbar_label = '$\mathrm{Relative\ Frequency}$'
    xlim = (0, 3000)
    xlim = (0, 3)
    ylim = (5e-4, 6)
    zlim = (3e-6, 1e-3)
 #   zlim = (1e-10, 1e-3)
    cmap = 'binary'
    nbins = 40
    profile_color = matplotlib.cm.get_cmap(cmap)(0.75)
    xscale = 'linear'
    profile_label = 'All Mass'

    fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output = output, weight_field = weight_field, 
                                       profile = profile, profile_label = profile_label, use_rvir = use_rvir,\
                                       profile_color = profile_color, nbins = nbins,\
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, \
                                       cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = data_cut)

    if append_observations:
        #rvir = rom.get_romulus_rvir('romulusC', output)
        rvir = rom.get_romulusC_r200(output)
        rvir = 1
        ipd.add_cluster_metallicity_observations(ax, color = 'firebrick', rvir = rvir)

    if append_profiles:
        data_list = ['hot', 'warm', 'cool', 'cold']
#        data_list = ['hot_icm', 'warm_icm', 'cool_icm', 'cold_icm']
        cmap_list = ['firebrick', 'goldenrod', 'seagreen', 'steelblue']
        title_list = ['$\mathrm{Hot\ Gas}$', '$\mathrm{Warm\ Gas}$', '$\mathrm{Cool\ Gas}$', '$\mathrm{Cold\ Gas}$']
        linestyle_list = ['solid', 'dashed', 'dashdot', 'dotted']
        nbins = [20, 20, 20, 20]
        nbins = [40, 40, 40, 40]
        for i, data_cut in enumerate(data_list):
            cmap = sns.dark_palette(cmap_list[i], as_cmap = True)
            ffig, aax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output = output, weight_field = weight_field, \
                                                 fig = fig, ax = ax, do_pcolormesh = False, \
                                                 use_average_profile = use_average_profile, use_rvir = use_rvir,\
                                                 profile = True, profile_linestyle = linestyle_list[i], \
                                                 profile_color = cmap_list[i], profile_label = title_list[i],\
                               xlabel = xlabel, ylabel = ylabel, xlim = xlim, ylim = ylim, zlim = zlim, nbins = nbins[i],\
                                   cbar_label = cbar_label, xscale = xscale, cmap = cmap, data_cut = data_cut)
        fs = 8
        ax.legend(loc = 'lower left', fontsize = fs)
    fig.tight_layout()
    plt.savefig('metallicity_radius_%06d.png'%(output), dpi = 300)



def plot_metallicity_density(output = 3035):
    # metalliciyt distribution 
    xfield = 'particle_H_nuclei_density'
    yfield = 'temperature'
    zfield = 'metallicity'
#    zfield = 'xray_intensity'
    xlabel = '$\mathrm{n}_{\mathrm{H}}\ (\mathrm{cm}^{-3})$'
    ylabel = '$\mathrm{Temperature\ (K)}$'
    cbar_label = '$\mathrm{Metallicity}\ (Z_{\odot})$'
#    cbar_label = 'xray intensity'
    xlim = (1e-8, 1e2)
    ylim = (1e3, 5e9)
    zlim = (1e-3, 5)
    cmap = 'BrBG_r'
    cmap = 'cubehelix'
    cmap = 'gist_earth'
    weight_field = 'Mass'
#    weight_field = None
#    zlim= (1e-50, 1e-35)
    fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output =  output, weight_field = weight_field, \
                                       xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
                     ylim = ylim, zlim = zlim, cbar_label = cbar_label,  cmap = cmap)

    ipd.plot_box(ax, 1e-6, 1e-2, 1e4, 1e6)
    ipd.plot_box(ax, 1e-4, .8, 2e6, 7e7) 

    fs = 13
    fs = 7
    ax.annotate('$\mathrm{Probed\ by\ UV}$\n $\mathrm{\ Absorption}$', xy = (3e-6, 5e4), fontsize = fs)
#    ax.annotate('Probed by X-ray \n \ \ Emission', xy = (2e-4, 8e6), fontsize = fs)
    ax.annotate('$\mathrm{Probed\ by\ X}$-$\mathrm{ray}$\n $\mathrm{\ \ \ Emission}$', xy = (2e-4, 8e6), fontsize = fs)                                    

    plt.savefig('metallicity_phase_%06d.png'%(output), dpi = 300)

def plot_cooling_time_ratio(output = 3035):
    xfield = 'particle_H_nuclei_density'
    yfield = 'temperature'
    zfield = 'metal_primordial_cooling_time_ratio'
    xlabel = '$\mathrm{n}_{\mathrm{H}}\ (\mathrm{cm}^{-3})$'
    ylabel = '$\mathrm{Temperature\ (K)}$'
    cbar_label = '$t_{cool, metal} / t_{cool, primordial}$'
    xlim = (1e-8, 1e2)
    ylim = (1e3, 5e9)
    zlim = (1e-2, 1)
    cmap = 'coolwarm'
    weight_field = 'Mass'
    fig, ax, im, cbar = ipd.plot_phase(xfield, yfield, zfield, output =  output, weight_field = weight_field, \
                                       xlabel = xlabel, ylabel = ylabel, xlim = xlim, \
                     ylim = ylim, zlim = zlim, cbar_label = cbar_label,  cmap = cmap)

    fs = 13
    plt.savefig('density_temperature_cooling_time_%06d.png'%(output), dpi = 300)




output = int(sys.argv[1])
#output = 3035
weight_field = None
data_cut = None
#plot_cooling_time_ratio()
plot_metallicity_radius(append_profiles = True, output = output, append_observations = True, use_rvir = True, \
                        weight_field = weight_field, data_cut = data_cut, use_average_profile = False)

#plot_metallicity_radius(append_profiles = False, output = output, append_observations = True, \
 #                       data_cut = 'hot_icm2', profile = True)

plot_metallicity_density(output = output)
