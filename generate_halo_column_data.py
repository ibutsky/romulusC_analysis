import numpy as np
import h5py as h5
import sys

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import ion_plot_definitions as ipd


def return_histogram_data(r_arr, cdens_arr, nbins = 800, rmax = 300):
    # turns the really long 1-d combined arrays of projected radius and column density
    # into a 2d histogram. Returns xbinx, ybins, and counts.T values in 1d
    xbins = np.linspace(0, rmax, nbins)
    ylims = (1e10, 1e16)
    ybins = 10**np.linspace(np.log10(ylims[0]), np.log10(ylims[1]), nbins)
    counts, x_edge, y_edge = np.histogram2d(r_arr, cdens_arr, bins=(xbins, ybins))
    x_bin_center = ((x_edge[1:] + x_edge[:-1]) / 2).reshape(nbins-1,1)
    # normalize counts in x-space to remove out linear increase in counts with 
    # radius due to circles of constant impact parameter
    counts /= x_bin_center 
    
    return xbins, ybins, counts.T.ravel()

def generate_ion_histograms(output, ion_list, rmax = 300):

    last = 228  
    last = 5 # for testing
    out_file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_data.h5'%(output), 'a')
    plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_plot_data.h5'%(output), 'a')
    
    halo_props = h5.File('/nobackup/ibutsky/data/romulusC_halo_data_%i'%(output), 'r')
    # ignoring the 0th entry, which is the main cluster halo
    halo_list = halo_props['halo_id'].value[1:last]
    mstar_list = halo_props['mstar'].value[1:last]
    dist_list = halo_props['dist_to_cluster'].value[1:last]
    cluster_rvir = halo_props['rvir'].value[0]

    halo_mask = (mstar_list > 1e9) & (mstar_list < 1e12) & (dist_list < 3.0 * cluster_rvir)
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

        lowm_c = np.array([])
        midm_c = np.array([])
        highm_c = np.array([])

        d1_c = np.array([])
        d2_c = np.array([])
        d3_c = np.array([])
        d4_c = np.array([])

        for j, halo in enumerate(halo_list):
            print(ion, halo)

            fn = '/nobackupp2/ibutsky/data/romulusC/column_%i_halo%i'%(output, halo)
            mstar = mstar_list[j]
            dtc = dist_list[j]  # distance to cluster center
            
            r_arr, cdens_arr = ipd.load_r_cdens(fn, ion, underscore = True)

            if mstar > 1e9 and mstar < 3e9:
                lowm_r = np.concatenate((lowm_r, r_arr))
                lowm_c = np.concatenate((lowm_c, cdens_arr))

            elif mstar >= 3e9 and mstar < 1e10:
                midm_r = np.concatenate((midm_r, r_arr))
                midm_c = np.concatenate((midm_c, cdens_arr))

            elif mstar >= 1e10 and mstar < 1e12:
                highm_r = np.concatenate((highm_r, r_arr))
                highm_c = np.concatenate((highm_c, cdens_arr))

            if dtc < 0.5*cluster_rvir:
                d1_r = np.concatenate((d1_r, r_arr))
                d1_c = np.concatenate((d1_c, cdens_arr))

            elif dtc >= 0.5*cluster_rvir and dtc < cluster_rvir:
                d2_r = np.concatenate((d2_r, r_arr))
                d2_c = np.concatenate((d2_c, cdens_arr))

            elif dtc >= 0.5*cluster_rvir and dtc < cluster_rvir:
                d3_r = np.concatenate((d3_r, r_arr))
                d3_c = np.concatenate((d3_c, cdens_arr))

            elif dtc >= 1.5*cluster_rvir:
                d4_r = np.concatenate((d4_r, r_arr))
                d4_c = np.concatenate((d4_c, cdens_arr))


        name_list = ['rbins_low_mass', 'rbins_med_mass', 'rbins_high_mass', 'rbins_dist_1', 'rbins_dist_2', \
                     'rbins_dist_3', 'rbins_dist_4', 'col_low_mass', 'col_med_mass', 'col_high_mass', \
                     'col_dist_1', 'col_dist_2', 'col_dist_3', 'col_dist_4']
        plot_name_list = ['low_mass', 'med_mass', 'high_mass', 'dist_1', 'dist_2', 'dist_3', 'dist_4']
        radius_list = [lowm_r, midm_r, highm_r, d1_r, d2_r, d3_r, d4_r]
        col_list = [lowm_c, midm_c, highm_c, d1_c, d2_c, d3_c, d4_c]
        data_list = np.append(radius_list, col_list)
 
        ion_out = ion.replace(" ", "")
        for n, data in zip(name_list, data_list):
            dset = "%s_%s" % (ion_out, n)
            if dset not in out_file.keys():
                out_file.create_dataset(dset, data=data)
                out_file.flush()        


        for r_arr, col_arr, name in zip(radius_list, col_list, plot_name_list):
            xbins, ybins, counts = return_histogram_data(r_arr, col_arr)
            nbins = 50
            y_median, y_err = ipd.make_profiles(r_arr, col_arr, xbins, nbins)

            plot_data = [xbins, ybins, counts, y_median, y_err]
            plot_names = ['xbins', 'ybins', 'counts', 'y_median', 'y_err']
            for pdata, pname in zip(plot_data, plot_names):
                plot_file.create_dataset('%s_%s_%s'%(ion_out, pname, name), data = pdata)
                plot_file.flush()

            


    

ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
output = 3035
generate_ion_histograms(output, ion_list)
