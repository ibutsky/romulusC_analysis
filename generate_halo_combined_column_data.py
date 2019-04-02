import numpy as np
import h5py as h5
import sys
import os

import ion_plot_definitions as ipd
import romulus_analysis_helper as rom

def combine_halo_column_densities(sim, output, ion_list, rmax = 300, mask = None):

    if mask == 'high_mass':
        out_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data_high_mass.h5'%(sim, output), 'w')
    else:
        out_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data.h5'%(sim, output), 'w')
    
    halo_props = h5.File('/nobackup/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')
    # ignoring the 0th entry, which is the main cluster halo
    halo_list = halo_props['halo_id'].value
    mstar_list = halo_props['mstar'].value
    dist_list = halo_props['dist_to_cluster'].value
#    cluster_rvir = halo_props['rvir'].value[0]
    cluster_rvir = rom.get_romulusC_r200(output)
    print(cluster_rvir)
    halo_mask = (mstar_list >= 1e9) & (mstar_list < 1e12) 
    if mask == 'high_mass':
        halo_mask = (mstar_list >= 1e10) & (mstar_list <= 1e12)
    if sim == 'romulusC':
        halo_mask = halo_mask & (dist_list < 4.0 * cluster_rvir)
    halo_list = halo_list[halo_mask]
    mstar_list = mstar_list[halo_mask]
    dist_list = dist_list[halo_mask]


    for i, ion in enumerate(ion_list):

        lowm_r = np.array([])
        midm_r = np.array([])
        highm_r = np.array([])

        d1_r = np.array([])
        d2_r = np.array([])
        d3_r = np.array([])
        d4_r = np.array([])
        d5_r = np.array([])

        lowm_c = np.array([])
        midm_c = np.array([])
        highm_c = np.array([])

        d1_c = np.array([])
        d2_c = np.array([])
        d3_c = np.array([])
        d4_c = np.array([])
        d5_c = np.array([])
        
        num_low = 0
        num_med = 0
        num_high = 0

        for j, halo in enumerate(halo_list):
            print(ion, halo)
            sys.stdout.flush()

            fn = '/nobackupp2/ibutsky/data/%s/column_%i_halo%i'%(sim, output, halo)
            mstar = mstar_list[j]
            dtc = dist_list[j]  # distance to cluster center
            
            r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore = True)

            if mstar > 1e9 and mstar < 3e9:
                lowm_r = np.concatenate((lowm_r, r_arr))
                lowm_c = np.concatenate((lowm_c, cdens_arr))
                num_low += 1

            elif mstar >= 3e9 and mstar < 1e10:
                midm_r = np.concatenate((midm_r, r_arr))
                midm_c = np.concatenate((midm_c, cdens_arr))
                num_med += 1

            elif mstar >= 1e10 and mstar < 1e12:
                highm_r = np.concatenate((highm_r, r_arr))
                highm_c = np.concatenate((highm_c, cdens_arr))
                num_high += 1
                
            if sim == 'romulusC':
                if dtc < 500:
                    d1_r = np.concatenate((d1_r, r_arr))
                    d1_c = np.concatenate((d1_c, cdens_arr))

                elif dtc >= 500 and dtc < 1000:
                    d2_r = np.concatenate((d2_r, r_arr))
                    d2_c = np.concatenate((d2_c, cdens_arr))

                elif dtc >= 1000 and dtc < 2000:
                    d3_r = np.concatenate((d3_r, r_arr))
                    d3_c = np.concatenate((d3_c, cdens_arr))

                elif dtc >= 2000 and dtc < 3000: 
                    d4_r = np.concatenate((d4_r, r_arr))
                    d4_c = np.concatenate((d4_c, cdens_arr))

                if dtc > 3000:
                    d5_r = np.concatenate((d5_r, r_arr))
                    d5_c = np.concatenate((d5_c, cdens_arr))
        print('analyzed %i low-mass, %i med-mass, and %i high-mass galaxies'%(num_low, num_med, num_high))

        name_list = ['low_mass', 'med_mass', 'high_mass']

        radius_list = [lowm_r, midm_r, highm_r]
        col_list = [lowm_c, midm_c, highm_c]
        
        if sim == 'romulusC':
            name_list = np.append(name_list, ['dist_1', 'dist_2', 'dist_3', 'dist_4', 'dist_5'])
            radius_list = np.append(radius_list, [d1_r, d2_r, d3_r, d4_r, d5_r])
            col_list = np.append(col_list, [d1_c, d2_c, d3_c, d4_c, d5_c])

        ion_out = ion.replace(" ", "")
        for dcol, drad, dname in zip(col_list, radius_list, name_list):
            dset = "%s_%s" % (ion_out, dname)
            # if dset not in out_file.keys():
            out_file.create_dataset("%s_col"%(dset), data=dcol)
            out_file.create_dataset("%s_rbin"%(dset), data=drad)
            out_file.flush()        
    

ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']

ion_list = ['H I', 'O VI', 'C IV']
sim = sys.argv[1]
output = int(sys.argv[2])

combine_halo_column_densities(sim, output, ion_list)#, mask = 'high_mass')
