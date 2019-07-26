import matplotlib
matplotlib.use('Agg')

import yt
#yt.enable_parallelism()

import trident

import numpy as np
import h5py as h5

import os, sys

import romulus_analysis_helper as rom
import ion_plot_definitions as ion_help

def generate_column_data(sim, ion_list, width=400, res = 800):

    field_list = ion_help.generate_ion_field_list(ion_list, 'number_density')
    ds, center = rom.load_charlotte_sim(sim)
    trident.add_ion_fields(ds, ions=ion_list)

    fn = '/nobackupp2/ibutsky/data/charlotte/%s_column_data.h5'%(sim)
    cdens_file = h5.File(fn)
    axis_list = ['x', 'y', 'z']
     
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
        #frb = ion_help.make_projection(ds, axis, field_list, center, width, res = res)

        for i, ion in enumerate(ion_list):
            dset = "%s_%s" % (ion.replace(" ", ""), axis)
            if dset not in cdens_file.keys():
                print(dset)
                sys.stdout.flush()
                #frb = ion_help.make_projection(ds, axis, field_list[i], center, width, res = res) 
                p = yt.ProjectionPlot(ds, axis, field_list[i], width = width, weight_field=None, center=center)
                p.set_zlim(field_list[i], 1e13, 1e5)
                p.save()
                frb = p.data_source.to_frb(width, res)
                print(frb)
                print(frb.keys())
                print(frb[field_list[i]])
                cdens_file.create_dataset(dset, data=frb[field_list[i]].d.ravel())
                cdens_file.flush()



sim =  sys.argv[1]
ion_list = ['H I', 'O VI', 'C IV']
width = 400


generate_column_data(sim,ion_list, width=width, res = 1600)


