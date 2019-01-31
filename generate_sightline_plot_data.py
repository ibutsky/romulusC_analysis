import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import seaborn as sns

import yt
yt.enable_parallelism()

import trident
import numpy as np
import h5py as h5
import os.path
import sys

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import romulusC_analysis as rom
import yt_functions as ytf
import ion_plot_definitions as ipd

def generate_spectrum_plot_data(index_start, index_end, output):
    ds = yt.load('/nobackupp2/ibutsky/romulusC/romulusC.%06d'%(output))
    ion_list = ['H I', 'C II', 'C III', 'C IV', 'Si II', 'Si III', 'Si IV', 'O VI']
    trident.add_ion_fields(ds, ions=ion_list)
    ds.add_field(("gas", "particle_H_nuclei_density"), function = ytf._H_nuc, \
             particle_type = True, force_override = True, units = "cm**(-3)")

    y_start = ds.domain_left_edge[2]
    y_end = ds.domain_right_edge[2]

    center = rom.get_romulusC_center(output)
    center_x = center[0]
    center_y = center[1]
    center_z = center[2]
    print(center_x, center_y, center_z)

    ray_id, z_list, x_list = np.loadtxt('/nobackupp2/ibutsky/data/spectra/coordinate_list.dat',\
                                skiprows = 1, unpack=True)

    for i in range(index_start, index_end):
        h5file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_sightline_%i_plot_data.h5'%(output, i), 'w')
        # note: the plus is important. x_list, z_list counted from center                              
        x = ((x_list[i] + center_x) / ds.length_unit).d   
        z = ((z_list[i] + center_z) / ds.length_unit).d
        print(x_list[i], z_list[i], ds.length_unit)
        ycen = (center_y / ds.length_unit).d

        # y from -2.5 mpc of center to 2.5 mpc from center
        ylen = (2500. / ds.length_unit).d
        ray_start = [x, ycen-ylen , z]
        ray_end = [x, ycen+ylen, z]

        ad = ds.r[ray_start:ray_end]
        ray = trident.make_simple_ray(ds,
                                      start_position = ray_start,
                                      end_position = ray_end,
                                      lines=ion_list)
        ad_ray = ray.all_data()

        field_list = ['y', 'temperature', 'density', 'metallicity', 'dl']
        source_list = [ad, ad, ad, ad, ad_ray]
        unit_list = ['kpc', 'K', 'g/cm**3', 'Zsun', 'cm']
        yt_ion_list = ipd.generate_ion_field_list(ion_list, 'number_density', full_name = False)
        yt_ion_list[0] = 'H_number_density'
        field_list = np.append(field_list, yt_ion_list)
        for j in range(len(yt_ion_list)):
            unit_list.append('cm**-3')
            source_list.append(ad_ray)

        for field,source,unit in zip(field_list, source_list, unit_list):
            if field not in h5file.keys():
                h5file.create_dataset(field, data = source[('gas', field)].in_units(unit))
                h5file.flush()
        h5file.create_dataset('y_lr', data = ad_ray['y'].in_units('kpc'))
        h5file.flush()
        print("saved sightline data %i\n"%(i))
                      

   
#index_start = int(sys.argv[1])
#index_end = int(sys.argv[2])
#output = int(sys.argv[3])
output = 3035
index_start = 9
index_end = 11
generate_spectrum_plot_data(index_start, index_end, output)

#num_points = sys.argv[3]

 #num_procs = int(sys.argv[1])
#if __name__ == '__main__':
#   pool = Pool(processes=num_procs) 
#   pool.map(find_column, 1000*np.ones(num_procs, dtype=np.int8))
   #pool.map(find_column, 1000*np.ones(num_procs, dtype=np.int8), np.arange(0, num_procs, dtype=np.int8))




