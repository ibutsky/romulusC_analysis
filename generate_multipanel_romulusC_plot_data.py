import matplotlib
matplotlib.use('Agg')

import yt
yt.enable_parallelism()
import trident
import h5py as h5
import numpy as np
import sys

from yt.visualization.base_plot_types import get_multi_plot
import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def _metallicity2(field, data):
    return data[('gas', 'metallicity')].in_units('Zsun')


output = int(sys.argv[1])
params = {"text.color" : "white", "xtick.color" : "white", "ytick.color" : "white"}               
plt.rcParams.update(params) 

field_list = [('gas', 'density'), ('Gas', 'Temperature'), ('Gas', 'metallicity2'), \
              ('gas', 'xray_intensity_0.5_7.0_keV'), ('gas', 'O_p5_number_density'), \
              ('gas', 'H_p0_number_density')]


#field_list = [('Gas', 'metallicity2'), ('gas', 'xray_intensity_0.5_7.0_keV')]
#field_list = [('gas', 'C_p2_number_density')]
#field_list = [('gas', 'O_p6_number_density'), ('gas', 'O_p7_number_density')]
weight_field = [('gas', 'density'), ('gas', 'density'), ('gas', 'density'), \
                None, None, None]

# load in simulation data and add ion fields
halo_props = h5.File('/nobackup/ibutsky/data/romulusC_halo_data_%i'%(output), 'r')
plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_data'%(output), 'a')
centers = halo_props['center'].value
ds = yt.load('/nobackup/ibutsky/romulusC/romulusC.%06d'%(output))
trident.add_ion_fields(ds, ions = ['O VI', 'H I', 'C III', 'O VII', 'O VIII'])
ds.add_field(('Gas', 'metallicity2'), function = _metallicity2, units = 'Zsun', particle_type = True)

xray_fields = yt.add_xray_emissivity_field(ds, 0.5, 7.0, redshift=ds.current_redshift, \
            cosmology=ds.cosmology, metallicity=("Gas", "metallicity2"), table_type='cloudy')
cen = (centers[0] / ds.length_unit).d

# set up projection plots for fields that are weighted and unweighted
for i in range(len(field_list)):
    proj = yt.ProjectionPlot(ds, 'y', field_list[i], weight_field = weight_field[i], center = cen)
    proj_frb =  proj.data_source.to_frb((5, 'Mpc'), 800)

    dset = field_list[i][1]
    if dset not in plot_data.keys():
        plot_data.create_dataset(dset, data = np.array(proj_frb[field_list[i]]))
        plot_data.flush()



