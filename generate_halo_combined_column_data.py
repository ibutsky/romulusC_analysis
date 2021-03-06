import numpy as np
import h5py as h5
import sys
import os

import ion_plot_definitions as ipd
import romulus_analysis_helper as rom

def combine_halo_column_densities(sim, output, ion_list, rmax = 300, mask = None, suffix = '_600'):

    if mask == 'high_mass':
        out_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data_high_mass%s.h5'%(sim, output, suffix), 'w')
    else:
        out_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data%s.h5'%(sim, output, suffix), 'w')
    
    halo_props = h5.File('/nobackup/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')
    # ignoring the 0th entry, which is the main cluster halo
    halo_list = halo_props['halo_id'].value
    mstar_list = halo_props['mstar'].value
    dist_list = halo_props['dist_to_cluster'].value
    contamination = halo_props['contamination'].value
#    cluster_rvir = halo_props['rvir'].value[0]
    cluster_rvir = rom.get_romulusC_r200(output)

    print(cluster_rvir)
    halo_mask = (contamination < 0.05) & (mstar_list >= 1e9) & (mstar_list < 1e12)
    if mask == 'high_mass':
        halo_mask = (mstar_list >= 1e10) & (mstar_list <= 1e12)
#    if sim == 'romulusC':
#        halo_mask = halo_mask & (dist_list < 4.0 * cluster_rvir)
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

        r1_r = np.array([])
        r2_r = np.array([])
        r3_r = np.array([])
        r4_r = np.array([])
        r5_r = np.array([])
        r6_r = np.array([])
        r7_r = np.array([])

        lowm_c = np.array([])
        midm_c = np.array([])
        highm_c = np.array([])

        d1_c = np.array([])
        d2_c = np.array([])
        d3_c = np.array([])
        d4_c = np.array([])

        r1_c = np.array([])
        r2_c = np.array([])
        r3_c = np.array([])
        r4_c = np.array([])
        r5_c = np.array([])
        r6_c = np.array([])
        r7_c = np.array([])
        
        num_low = 0
        num_med = 0
        num_high = 0

        num_d1 = 0
        num_d2 = 0
        num_d3 = 0
        num_d4 = 0

        num_r1 = 0
        num_r2 = 0 
        num_r3 = 0
        num_r4 = 0
        num_r5 = 0
        num_r6 = 0
        num_r7 = 0

        for j, halo in enumerate(halo_list):
            print(ion, halo)
            sys.stdout.flush()

            fn = '/nobackupp2/ibutsky/data/%s/column_%i_halo%i%s'%(sim, output, halo, suffix)
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
                    num_d1 += 1

                elif dtc >= 500 and dtc < 1000:
                    d2_r = np.concatenate((d2_r, r_arr))
                    d2_c = np.concatenate((d2_c, cdens_arr))
                    num_d2 += 1

                elif dtc >= 1000 and dtc < 2000:
                    d3_r = np.concatenate((d3_r, r_arr))
                    d3_c = np.concatenate((d3_c, cdens_arr))
                    num_d3 += 1

                elif dtc >= 2000 and dtc < 3000: 
                    d4_r = np.concatenate((d4_r, r_arr))
                    d4_c = np.concatenate((d4_c, cdens_arr))
                    num_d4 += 1

                if dtc <  0.5*cluster_rvir:
                    r1_r = np.concatenate((r1_r, r_arr))
                    r1_c = np.concatenate((r1_c, cdens_arr))
                    num_r1 += 1

                elif dtc >= 0.5* cluster_rvir and dtc < cluster_rvir:
                    r2_r = np.concatenate((r2_r, r_arr))
                    r2_c = np.concatenate((r2_c, cdens_arr))
                    num_r2 += 1

                elif dtc >= cluster_rvir and dtc < 2 * cluster_rvir:
                    r3_r = np.concatenate((r3_r, r_arr))
                    r3_c = np.concatenate((r3_c, cdens_arr))
                    num_r3 += 1

                elif dtc >= 2* cluster_rvir and dtc < 3* cluster_rvir:
                    r4_r = np.concatenate((r4_r, r_arr))
                    r4_c = np.concatenate((r4_c, cdens_arr))
                    num_r4 += 1

                elif dtc >= 3* cluster_rvir and dtc < 4* cluster_rvir:
                    r5_r = np.concatenate((r5_r, r_arr))
                    r5_c = np.concatenate((r5_c, cdens_arr))
                    num_r5 += 1

                
                if dtc < cluster_rvir:
                    r6_r = np.concatenate((r6_r, r_arr))
                    r6_c = np.concatenate((r6_c, cdens_arr))
                    num_r6 += 1

                

        print('analyzed %i low-mass, %i med-mass, and %i high-mass galaxies'%(num_low, num_med, num_high))
        print('Galaxies in [d1, d2, d3, d4] = [%i, %i, %i, %i]'%(num_d1, num_d2, num_d3, num_d4))
        print('Galaxies in [r1, r2, r3, r4, r5, r6] = [%i, %i, %i, %i, %i]'%(num_r1, num_r2, num_r3, num_r4, num_r5))

        name_list = ['low_mass', 'med_mass', 'high_mass']

        radius_list = [lowm_r, midm_r, highm_r]
        col_list = [lowm_c, midm_c, highm_c]
        
        if sim == 'romulusC':
            name_list = np.append(name_list, ['dist_1', 'dist_2', 'dist_3', 'dist_4', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6'])
            radius_list = np.append(radius_list, [d1_r, d2_r, d3_r, d4_r, r1_r, r2_r, r3_r, r4_r, r5_r, r6_r])
            col_list = np.append(col_list, [d1_c, d2_c, d3_c, d4_c, r1_c, r2_c, r3_c, r4_c, r5_c, r6_c])

        ion_out = ion.replace(" ", "")
        for dcol, drad, dname in zip(col_list, radius_list, name_list):
            dset = "%s_%s" % (ion_out, dname)
            print(dset)
            sys.stdout.flush()
            # if dset not in out_file.keys():
            out_file.create_dataset("%s_col"%(dset), data=dcol)
            out_file.create_dataset("%s_rbin"%(dset), data=drad)
            out_file.flush()        
    

ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']

ion_list = ['H I', 'C IV', 'O VI']
sim = sys.argv[1]
output = int(sys.argv[2])

combine_halo_column_densities(sim, output, ion_list)#, mask = 'high_mass')
