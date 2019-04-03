import matplotlib
matplotlib.use('Agg')

import yt

import trident

import numpy as np
import h5py as h5

import os, sys
import romulus_analysis_helper as rom_help
import ion_plot_definitions as ion_help
import yt_functions as ytf
def generate_halo_metal_mass_data(sim, output, start_index = 0, end_index = None):

    ds = yt.load('/nobackupp2/ibutsky/simulations/%s/%s.%06d'%(sim, sim, output))
    ds.add_field(('gas', 'metal_mass'), function = ytf._metal_mass, \
                 display_name = 'Metal Mass', particle_type = True, units =  'Msun')

    halo_props = h5.File('/nobackupp2/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')
    halo_ids = halo_props['halo_id'][:]
    
    fn = '/nobackupp2/ibutsky/data/YalePaper/%s.%06d_halo_metal_mass.dat'%(sim, output)
    if os.path.isfile(fn):
        outfile = open(fn, 'a')
    else:
        outfile = open(fn, 'w')
        outfile.write('# halo_id, metal_mass (Msun) stellar_mass (Msun) Mvir (Msun)  dist_to_cluster (kpc)\n')

    if end_index == None:
        end_index = len(halo_ids)
    for i in range(len(halo_ids)):
        halo_id = halo_ids[i]
        rvir = halo_props['rvir'][i]
        mstar = halo_props['mstar'][i]
        halo_center = halo_props['center'][i]
        mvir = halo_props['mvir'][i]
        dist_to_cluster = halo_props['dist_to_cluster'][i]
        center = (halo_center / ds.length_unit).d
        
        
        print(halo_id, mstar)
        sys.stdout.flush()
        sp = ds.sphere(center, (rvir, 'kpc'))
        metal_mass = sp.quantities.total_quantity([('gas', 'metal_mass')])
#        print("%e %e")%(metal_mass, metal_mass / mstar) 
        print("%e"%(metal_mass))
        sys.stdout.flush()

        outfile.write("%i %e %e %e %e\n"%(halo_id, metal_mass, mstar, mvir, dist_to_cluster))
        outfile.flush()


sim =  sys.argv[1]
output = int(sys.argv[2])

generate_halo_metal_mass_data(sim, output)


