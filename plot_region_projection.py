import matplotlib
matplotlib.use('Agg')

import yt
yt.enable_parallelism()
import trident
import h5py as h5
import numpy as np

from yt.visualization.base_plot_types import get_multi_plot
import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import sys

region = sys.argv[1]
output = int(sys.argv[2])

params = {"text.color" : "white",                                                                                    
          "xtick.color" : "white",                                                                                   
          "ytick.color" : "white"}                                                                                   
plt.rcParams.update(params) 

ray_list = [0, 3, 6, 8, 10, 11, 12, 13, 14, 15] #original
ray_list = [0, 6, 8, 15]
ray_list = [5, 6, 7]


data_width = 1200 #hardcoded

width = 600
rmin = 0 + width/2
rmax = data_width - 600/2

field = ('gas', 'O_p5_number_density')
cmap = 'magma'

#zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (5e-3, 5), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e17)] 
#zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (5e-3, 5), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e15)]

cbar_title = r'$\mathrm{O\ VI\ Column Density}\ (\mathrm{cm^{-2}})$'
zlims = (1e10, 5e14) #original
zlims = (1e11, 7e14)

# load in simulation data and add ion fields

if region == 'romulusC':
    frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_sightline_plot_data'%(output), 'r')
else:
    frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_sightline_plot_data'%(output), 'r')

orient = 'horizontal'

if len(ray_list) <= 4:
    nrows = 1
    ncols = len(ray_list)
else:
    nrows = 2
    ncols = int (len(ray_list) / nrows)
fig, axes, colorbars = get_multi_plot(ncols, nrows, colorbar=None, bw = 4)

for i, ray_id in enumerate(ray_list):
    row = int(i / ncols)
    col = i - ncols*row 
    print(row,col)
    img_data = np.array(frb['ray_%i_%s'%(ray_id, field[1])])

    ax = axes[row][col]
        
    im = ax.imshow(img_data, origin = 'lower', norm = LogNorm(), extent=[rmin, rmax, rmin, rmax],\
                               vmin = zlims[0], vmax = zlims[1])
    im.set_cmap(cmap)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    if i == 0:
        cbax = inset_axes(ax, width = "90%", height = "3%", loc = 9)
        cbar = fig.colorbar(im, cax=cbax, orientation = 'horizontal')
        cbar.set_label(cbar_title, color = 'white')


# And now we're done!
fig.savefig("multipanel_plot_romulusC_%i_sightlines.png"%(output))
