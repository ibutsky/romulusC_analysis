import matplotlib
matplotlib.use('Agg')

import yt
#yt.enable_parallelism()

import trident

import numpy as np
import h5py as h5

import os, sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append('/nobackup/ibutsky/scripts/plot_help')
import romulus_analysis_helper as rom_help
import ion_plot_definitions as ion_help

def generate_halo_column_data(sim, output, ion_list, res = 800, start_index = 0, end_index = 1000):

    field_list = ion_help.generate_ion_field_list(ion_list, 'number_density')
    ds = yt.load('/nobackupp2/ibutsky/simulations/%s/%s.%06d'%(sim, sim, output))
    trident.add_ion_fields(ds, ions=ion_list)

    halo_props = h5.File('/nobackupp2/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')
    halo_ids = halo_props['halo_id'][:]
    mstars = halo_props['mstar'][:]
    centers = halo_props['center'][:]
    contamination = halo_props['contamination'][:]

    mask = (mstars >= 1e9) & (halo_ids > 0) & (contamination < 0.05)
    
    if start_index > end_index:
        counter = -1
    else:
        counter = 1

    for i in np.arange(start_index, end_index, counter):
        halo_id = halo_ids[mask][i]
        mstar = mstars[mask][i]
        halo_center = centers[mask][i]
        center = (halo_center / ds.length_unit).d

        print(i, halo_id, mstar)
        sys.stdout.flush()

        cdens_file = h5.File('/nobackupp2/ibutsky/data/%s/column_%i_halo%i_600'%(sim, output, halo_id), 'a') 
    
        width = yt.YTQuantity(600, 'kpc')
        px, py = np.mgrid[-width/2:width/2:res*1j, -width/2:width/2:res*1j]
        radius = (px**2.0 + py**2.0)**0.5

        if "radius" not in cdens_file.keys():
            cdens_file.create_dataset("radius", data = radius.ravel())
            
        for j, ion in enumerate(ion_list):
            for axis in ['x', 'y', 'z']:
                dset = "%s_%s" % (ion, axis)
                if dset not in cdens_file.keys():
                    frb = ion_help.make_projection(ds, axis, field_list, center, width, res = res)
                    if dset not in cdens_file.keys():
                        cdens_file.create_dataset(dset, data=frb[field_list[j]].ravel())
                        cdens_file.flush()

        cdens_file.close()


sim =  'romulusC'
output = 3035
start_index = int(sys.argv[1])
end_index = int(sys.argv[2])
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
ion_list = ['H I', 'O VI', 'C IV']
#ion_list = ['C IV', 'O VI', 'H I']

generate_halo_column_data(sim, output, ion_list, start_index = start_index, end_index = end_index)


