import numpy as np
import h5py as h5
import sys

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import ion_plot_definitions as ipd

def generate_ion_profiles(output, ion_list, nbins = 100, rmax = 300):
    ''' Needs ion column data to be preprocessed by generate_halo_column_data.py. 
        Takes the number output of romulusC and the list of ions and generates an h5 file
        with  the radial bins, median, median error, and covering fraction of that ion'''
    frb = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_data.h5'%(output), 'r')
    plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_profile_data.h5'%(output), 'w')

    bin_name_list = ['low_mass', 'med_mass', 'high_mass', 'dist_1', 'dist_2', 'dist_3', 'dist_4']

    for i, ion in enumerate(ion_list):
        ion_out = ion.replace(" ", "")
        for bin_name in bin_name_list:
            print(ion, bin_name)
            sys.stdout.flush()
            r_arr = frb[('%s_%s_rbin'%(ion_out, bin_name))][:]
            col_arr = frb[('%s_%s_col'%(ion_out, bin_name))][:]

            rbins = np.linspace(0, rmax, nbins)
            centered_r_bins = rbins + (rmax/nbins/2.0)

            # observational threshold of ion in absorption in UV
            # hand-wavey calculation tabulated in ion_plot_definitions
            threshold = ipd.return_observational_threshold(ion)
            y_median, y_err, covering_fraction = \
                    ipd.make_median_and_cfrac_profiles(r_arr, col_arr, rbins, nbins, threshold)
                
            
            # data to be saved in outfile (hdf5 format) and its name
            plot_data = [centered_r_bins, y_median, y_err, covering_fraction]
            plot_names = ['rbins', 'median_col', 'median_err', 'covering_fraction']

            for pdata, pname in zip(plot_data, plot_names):
                dset = '%s_%s_%s'%(ion_out, bin_name, pname)
                plot_file.create_dataset(dset, data = pdata)
                plot_file.flush()

                
#### NEXT STEP: add covering fraction 
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
#ion_list = ['O VI']
output = 3035
generate_ion_profiles(output, ion_list)














