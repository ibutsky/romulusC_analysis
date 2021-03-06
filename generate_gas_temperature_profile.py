import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt
import h5py as h5
import sys

import yt
from yt.units.yt_array import YTQuantity
import numpy as np

import yt_functions as ytf
import ion_plot_definitions as ipd
import romulus_analysis_helper as rom_help

def _metal_mass(field, data):
    return data[('Gas', 'metallicity')] * data[('Gas', 'Mass')].in_units('Msun')

def make_mass_profile(ad, yfield = ('Gas', 'Mass')):
    xfield = ('gas', 'spherical_position_radius')
    p = yt.ProfilePlot(ad, xfield, yfield, weight_field = None,  x_log = False, n_bins = 16)
    p.set_unit(xfield, 'kpc')
    p.set_unit(yfield, 'Msun')
    profile = p.profiles[0]
    rbins = profile.x
    return rbins, profile[yfield]


output = int(sys.argv[1])
plot_type = sys.argv[2]

ds = ytf.load_romulusC(output)
ds.add_field(('gas', 'metal_mass'), function = _metal_mass, units = 'Msun', particle_type = True)

cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
rvir = rom_help.get_romulus_rvir('romulusC', output)
sp = ds.sphere(cen, (3.*rvir, 'kpc'))
icm = "(obj[('gas', 'particle_H_nuclei_density')] < 0.1)"

cold = sp.cut_region([icm + "& (obj[('gas', 'temperature')]  < 1e4)"])
cool = sp.cut_region([icm + "& (obj[('gas', 'temperature')]  >= 1e4) & (obj[('gas', 'temperature')] < 1e5)"])
warm = sp.cut_region([icm + "& (obj[('gas', 'temperature')]  >= 1e5) & (obj[('gas', 'temperature')] < 1e6)"])
hot  = sp.cut_region([icm + "& (obj[('gas', 'temperature')]  >= 1e6)"])

xfield = ('gas', 'spherical_position_radius')
if plot_type == 'gas':
    yfield = ('Gas', 'Mass')
elif plot_type == 'metal':
    yfield = ('gas', 'metal_mass')

x_cold, y_cold = make_mass_profile(cold, yfield = yfield)
x_cool, y_cool = make_mass_profile(cool, yfield = yfield)  
x_warm, y_warm = make_mass_profile(warm, yfield = yfield) 
x_hot, y_hot = make_mass_profile(hot,  yfield = yfield)

x_cold = cold[xfield].in_units('kpc')
x_cool = cool[xfield].in_units('kpc')
x_warm = warm[xfield].in_units('kpc')
x_hot  = hot[ xfield].in_units('kpc')

y_cold = cold[yfield].in_units('Msun')
y_cool = cool[yfield].in_units('Msun')
y_warm = warm[yfield].in_units('Msun')
y_hot  = hot[yfield].in_units('Msun')


dset_list = ['rbins_cold', 'rbins_cool',  'rbins_warm', 'rbins_hot', 'mass_cold', 'mass_cool', 'mass_warm', 'mass_hot']
data_list = [x_cold, x_cool, x_warm, x_hot, y_cold, y_cool, y_warm, y_hot]
if plot_type == 'gas':
    outfile = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC_%i_gas_temperature_profile_data_icm'%(output), 'w')
elif plot_type == 'metal':
    outfile = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC_%i_metal_temperature_profile_data_icm'%(output), 'w')
for dset, data in zip(dset_list, data_list):
    if dset not in outfile.keys():
        outfile.create_dataset(dset, data=data)
        outfile.flush()
