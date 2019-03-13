import matplotlib
matplotlib.use('Agg')

import yt
import trident
import h5py as h5
import numpy as np
import sys

from yt.visualization.base_plot_types import get_multi_plot
import matplotlib.colorbar as cb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes



params = {"text.color" : "white",                                                                                    
          "xtick.color" : "white",                                                                                   
          "ytick.color" : "white"}                                                                                   
plt.rcParams.update(params) 


output = int(sys.argv[1])

field_list = [('gas', 'H_p0_number_density'), ('gas', 'temperature')]
width = 5

#cmap_list = ['dusk', 'magma', 'cubehelix', 'purple_mm']
cmap_list = ['purple_mm', 'afmhot']
zlim_list = [(1e14, 1e19), (5e4, 5e7)]
cbar_title_list = [r'$\mathrm{H\ I\ Column\ Density}\ (\mathrm{cm^{-2}})$', r'$\mathrm{Temperature\ (K)}$']

#zlim = (1e-31, 1e-24)

#frb = h5.File('/nobackup/ibutsky/data/YalePaper/white_paper_plot_data', 'r')
frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_plot_data'%(output), 'r')

print(list(frb.keys()))
#initiate figure and axes
orient = 'horizontal'
nrows = 1
ncols = 1
for field, cmap, zlim, cbar_title in zip(field_list, cmap_list, zlim_list, cbar_title_list):

    fig, axes, colorbars = get_multi_plot(ncols, nrows, colorbar = None, bw = 4) #colorbar=None

#    dset = '%s_%iMpc'%(field[1], width)
    dset = field[1]
    img_data = np.array(frb[dset])

    im = axes[0][0].imshow(img_data, origin = 'lower', norm = LogNorm(),\
                               cmap = cmap, vmin = zlim[0], vmax = zlim[1])

#    axes[0][0].xaxis.set_visible(False)
#    axes[0][0].yaxis.set_visible(False)
    cbax = inset_axes(axes[0][0], width = "90%", height = "3%", loc = 9)
    cbar = fig.colorbar(im, cax=cbax, orientation = 'horizontal')
    cbar.set_label(cbar_title, color = 'white')

#    im.set_cmap(cmap)

    # fig.savefig("white_paper_cover_%s.png"%(cmap), dpi = 300)
    fig.tight_layout()
    fig.savefig("romulusC_%i_%s.png"%(output, field[1]), dpi = 300)
