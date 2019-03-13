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

output = int(sys.argv[1])
#output = 3035

ds = ytf.load_romulusC(output)
cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
sp = ds.sphere(cen, (500, 'kpc'))


xfield = ('gas', 'spherical_position_radius')
yfield = ('Gas', 'Mass')
pm = yt.ProfilePlot(sp, xfield, yfield, weight_field = None, accumulation = True, n_bins = 128)
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
tff = num / denom

g = G*mass_enc / rbins**2
tff = np.sqrt(2.*rbins / g)


yfield = ('gas', 'primordial_cooling_time')
pc = yt.ProfilePlot(sp, xfield, yfield, weight_field = ('Gas', 'Mass'), n_bins = 128)
pc.set_unit(xfield, 'cm')
pc.set_unit(yfield, 's')
pc.set_log(xfield, False)
print(pc.profiles[0].x)

tcool = pc.profiles[0][yfield]
y = tcool / tff

#pc.profiles[0][yfield] = y

plt.plot(rbins.in_units('kpc'), y)
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('$ t_{cool} / t_{ff}$')
#plot = yt.ProfilePlot.from_profiles(pc.profiles[0])
plt.savefig('cooling_profile_%i.png'%(output), dpi = 300)
plt.clf()

plt.plot(rbins.in_units('kpc'), tff.in_units('yr'))
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('Free Fall Time (yr)')
plt.savefig('freefall_time_profile_%i.png'%(output), dpi = 300)
plt.clf()


plt.plot(rbins.in_units('kpc'), tcool.in_units('yr'))
plt.yscale('log')
plt.xlabel('Spherical Radius (kpc)')
plt.ylabel('Primordial Cooling Time (yr)')
plt.savefig('cooling_time_profile_%i.png'%(output), dpi = 300)
