#also used for Keck proposal

import yt
import trident
import h5py as h5
import numpy as np
import sys
import romulus_analysis_helper as rom


sim = 'romulusC'
output= 3035
field = ('gas', 'H_p0_number_density')

plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/white_paper_plot_data', 'a')
ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%(output))
cen = rom.get_romulus_yt_center(sim, output, ds)
rvir = rom.get_romulus_rvir(sim, output)
trident.add_ion_fields(ds, ions = ['H I', 'O VI'])

p = yt.ProjectionPlot(ds, 'y', field, weight_field = None, center = cen, width = (5, 'Mpc'))
p.set_cmap(field, 'purple_mm')
p.set_zlim(field, 3e12, 1e17)
p.set_colorbar_label(field, '$\mathrm{H\ I\ Column\ Density\ (cm}^{-2})$')
p.set_font_size(26)
p.save('HI_fg2009.png')

field = ('gas', 'O_p5_number_density')
p = yt.ProjectionPlot(ds, 'y', field, weight_field = None, center = cen, width = (5, 'Mpc'))
p.set_cmap(field, 'dusk')
p.set_zlim(field, 1e13, 1e15)
p.set_colorbar_label(field, '$\mathrm{O\ VI\ Column\ Density\ (cm}^{-2})$')
p.set_font_size(26)
p.save('OVI_fg2009.png')

