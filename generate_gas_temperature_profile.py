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


def make_mass_profile(ad):
    xfield = ('gas', 'spherical_position_radius')
    yfield = ('Gas', 'Mass')
    p = yt.ProfilePlot(ad, xfield, yfield, weight_field = None,  x_log = False, n_bins = 16)
    p.set_unit(xfield, 'kpc')
    p.set_unit(yfield, 'Msun')
    profile = p.profiles[0]
    rbins = profile.x
    return rbins, profile[yfield]


output = int(sys.argv[1])

ds = ytf.load_romulusC(output)
cen = rom_help.get_romulus_yt_center('romulusC', output, ds)
rvir = rom_help.get_romulus_rvir('romulusC', output)
sp = ds.sphere(cen, (3.*rvir, 'kpc'))
icm = sp.cut_region(["(obj[('gas', 'particle_H_nuclei_density')] < 0.1)"])

icm_cold = sp.cut_region(["(obj[('gas', 'particle_H_nuclei_density')] < 0.1) & (obj[('gas', 'temperature')] <= 1e4)"])
icm_cool = sp.cut_region(["(obj[('gas', 'particle_H_nuclei_density')] < 0.1) & (obj[('gas', 'temperature')]  > 1e4) & (obj[('gas', 'temperature')] <= 1e5)"])
icm_warm = sp.cut_region(["(obj[('gas', 'particle_H_nuclei_density')] < 0.1) & (obj[('gas', 'temperature')]  > 1e5) & (obj[('gas', 'temperature')] <= 1e6)"])
icm_hot  = sp.cut_region(["(obj[('gas', 'particle_H_nuclei_density')] < 0.1) & (obj[('gas', 'temperature')]  > 1e6)"])

#x_cool, y_cool = make_mass_profile(icm_cool)
#x_warm, y_warm = make_mass_profile(icm_warm)
#x_hot, y_hot = make_mass_profile(icm_hot)

xfield = ('gas', 'spherical_position_radius')
yfield = ('Gas', 'Mass')

x_cold = icm_cold[xfield].in_units('kpc')
x_cool = icm_cool[xfield].in_units('kpc')
x_warm = icm_warm[xfield].in_units('kpc')
x_hot  = icm_hot[ xfield].in_units('kpc')

y_cold = icm_cold[yfield].in_units('Msun')
y_cool = icm_cool[yfield].in_units('Msun')
y_warm = icm_warm[yfield].in_units('Msun')
y_hot  = icm_hot[ yfield].in_units('Msun')


dset_list = ['rbins_cold', 'rbins_cool',  'rbins_warm', 'rbins_hot', 'mass_cold', 'mass_cool', 'mass_warm', 'mass_hot']
data_list = [x_cold, x_cool, x_warm, x_hot, y_cold, y_cool, y_warm, y_hot]
outfile = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC_%i_gas_temperature_profile_data'%(output), 'w')
for dset, data in zip(dset_list, data_list):
    if dset not in outfile.keys():
        outfile.create_dataset(dset, data=data)
        outfile.flush()
