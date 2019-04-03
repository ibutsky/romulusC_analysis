##### use this for figure 8 in the paper #####
import yt
yt.enable_parallelism()
import trident
import h5py as h5
import numpy as np
import sys

import romulus_analysis_helper as rom

#output = int(sys.argv[1])
output = 3035

ion_list = ['O VI']
field = ('gas', 'O_p5_number_density')
weight_field = None

# load in simulation data and add ion fields
ray_id_list, x_list, z_list = np.loadtxt('data/temp_coordinate_list.dat', skiprows = 1, unpack=True)

plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_sightline_plot_data_fixed2'%(output), 'w')
center = rom.get_romulus_center('romulusC', output)

ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%(output))
trident.add_ion_fields(ds, ions = ion_list)



# set up projection plots for fields that are weighted and unweighted
# note: ray_x, ray_z ordering should be consistent with data/coordinate_list.dat

for ray_id, ray_x, ray_z in zip(ray_id_list, x_list, z_list):
    dset = 'ray_%i_%s'%(ray_id, field[1])
    if dset not in plot_data.keys():
        plot_center = [center[0]+ray_x, center[1], center[2]+ray_z]
        print(center, plot_center)
        sys.stdout.flush()
        plot_center = (plot_center / ds.length_unit).d
        proj = yt.ProjectionPlot(ds, 'y', field, weight_field = weight_field, width = (1200, 'kpc'), center = plot_center)
        proj_frb =  proj.data_source.to_frb((1200, 'kpc'), 1600)

        plot_data.create_dataset(dset, data = np.array(proj_frb[field]))
        plot_data.flush()



