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

import ion_plot_definitions as ipd

#output = int(sys.argv[1])
output = 3035
params = {"text.color" : "white",                                                                                    
          "xtick.color" : "white",                                                                                   
          "ytick.color" : "white"}                                                                                   
plt.rcParams.update(params) 

ray_list = [5, 6, 7]

ray_list = [2, 7, 12]
ray_list = [14, 1, 12]
ray_list = [2, 7, 12]

data_width = 1200. #hardcoded; the width of the projection that was generated
data_res  = 1599. #hardcode 
ratio = data_res / data_width

img_width = 1200 #desired width of the image
img_center = data_width / 2 # assuming range of [0, data_width]
rmin = img_center - img_width/2  # in physical units (kpc)
rmax = img_center + img_width/2

data_center = data_res / 2.
data_min = int(data_center - ratio * img_width / 2.) #in pixel units
data_max = int(data_center + ratio * img_width / 2.) 

print(rmin, rmax, data_min, data_max)
field = ('gas', 'O_p5_number_density')
cmap = 'dusk'

#zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (5e-3, 5), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e17)] 
#zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (5e-3, 5), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e15)]

cbar_title = r'$\mathrm{O\ VI\ Column\ Density}\ (\mathrm{cm^{-2}})$'
zlims = (1e10, 5e14) #original
zlims = (7e12, 1e16)

# load in simulation data and add ion fields

frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_sightline_plot_data_fixed'%(output), 'r')
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
#    img_data = ipd.crop_imshow(img_data, data_min, data_max, data_min, data_max)
    ax = axes[row][col]
    # note: the extent call makes the units of the plot 0 to 1200 (physical) instead of 0 to 1600 (number of pixels)
    print(img_data.min(), img_data.max())
    im = ax.imshow(img_data, origin = 'lower', norm = LogNorm(),vmin = zlims[0], vmax = zlims[1], \
                   extent = [rmin, rmax, rmin, rmax], zorder = 1)
    ax.scatter(600, 600, marker = '+', s = 200, c = 'white', zorder = 10)
    im.set_cmap(cmap)
    
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
 
    if i == 0:
        cbax = inset_axes(ax, width = "90%", height = "3%", loc = 9)
        cbar = fig.colorbar(im, cax=cbax, orientation = 'horizontal')
        cbar.set_label(cbar_title, color = 'white')
        ax.axhline(rmin + 0.1*img_width, rmax - 200, rmax - 100, zorder = 10)
        ax.annotate('', xy = (1000, 100),xycoords = 'data',  xytext=(1100, 100), textcoords='data', \
                    arrowprops=dict(arrowstyle="-", connectionstyle = "arc3", linewidth = 3, edgecolor = "white", facecolor = "white"))
        ax.annotate('100 kpc', xy=(970, 130))


# And now we're done!
fig.savefig("multipanel_plot_romulusC_%i_sightlines.png"%(output))
