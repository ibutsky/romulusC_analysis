import yt
import trident
import h5py as h5
import sys 


import yt_functions as ytf
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom_help

output = int(sys.argv[1])
#output = 

ion_list = ['H I']
ds = ytf.load_romulusC(output, ions = ion_list)

cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
sp = ds.sphere(cen, (3300, 'kpc'))
#icm = sp.cut_region(["obj[('gas', 'metallicity')] > 0"])  
icm = sp.cut_region(["(obj[('gas', 'metal_cooling_time')]>0) & (obj[('gas', 'metal_primordial_cooling_time_ratio')] > 0) & (obj[('gas', 'temperature')] >= 1e4)  & (obj[('gas', 'temperature')] <= 1e6) & (obj[('gas', 'particle_H_nuclei_density')] > 1e-6) & (obj[('gas', 'particle_H_nuclei_density')] < 1e-2)"])
#icm_mask = sp[('gas', 'particle_H_nuclei_density')] > 0.1
#icm = sp.cut_region(["obj[('gas', 'particle_H_nuclei_density')] < 0.1"])

xfield = ('gas', 'spherical_position_radius')
zfield = ('Gas', 'Mass')
yfield = ('gas', 'metal_primordial_cooling_time_ratio')
#icm =                                                                                                                                  
p = yt.PhasePlot(icm, xfield, yfield, zfield, weight_field = None)
p.set_unit(xfield, 'kpc')
p.set_unit(zfield, 'Msun')
p.set_log(xfield, False)
p.set_log(yfield, True)                                                                                                                
p.set_ylim(1e-2, 1e2)
p.save('%s_cgm'%(yfield[1]))


yfield = ('gas', 'primordial_cooling_time')

p = yt.PhasePlot(icm, xfield, yfield, zfield, weight_field = None)
p.set_unit(xfield, 'kpc')
p.set_unit(yfield, 'yr')
p.set_unit(zfield, 'Msun')
p.set_log(xfield, False)
p.set_log(yfield, True)
p.save('%s_cgm'%(yfield[1]))
p.save()

#profile = p.profiles[0]
#rbins = profile.x
#mass_enc = profile[yfield]

yfield = ('gas', 'metal_cooling_time')
p = yt.PhasePlot(icm, xfield, yfield, zfield, weight_field = None)
p.set_unit(xfield, 'kpc')
p.set_unit(yfield, 'yr')
p.set_unit(zfield, 'Msun')
p.set_log(xfield, False)
p.set_log(yfield, True)
p.save('%s_cgm'%(yfield[1]))
p.save()
    
