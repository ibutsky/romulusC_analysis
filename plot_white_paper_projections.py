import matplotlib
matplotlib.use('Agg')

import yt
from yt.visualization.base_plot_types import get_multi_plot                                                                   

import h5py as h5
import numpy as np
import sys

import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes



params = {"text.color" : "white",                                                                                    
          "xtick.color" : "white",                                                                                   
          "ytick.color" : "white"}                                                                                   
plt.rcParams.update(params) 


# output is the first argument of python program
# possibilities right now are: 768 or 960
# can also hard-code this
output = int(sys.argv[1])
 
field_list = [('gas', 'H_p0_number_density'), ('gas', 'temperature')]
cmap_list = ['purple_mm', 'afmhot']
zlim_list = [(1e14, 1e20), (1e4, 1e6)]
cbar_title_list = [r'$\mathrm{H\ I\ Column\ Density}\ (\mathrm{cm^{-2}})$', r'$\mathrm{Temperature\ (K)}$']


# load pre-generated plot data
frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_plot_data'%(output), 'r')

for field, cmap, zlim, cbar_title in zip(field_list, cmap_list, zlim_list, cbar_title_list):

    # This uses yt to generate a fig/axes object. You can also use plt.subplots (see commented out line below)
    fig, axes, colorbars = get_multi_plot(1, 1, colorbar = None, bw = 4) 
    ax = axes[0][0]
#    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize=(7, 7))
    
    dset = field[1]
    img_data = np.array(frb[dset])

    im = ax.imshow(img_data, origin = 'lower', norm = LogNorm(),\
                               cmap = cmap, vmin = zlim[0], vmax = zlim[1])

    cbax = inset_axes(ax, width = "90%", height = "3%", loc = 9)
    cbar = fig.colorbar(im, cax=cbax, orientation = 'horizontal')
    cbar.set_label(cbar_title, color = 'white')

    fig.tight_layout()
    fig.savefig("romulusC_%i_%s.png"%(output, field[1]), dpi = 300)
