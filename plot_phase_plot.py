import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
from matplotlib.colors import LogNorm
import matplotlib.colorbar as cb

import seaborn as sns
sns.set_style("white",{'font.family':'serif', 'axes.grid': True, "ytick.major.size": 0.1,
                "ytick.minor.size": 0.05,
                'grid.linestyle': '--'})

import yt
from yt.visualization.base_plot_types import get_multi_plot
import h5py as h5
import numpy 


output = 3035
xfield = 'spherical_position_radius'
yfield = 'metallicity'
zfield = 'mass'

plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_phase_data_%s_%s_%s_3.h5'\
                      %(output, xfield, yfield, zfield), 'r')


x = plot_data[xfield].value
y = plot_data[yfield].value
z = plot_data[zfield].value
print(z.min(), z.max())

fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize=(5, 4.5))
#fig, axes, colorbars = get_multi_plot(1, 1, colorbar=None, bw = 4)
#ax = axes[0][0]

ax.set_xlabel('$\mathrm{Radius\ (kpc)}$')
ax.set_ylabel('$\mathrm{Metallicity}\ (Z_{\odot})$')
ax.set_xlim(0, 3000)
ax.set_ylim(1e-4, 6)
ax.set_yscale('log')
ax.pcolormesh(x, y, z.T, norm = LogNorm(), cmap = 'bone_r', vmin = 1e-5, vmax = 1e-2)

fig.tight_layout()
plt.savefig('romulusC_%06d_metallicity_radius.png'%(output), dpi = 300)
