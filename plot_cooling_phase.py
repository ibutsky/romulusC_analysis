import yt
import trident
import h5py as h5
import sys 


import yt_functions as ytf
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom_help

#output = int(sys.argv[1])
output = 3035

ion_list = ['H I']
ds = ytf.load_romulusC(output, ions = ion_list)

cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
sp = ds.sphere(cen, (500, 'kpc'))
#icm_mask = sp[('gas', 'particle_H_nuclei_density')] > 0.1
icm = sp.cut_region(["obj[('gas', 'particle_H_nuclei_density')] < 0.1"])

#xfield = ("gas", "particle_H_nuclei_density")                                                                                                    


xfield = ('gas', 'spherical_position_radius')

# first calculate the cumulative mass within radius
#yfield = ('Gas', 'Mass')
#p = yt.ProfilePlot(sp, xfield, yfield, weight_field = None, accumulation = True, n_bins = 128)
#p.set_unit(xfield, 'cm')
#p.set_unit(yfield, 'g')
#p.set_log(xfield, False)

#profile = p.profiles[0]
#rbins = profile.x
#mass_enc = profile[yfield]

yfield = ('gas', 'primordial_cooling_time')
zfield = ('Gas', 'Mass')
ph = yt.PhasePlot(sp, xfield, yfield, zfield, weight_field = None)

for field in [xfield, yfield, zfield]:

    ph.set_unit(field, ytf.preferred_unit(field))
    ph.set_log(field, ytf.preferred_log(field))
        
    ph.set_cmap(zfield, 'kelp')
    ph.set_xlim(0, 500)
    
ph.save()#'/nobackup/ibutsky/plots/YalePaper/romulusC_phase_density_%s_%s_%i.png'%(ion, field, output))


