import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import yt
import trident
import h5py as h5
import numpy as np
import sys


output = int(sys.argv[1])

ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%output)
trident.add_ion_fields(ds, ions=['O VI'])


# load and initialize halo properties
halo_data = h5.File('/nobackup/ibutsky/data/romulusC_halo_data_%i'%(output), 'r')
centers = halo_data['center'].value
rvirs = halo_data['rvir'].value
mvirs = halo_data['mvir'].value
mstars = halo_data['mstar'].value
cluster_center = (centers[0]/ds.length_unit).d
cluster_x = cluster_center[0]
cluster_z = cluster_center[2]


# load sightline properties
# really "ray_z" and "ray_x" are in plot coordinates, not the coordinates of the simulation
ray_id_list, ray_z_list, ray_x_list = np.loadtxt('data/coordinate_list.dat', \
                                    skiprows = 1, unpack=True)

dx = ray_x_list[5]*0.1
dz = ray_z_list[5]*0.1
print(dx, dz)

zfield = ('gas', 'O_p5_number_density')
p = yt.ProjectionPlot(ds, 'y', zfield, weight_field = None, \
                      width = (6000, 'kpc'), center = cluster_center, fontsize = 18)



p.set_cmap(zfield, 'dusk')
p.set_colorbar_label(zfield, '$\mathrm{O\ VI\ Column\ Density\ (cm}^{-2})$')
p.set_zlim(zfield, 1e12, 1e15)
p.hide_axes()
p.annotate_scale()

#mass_bins = [[1e9, 3.16228e9], [3.16228e9, 1e10], [1e10, 1e15], [1e9, 1e15]]
#labels = ['low_mass', 'medium_mass', 'high_mass', 'all']

mass_bins = [[1e9, 1e15]]
labels = ['all']


for mass_range, label in zip(mass_bins, labels):
 #   p.annotate_scale()

    # annotate sightlines
    for ray_id, plot_x, plot_z in zip(ray_id_list, ray_x_list, ray_z_list):
        p.annotate_marker((plot_x,plot_z), marker = '*', coord_system = 'plot', \
                      plot_args={'color':'darkseagreen', 's':500, 'zorder':10, 'edgecolor':'black'})
#        p.annotate_text((plot_x+dx, plot_z+dx), "%i"%(ray_id), coord_system = 'plot', \
 #                       text_args={'color':'red', 'zorder':11})
    # annotate galaxy halos
    mask = (mstars > mass_range[0]) & (mstars < mass_range[1])
    for center, rvir in zip(centers[mask], rvirs[mask]):
        yt_cen = (center / ds.length_unit).d
        p.annotate_sphere(yt_cen, radius = (rvir, 'kpc'), circle_args={'color':'white', 'zorder':1})
    p.save('romulusC_%06d_projection_OVI_sightlines_halos_%s.png'%(output, label))
    p.annotate_clear()


