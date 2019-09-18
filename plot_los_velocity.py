import yt
yt.enable_parallelism()
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import romulus_analysis_helper as rom
import seaborn as sns

output = int(sys.argv[1])

ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%(output))

cen = rom.get_romulus_yt_center('romulusC', output, ds)

sp = ds.sphere(cen, (3, 'Mpc'))
bv = sp.quantities.bulk_velocity().in_units('km/s')

ad = sp.cut_region("(obj[('gas', 'temperature')]  >= 1e4) & (obj[('gas', 'temperature')] <= 1e6)")


vx = ad['velocity_x'].in_units('km/s') - bv[0]
vy = ad['velocity_y'].in_units('km/s') - bv[1]
vz = ad['velocity_z'].in_units('km/s') - bv[2]

all_velocity = np.append(vx.d, vy.d)
all_velocity = np.append(all_velocity, vz.d)

nbins = np.linspace(-900, 900, 60)


fig, ax = plt.subplots()
ax.hist(all_velocity, bins = nbins, density = True, histtype='bar', alpha = 0.7, edgecolor = 'black')
ax.set_xlabel('LOS Velocity (km/s)')
ax.set_ylabel('Relative Frequency')
ax.set_xlim(-900, 900)
fig.tight_layout()

plt.savefig('romulusC_%06d_los_velocity_coolwarm.png'%(output), dpi = 300)
