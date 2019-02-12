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

def generate_halo_column_data(sim, output, ion_list, res = 800):

    field_list = ion_help.generate_ion_field_list(ion_list, 'number_density')
    ds = yt.load('/nobackupp2/ibutsky/simulations/%s/%s.%06d'%(sim, sim, output))
    trident.add_ion_fields(ds, ions=ion_list)

    halo_props = h5.File('/nobackupp2/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')
    halo_ids = halo_props['halo_id'][:]


    for i in range(len(halo_ids)):
        halo_id = halo_ids[i]
        rvir = halo_props['rvir'][i]
        mstar = halo_props['mstar'][i]
        halo_center = halo_props['center'][i]
        center = (halo_center / ds.length_unit).d

        cdens_file = h5.File('/nobackupp2/ibutsky/data/%s/column_%i_halo%i'%(sim, output, halo_id), 'a') 
    
        width = yt.YTQuantity(2*rvir, 'kpc')
        px, py = np.mgrid[-width/2:width/2:res*1j, -width/2:width/2:res*1j]
        radius = (px**2.0 + py**2.0)**0.5

        if "px" not in cdens_file.keys():
            cdens_file.create_dataset("px", data=px.ravel())

        if "py" not in cdens_file.keys():
            cdens_file.create_dataset("py", data=py.ravel())

        if "radius" not in cdens_file.keys():
            cdens_file.create_dataset("radius", data = radius.ravel())

        if mstar > 1e9:
            print(i, halo_id, mstar)
            sys.stdout.flush()
            for axis in ['x']:#, 'y', 'z']:
                for j, ion in enumerate(ion_list):
                    dset = "%s_%s" % (ion, axis)
                    if dset not in cdens_file.keys():
                        frb = ion_help.make_projection(ds, axis, field_list, center, width, res = res)
                        cdens_file.create_dataset(dset, data=frb[field_list[j]].ravel())
                        cdens_file.flush()



sim =  sys.argv[1]
output = int(sys.argv[2])
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']

generate_halo_column_data(sim, output, ion_list)


