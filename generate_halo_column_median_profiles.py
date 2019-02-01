import numpy as np
import h5py as h5
import sys

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import ion_plot_definitions as ipd


def generate_ion_profiles(output, ion_list, nbins = 800, rmax = 300):
    frb = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_data.h5'%(output), 'r')
    plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_profile_data.h5'%(output), 'w')

    bin_name_list = ['low_mass', 'med_mass', 'high_mass', 'dist_1', 'dist_2', 'dist_3', 'dist_4']
    plot_names = ['x_median', 'y_median', 'y_err']

    for i, ion in enumerate(ion_list):
        ion_out = ion.replace(" ", "")
        for bin_name in bin_name_list:
            print(ion, bin_name)
            r_arr = frb[('%s_%s_rbin'%(ion_out, bin_name))][:]
            col_arr = frb[('%s_%s_col'%(ion_out, bin_name))][:]
            

            nbins_med = 60
            rbins_med = np.linspace(0, rmax, nbins_med)
#            centered_r_bins = rbins_med + (rmax/nbins_med/2.0)

            y_median, y_err = ipd.make_profiles(r_arr, col_arr, rbins_med, nbins_med)
                
            plot_data = [rbins_med, y_median, y_err]
            for pdata, pname in zip(plot_data, plot_names):
                dset = '%s_%s_%s'%(ion_out, bin_name, pname)
                plot_file.create_dataset(dset, data = pdata)
                plot_file.flush()

                
#### NEXT STEP: add covering fraction 
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
#ion_list = ['O VI']
output = 3035
generate_ion_profiles(output, ion_list)














