import yt
yt.enable_parallelism()

import trident
import numpy as np
import os.path
import sys

sys.path.append("/nobackup/ibutsky/scripts/plot_help/")
import romulusC_analysis as rom
import yt_functions as ytf

def generate_spectra(index_start, index_end, output, sn_list = [10]):

    ds = yt.load('/nobackupp2/ibutsky/simulations/romulusC/romulusC.%06d'%(output))
    ion_list = ['H I', 'C II', 'C III', 'C IV', 'O VI']
    trident.add_ion_fields(ds, ions=ion_list)
    ds.add_field(("gas", "particle_H_nuclei_density"), function = ytf._H_nuc, \
             particle_type = True, force_override = True, units = "cm**(-3)")

    y_start = ds.domain_left_edge[2]
    y_end = ds.domain_right_edge[2]

    center = rom.get_romulusC_center(output)

    center_x = center[0]
    center_z = center[2]
    print(center_x, center_z)

    ray_id, x_list, z_list = np.loadtxt('/nobackupp2/ibutsky/data/YalePaper/spectra/coordinate_list.dat',\
                                skiprows = 1, unpack=True)

    outfile = open('/nobackup/ibutsky/data/YalePaper/spectra/romulusC_sightline_%i_extra_data.dat'%(output), 'a')
#    outfile.write('# ray_id N_{HI}, N_{CII}, N_{CIII}, N_{CIV}, N_{OVI}, T_ave, nH_ave, M_tot(Msun) \n');
    for i in range(index_start, index_end):
        x = ((x_list[i] + center_x) / ds.length_unit).d   # note: the plus is important. x_list, z_list counted from center
        z = ((z_list[i] + center_z) / ds.length_unit).d
        print(x_list[i], z_list[i], ds.length_unit)

        ray_start = [x, -0.5, z]
        ray_end = [x, 0.5, z]
        print(ray_start, ray_end)
        ray = trident.make_simple_ray(ds,
                                      start_position = ray_start,
                                      end_position = ray_end,
                                      lines='all',
                                      ftype='gas',
                                      data_filename='/nobackup/ibutsky/data/YalePaper/spectra/ray_%i_%i.h5'%(output, i))
                
        ad = ray.all_data()
        for sn in sn_list:
            for choice in[130, 160]:
                instrument = 'COS-G'+str(choice)+'M'
                sg = trident.SpectrumGenerator(instrument)
                sg.make_spectrum(ray, lines= 'all')
                sg.apply_lsf()
                sg.add_gaussian_noise(sn)
                sg.save_spectrum('/nobackup/ibutsky/data/YalePaper/spectra/romulusC_sightline_%i_%s_sn%i_%i.fits'%(output, choice, sn, i), format = 'FITS')

        H_col = (ad[('gas', 'dl')] * ad[('gas', 'H_number_density')]).sum()
        CII_col = (ad[('gas', 'dl')] * ad[('gas', 'C_p1_number_density')]).sum()
        CIII_col = (ad[('gas', 'dl')] * ad[('gas', 'C_p2_number_density')]).sum()
        CIV_col = (ad[('gas', 'dl')] * ad[('gas', 'C_p3_number_density')]).sum()
        O_col = (ad[('gas', 'dl')] * ad[('gas', 'O_p5_number_density')]).sum()

        ray = ds.ray(ray_start, ray_end)
        weight = ('gas', 'mass')
        T_ave = ray.quantities.weighted_average_quantity(('gas', 'temperature'), weight)
        rho_ave = ray.quantities.weighted_average_quantity(('gas', 'particle_H_nuclei_density'), weight)
        M_tot = ray.quantities.total_quantity(('gas', 'mass')).in_units('Msun')

        outfile.write('%i %e %e %e %e %e %e %e %e %e %e \n'%(i, H_col, CII_col, CIII_col, CIV_col, O_col, T_ave, rho_ave, M_tot, x, z))
        outfile.flush()
                      

   
index_start = int(sys.argv[1])
index_end = int(sys.argv[2])
output = int(sys.argv[3])

sn_list = [12, 13, 15, 17, 20]
sn_list = [50]
generate_spectra(index_start, index_end, output, sn_list = sn_list)

#num_points = sys.argv[3]

#num_procs = int(sys.argv[1])
#if __name__ == '__main__':
#   pool = Pool(processes=num_procs) 
#   pool.map(find_column, 1000*np.ones(num_procs, dtype=np.int8))
   #pool.map(find_column, 1000*np.ones(num_procs, dtype=np.int8), np.arange(0, num_procs, dtype=np.int8))


