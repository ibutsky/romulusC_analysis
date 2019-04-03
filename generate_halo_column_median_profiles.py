import numpy as np
import h5py as h5
import sys

#sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import ion_plot_definitions as ipd

def generate_ion_profiles(sim, output, ion_list, nbins = 100, rmax = 300, mask = 'all', suffix  = '_300'):
    ''' Needs ion column data to be preprocessed by generate_halo_column_data.py. 
        Takes the number output of romulusC and the list of ions and generates an h5 file
        with  the radial bins, median, median error, and covering fraction of that ion'''
    
    if mask == 'high_mass':
        frb = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data_high_mass.h5'%(sim, output), 'r')
        plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data_high_mass.h5'%(sim, output), 'w')
    else:
        frb = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_data%s.h5'%(sim, output, suffix), 'r')
        plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/%s.%06d_combined_halo_ion_profile_data%s.h5'%(sim, output, suffix), 'w')
        
    print(list(frb.keys()))
    bin_name_list = ['low_mass', 'med_mass', 'high_mass']
    if sim == 'romulusC':
        bin_name_list = np.append(bin_name_list, ['dist_1', 'dist_2', 'dist_3', 'dist_4', 'r1', 'r2','r3', 'r4'])
    
    for i, ion in enumerate(ion_list):
        ion_out = ion.replace(" ", "")
        for bin_name in bin_name_list:
            print(ion, bin_name)
            sys.stdout.flush()
            r_arr = frb[('%s_%s_rbin'%(ion_out, bin_name))][:]
            col_arr = frb[('%s_%s_col'%(ion_out, bin_name))][:]

            # observational threshold of ion in absorption in UV
            # hand-wavey calculation tabulated in ion_plot_definitions
            centered_r_bins, y_median, y_err, covering_fraction = \
                    ipd.median_and_cfrac_profiles(ion, r_arr, col_arr, r_max = rmax, n_bins = nbins)
                
            
            # data to be saved in outfile (hdf5 format) and its name
            plot_data = [centered_r_bins, y_median, y_err, covering_fraction]
            plot_names = ['rbins', 'median_col', 'median_err', 'covering_fraction']

            for pdata, pname in zip(plot_data, plot_names):
                dset = '%s_%s_%s'%(ion_out, bin_name, pname)
                plot_file.create_dataset(dset, data = pdata)
                plot_file.flush()

                
#### NEXT STEP: add covering fraction 
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
ion_list = ['H I', 'O VI', 'C IV']
#output = 3035
sim = sys.argv[1]
output = int(sys.argv[2])
#generate_ion_profiles(sim, output, ion_list, mask = 'high_mass')
generate_ion_profiles(sim, output, ion_list)





