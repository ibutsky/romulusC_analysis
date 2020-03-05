import yt
yt.enable_parallelism()
import trident
import h5py as h5
import numpy as np
import sys

import romulus_analysis_helper as rom



field_list = [('gas', 'H_p0_number_density'), ('gas', 'temperature')]
weight_list = [None, ('gas', 'density')]
width = 5 

def get_redshift(output):
    if output == 636:
        return 3.0
    elif output == 672:
        return 2.85
    elif output == 768:
        return 2.52
    elif output == 864:
        return 2.25
    elif output == 960:
        return 2.03

def generate_projection_data(output, field_list, weight_list, width):
    sim = 'romulusC'
    rvir = rom.get_romulus_rvir(sim, output)
#    z = get_redshift(output)
#    width = width / (1. + z)
#    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/white_paper_plot_data', 'a')
    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/multipanel_romulusC_%i_plot_data'%(output), 'a')
    ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%(output))
    z = ds.current_redshift
    width = width / (1. + z)
    trident.add_ion_fields(ds, ions = ['H I'])
    cen = rom.get_romulus_yt_center(sim, output, ds)

    # set up projection plots for fields that are weighted and unweighted
    for field, weight in zip(field_list, weight_list):
        dset = field[1]
        if dset not in plot_data.keys():
            proj = yt.ProjectionPlot(ds, 'y', field, weight_field= weight, center = cen)
            proj_frb =  proj.data_source.to_frb((width, 'Mpc'), 1600)

            plot_data.create_dataset(dset, data = np.array(proj_frb[field]))
            plot_data.flush()
            
            

output = 1536
#for output in output_list:
#output_list = [768, 960]
#for output in output_list:
generate_projection_data(output, field_list, weight_list, width)


#field = ('gas', 'H_number_density')
#p = yt.ProjectionPlot(ds, 'y', field, weight_field = None, center = cen, width = (5, 'Mpc'))
