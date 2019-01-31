import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import seaborn as sns

import numpy as np
import h5py as h5


# redshift 0.3 output of romulusC
output = 3035

for ray_id in range(11):
    plot_data = h5.File('/nobackupp2/ibutsky/data/YalePaper/romulusC.%06d_\
sightline_%i_plot_data.h5'%(output, ray_id), 'r')

    # see all of the available arrays in the file
    # naming convention: O_p5_number_density = O VI number density
    print(list(plot_data.keys()))
    
    # Position along the ray (along the y-axis). 0 = cluster center
    y = plot_data['y'].value
    temperature = plot_data['temperature'].value
    # size of cell along sightline
    dl = plot_data['dl'].value

    # O VI and H I column densities
    ocol = dl * plot_data['O_p5_number_density'].value
    hcol = dl * plot_data['H_number_density'].value

    # example plot
    fig, ax = plt.subplots(nrows = 3, ncols = 1 , figsize = (10, 10), sharex=True, sharey=False)
    ax[0].scatter(y, temperature)
    ax[0].set_yscale('log')
    ax[0].set_xlim(-3000, 3000)
    ax[0].set_ylim(3e2, 1e8)
    ax[0].set_xlabel('Lightray Trajectory (kpc)')
    ax[0].set_ylabel('Temperature (K)')

    ax[1].scatter(y, np.cumsum(hcol), label = 'Cumulative H I Column Density')
    ax[1].scatter(y, hcol, label = 'Local H I Column Density')
    ax[1].set_yscale('log')
    ax[1].set_ylim(1e3, 1e15)
    ax[1].set_xlabel('Lightray Trajectory (kpc)')
    ax[1].set_ylabel('H I Column Density')
    ax[1].legend()

    ax[2].scatter(y, np.cumsum(ocol), label = 'Cumulative O VI Column Density')
    ax[2].scatter(y, ocol, label = 'Local O VI Column Density')
    ax[2].set_yscale('log')
    ax[2].set_ylim(1e3, 1e15)
    ax[2].set_xlabel('Lightray Trajectory (kpc)')
    ax[2].set_ylabel('O VI Column Density')
    ax[2].legend()

    fig.tight_layout()
    plt.savefig('/nobackup/ibutsky/plots/YalePaper/romulusC.%06d_sightline_%i_multipanel.png'%(output, ray_id))
    plt.clf()
        
                      

