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

def generate_column_data(sim, output, ion_list, width, res = 800, cluster_center = True, ionization_table = 'hm2012'):

    field_list = ion_help.generate_ion_field_list(ion_list, 'number_density')
    ds = yt.load('/nobackupp2/ibutsky/simulations/%s/%s.%06d'%(sim, sim, output))
    
    trident.add_ion_fields(ds, ions=ion_list)

    # "regular" column density measured as impact parameter from cluster center
    if cluster_center:
        fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_column_data.h5'%(sim, sim, output)
        if ionization_table == 'fg2009':
            fn = '/nobackupp2/ibutsky/data/%s/%s.%06d_fg2009_column_data.h5'%(sim, sim, output)
        cdens_file = h5.File(fn)
        print(list(cdens_file.keys()))
        center = rom_help.get_romulus_yt_center(sim, output, ds)
        axis_list = ['x', 'y', 'z']
        print('using cluster center')

    else:
        cdens_file = h5.File('/nobackupp2/ibutsky/data/%s/%s.%06d_column_data_special_regions.h5'%(sim, sim, output), 'a')
        id_list, center_x, center_y, width_list = \
                np.loadtxt('/nobackup/ibutsky/data/YalePaper/%s.%06d_gas_rich_y_coordinate_list.dat', skiprows=2)
        axis_list = ['y']

    width = yt.YTQuantity(width, 'kpc')
    px, py = np.mgrid[-width/2:width/2:res*1j, -width/2:width/2:res*1j]
    radius = (px**2.0 + py**2.0)**0.5
    
    if "px" not in cdens_file.keys():
        cdens_file.create_dataset("px", data=px.ravel())

    if "py" not in cdens_file.keys():
        cdens_file.create_dataset("py", data=py.ravel())

    if "radius" not in cdens_file.keys():
        cdens_file.create_dataset("radius", data = radius.ravel())

    for axis in axis_list:
#        frb = ion_help.make_projection(ds, axis, field_list, center, width, res = res)

        for i, ion in enumerate(ion_list):
            dset = "%s_%s" % (ion.replace(" ", ""), axis)
            if dset not in cdens_file.keys():
                print(dset)
                sys.stdout.flush()
                frb = ion_help.make_projection(ds, axis, field_list[i], center, width, res = res) 
                cdens_file.create_dataset(dset, data=frb[field_list[i]].ravel())
                cdens_file.flush()



sim =  sys.argv[1]
output = int(sys.argv[2])
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
ion_list = ['H I', 'O VI', 'C IV']
width = 6000


generate_column_data(sim, output, ion_list, width, res = 1600, ionization_table = 'fg2009')


