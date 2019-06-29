import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import sys

import yt
from yt.units.yt_array import YTQuantity
import numpy as np

import yt_functions as ytf
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom_help

#output = int(sys.argv[1])
output = 3035

ds = ytf.load_romulusC(output)
cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
ad = ds.sphere(cen, (3300, 'kpc'))
#sp = ad.cut_region(["(obj[('gas', 'metal_cooling_time')]>0) & (obj[('gas', 'metal_primordial_cooling_time_ratio')] > 0) & (obj[('gas', 'temperature')] >= 1e4)  & (obj[('gas', 'temperature')] <= 1e6) & (obj[('gas', 'particle_H_nuclei_density')] > 1e-6) & (obj[('gas', 'particle_H_nuclei_density')] < 1e-2)"])

sp = ad.cut_region(["(obj[('gas', 'temperature')] >= 1e4)  & (obj[('gas', 'temperature')] <= 1e6) & (obj[('gas', 'particle_H_nuclei_density')] > 1e-6) & (obj[('gas', 'particle_H_nuclei_density')] < 1e-2)"])
#sp = ad

xfield = ('gas', 'spherical_position_radius')
yfield = ('Gas', 'Mass')
#mass enclosed needs to have all mass, not just CGM mass
pm = yt.ProfilePlot(ad, xfield, yfield, weight_field = None, accumulation = True, n_bins = 128)
pm.set_unit(xfield, 'cm')
pm.set_unit(yfield, 'g')
pm.set_log(xfield, False)

profile = pm.profiles[0]
rbins = profile.x
print(rbins)
mass_enc = profile[yfield]

G = YTQuantity(6.67e-8, 'cm**3/g/s**2')
num = np.pi * rbins**(3./2.)
denom = np.sqrt(2*G*mass_enc)
tff2 = num / denom

g = G*mass_enc / rbins**2
tff = np.sqrt(2.*rbins / g)


yfield = ('gas', 'primordial_cooling_time')
yfield2 = ('gas', 'metal_cooling_time')
pc = yt.ProfilePlot(sp, xfield, [yfield, yfield2], weight_field = ('gas', 'ones'), n_bins = 128)
pc.set_unit(xfield, 'cm')
pc.set_unit(yfield, 's')
pc.set_log(xfield, False)
print(pc.profiles[0].x)

tcool = pc.profiles[0][yfield]
tcool_metal = pc.profiles[0][yfield2]

plt.plot(rbins.in_units('kpc'), tcool/tff)
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('$ t_{cool, primordial} / t_{ff}$')
plt.savefig('primordial_cooling_ff_profile_cgm_%i.png'%(output), dpi = 300)
plt.clf()

plt.plot(rbins.in_units('kpc'), tcool_metal/tff)
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('$ t_{cool, metal} / t_{ff}$')
plt.savefig('metal_cooling_ff_profile_cgm_%i.png'%(output), dpi = 300)
plt.clf()

plt.plot(rbins.in_units('kpc'), tff.in_units('yr'), label = 'tff = sqrt(2r/g)')
plt.plot(rbins.in_units('kpc'), tff2.in_units('yr'), label = 'tff = wiki')
plt.legend()
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('Free Fall Time (yr)')
plt.savefig('freefall_time_profile_cgm_%i.png'%(output), dpi = 300)
plt.clf()


plt.plot(rbins.in_units('kpc'), tcool.in_units('yr'))
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('Primordial Cooling Time (yr)')
plt.savefig('primordial_cooling_time_profile_cgm_%i.png'%(output), dpi = 300)


plt.plot(rbins.in_units('kpc'), tcool_metal.in_units('yr'))
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('Metal Cooling Time (yr)')
plt.savefig('metal_cooling_time_profile_cgm_%i.png'%(output), dpi = 300)
