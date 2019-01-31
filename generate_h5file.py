import matplotlib

import yt
yt.enable_parallelism()

import trident

import numpy as np
import h5py as h5

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/nobackup/ibutsky/scripts/plot_help')
import romulusC_analysis as rom_help
import ion_plot_definitions as ion_help

def generate_hdf5_file(output, ion_list, width):

    field_list = ion_help.generate_ion_field_list(ion_list, 'number_density')
    print(field_list)
    ds = yt.load('/nobackupp2/ibutsky/romulusC/romulusC.%06d'%(output))
    
    trident.add_ion_fields(ds, ions=ion_list)
    cdens_file = h5.File('/nobackupp2/ibutsky/data/romulusC/column_%d.h5'%(output), 'a')
    
    width = yt.YTQuantity(width, 'kpc')
    res = 800 #standard for projection plots
    px, py = np.mgrid[-width/2:width/2:res*1j, -width/2:width/2:res*1j]
    radius = (px**2.0 + py**2.0)**0.5

    center_kpc = rom_help.get_romulusC_center(output)
    center = (center_kpc / ds.length_unit).d
    print(center_kpc, center)

    if "px" not in cdens_file.keys():
        cdens_file.create_dataset("px", data=px.ravel())

    if "py" not in cdens_file.keys():
        cdens_file.create_dataset("py", data=py.ravel())

    if "radius" not in cdens_file.keys():
        cdens_file.create_dataset("radius", data = radius.ravel())

    for axis in ['x', 'y', 'z']:
        frb = ion_help.make_projection(ds, axis, field_list, center, width)

        for i, ion in enumerate(ion_list):
            dset = "%s %s" % (ion, axis)
            if dset not in cdens_file.keys():
                cdens_file.create_dataset(dset, data=frb[field_list[i]].ravel())
                cdens_file.flush()



#output = int(sys.argv[1])
ion_list = ['H I', 'O VI', 'Mg II', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
width = 5000

output_list = [3035, 3360, 3697]
for output in output_list:
    generate_hdf5_file(output, ion_list, width)


