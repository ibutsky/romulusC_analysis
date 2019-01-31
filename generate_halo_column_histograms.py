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

def generate_ion_histograms(output, ion_list, nbins = 800, rmax = 300):
    frb = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_data2.h5'%(output), 'r')
    plot_file = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_combined_halo_ion_plot_data.h5'%(output), 'w')

    bin_name_list = ['low_mass', 'med_mass', 'high_mass', 'dist_1', 'dist_2', 'dist_3', 'dist_4']
    plot_names = ['xbins', 'ybins', 'counts', 'x_median', 'y_median', 'y_err']

    for i, ion in enumerate(ion_list):
        ion_out = ion.replace(" ", "")
        for bin_name in bin_name_list:
            print(ion, bin_name)
            r_arr = frb[('%s_rbins_%s'%(ion_out, bin_name))]
            col_arr = frb[('%s_col_%s'%(ion_out, bin_name))]
            

            # since the arrays are huge (~90 million entries), we're going to split them up
            # and calculate the counts separately (much faster) and then add them upp
            num_slices = 8
            dlen = int(len(r_arr) / num_slices)
            multiplier = np.arange(num_slices + 1)            
            counts = np.zeros((nbins-1)**2)

            for m in range(len(multiplier)-1):
                print(m)
                start = multiplier[m] * dlen
                end = multiplier[m+1] * dlen
                r = r_arr[start:end]
                col = r_arr[start:end]
                xbins, ybins, dcounts = return_histogram_data(r, col)
                counts += dcounts

            print('made histogram!')
            nbins_med = 60
            rbins = np.linspace(0, rmax, nbins_med) 
            y_median, y_err = ipd.make_profiles(r_arr, col_arr, rbins, nbins_med)
            print('made profiles!')
            
            temp_median = []
            temp_err = []
            plot_data = [xbins, ybins, counts, rbins, y_median, y_err]
            for pdata, pname in zip(plot_data, plot_names):
                dset = '%s_%s_%s'%(ion_out, pname, bin_name)
                plot_file.create_dataset(dset, data = pdata)
                plot_file.flush()

                
#### NEXT STEP: add covering fraction 
ion_list = ['H I', 'O VI', 'Si II', 'Si III', 'Si IV', 'C II', 'C III', 'C IV']
output = 3035
generate_ion_histograms(output, ion_list)














