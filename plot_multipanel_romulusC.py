import matplotlib
matplotlib.use('Agg')
from matplotlib.patches import Circle

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

output = int(sys.argv[1])

params = {"text.color" : "white",                                                                                    
          "xtick.color" : "white",                                                                                   
          "ytick.color" : "white"}                                                                                   
plt.rcParams.update(params) 

field_list = [('gas', 'density'), ('Gas', 'Temperature'), ('Gas', 'metallicity2'), \
              ('gas', 'xray_intensity_0.5_7.0_keV'), ('gas', 'O_p5_number_density'), \
              ('gas', 'H_p0_number_density')]
#cmap_list = ['magma', 'afmhot', 'Blues_r','bone',  'dusk', 'purple_mm']
cmap_list = ['magma', 'afmhot', 'gist_earth','bone',  'dusk', 'purple_mm']
#BrBG_r
#zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (5e-3, 5), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e17)] 
zlim_list = [(1e-30, 1e-25), (1e5, 1e8), (1e-3, 1), (1e-21, 1e-15), (1e13, 1e15), (3e12, 1e17)]


cbar_title_list =[r'$\mathrm{Density}\ (\mathrm{g\ cm^{-3}})$', \
                  r'$\mathrm{Temperature}\ (\mathrm{K})$', \
                  r'$\mathrm{Metallicity\ } (\mathrm{Z_{\odot}})$',\
                  r'$\mathrm{X-ray\ Intensity (0.5 - 7.0 keV)}\ (\frac{\mathrm{erg}}{\mathrm{arcsec}^2\mathrm{\ cm}^2 \mathrm{\ s}})$', \
                  r'$\mathrm{O\ VI\ Column\ Density}\ (\mathrm{cm^{-2}})$', \
                  r'$\mathrm{H\ I\ Column\ Density}\ (\mathrm{cm^{-2}})$']



#field_list = [('gas', 'H_p0_number_density')]
#cmap_list = ['kelp']
#zlim_list = [(1e11, 1e16)]
#cbar_title_list = [r'$\mathrm{H\ I\ Column\ Density}\ (\mathrm{cm^{-2}})$']

# load in simulation data and add ion fields

frb = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_plot_data'%(output), 'r')
print(list(frb.keys()))
#initiate figure and axes
orient = 'horizontal'
#nrows = 2
#ncols = 3

nrows = int(len(field_list)/3)
ncols = int(len(field_list)/nrows)
print(nrows, ncols)
fig, axes, colorbars = get_multi_plot(ncols, nrows, colorbar=None, bw = 4)

for i in range(nrows*ncols):
    row = int(i / ncols)
    col = i - ncols*row 
    print(row,col)
    img_data = np.array(frb[field_list[i][1]])
    print(field_list[i], img_data)
    im = axes[row][col].imshow(img_data, origin = 'lower', norm = LogNorm(),\
                               vmin = zlim_list[i][0], vmax = zlim_list[i][1])
    im.set_cmap(cmap_list[i])
    print(axes[row][col].get_xlim())
    csize = (831. / 5000.)*1600
#    circ = Circle((800,800), csize, edgecolor = 'white', fill = False, \
 #                 linestyle = (0,(5, 10)),  linewidth = 2)
  #  axes[row][col].add_patch(circ)
    circ = Circle((800,800), 2*csize, edgecolor = 'white', fill = False, \
                  linestyle = 'dotted',  linewidth = 1.5)
    axes[row][col].add_patch(circ)
    axes[row][col].xaxis.set_visible(False)
    axes[row][col].yaxis.set_visible(False)

    cbax = inset_axes(axes[row][col], width = "90%", height = "3%", loc = 9)
    cbar = fig.colorbar(im, cax=cbax, orientation = 'horizontal')
    cbar.set_label(cbar_title_list[i], color = 'white')


w = 500 * 1600. / 5000.
axes[1][0].annotate('', xy = (1200, 100),xycoords = 'data',  xytext=(1200+w, 100), textcoords='data', \
                    arrowprops=dict(arrowstyle="-", connectionstyle = "arc3", linewidth = 3, \
                    edgecolor = "white", facecolor = "white"))
axes[1][0].annotate('500 kpc', xy=(1170, 150))
# And now we're done!
fig.savefig("multipanel_plot_romulusC_%i.png"%(output))
#fig.savefig("romulusC_HI.png", dpi = 300)
