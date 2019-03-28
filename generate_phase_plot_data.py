import yt
import trident
import h5py as h5
import sys 

def _H_nuc(field, data):
    return data["H_nuclei_density"]

def _metal_mass(field, data):
    return data[('Gas', 'metallicity')] * data[('Gas', 'Mass')].in_units('Msun')

def _metallicity2(field, data):
    return data[('gas', 'metallicity')].in_units('Zsun')

def _xray_luminosity2(field, data):
    return data[('gas', 'xray_luminosity_0.5_7.0_keV')]

def _xray_intensity2(field, data):
    return data[('gas', 'xray_intensity_0.5_7.0_keV')]


import romulus_analysis_helper as rom
import yt_functions as ytf

def generate_phase_plot_data(output, xfield, yfield, zfield, icm_cut = None, weight_field = ('Gas', 'Mass'), \
                             xbins = 128, ybins = 128, fractional = False, xlim = None, ylim = None):
    sim = 'romulusC'
    ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%(output))
    ds.add_field(("gas", "particle_H_nuclei_density"), function = _H_nuc, \
             particle_type = True, force_override = True, units = "cm**(-3)")

    redshift = ds.current_redshift
    if output == 4096:
        redshift = 0.01
    ds.add_field(('Gas', 'metallicity2'), function = _metallicity2, units = 'Zsun', particle_type = True)
    xray_fields = yt.add_xray_emissivity_field(ds, 0.5, 7.0, redshift=redshift, \
                    cosmology=ds.cosmology, metallicity=("Gas", "metallicity2"), table_type='cloudy')

    ds.add_field(('gas', 'xray_luminosity'), function = _xray_luminosity2, particle_type = True)
    ds.add_field(('gas', 'xray_intensity'), function = _xray_intensity2, units = 'erg/(arcsec**2*cm**3*s)', particle_type = True)


    cen = rom.get_romulus_yt_center(sim, output, ds)
    rvir = rom.get_romulus_rvir(sim, output)
    
    icm_mask = None

    sp = ds.sphere(cen, (3.*rvir, 'kpc'))

    if icm_cut == 'xray':
        icm_mask = "(obj[('gas', 'xray_intensity')] > 1e-44)"
    elif icm_cut == 'uv':
        icm_mask = "(obj[('gas', 'particle_H_nuclei_density')] > 1e-6) & (obj[('gas', 'particle_H_nuclei_density')] > 1e-2)"
        icm_mask = "& (obj[('gas', 'temperature')] > 1e4) & (obj[('gas', 'temperature')] < 1e6)"

    elif icm_cut == 'cold':
        icm_mask = "(obj[('gas', 'temperature')] < 1e4)"
    elif icm_cut == 'cool':
        icm_mask = " (obj[('gas', 'temperature')]  >= 1e4) & (obj[('gas', 'temperature')] < 1e5)"
    elif icm_cut == 'coolwarm':
        icm_mask = "(obj[('gas', 'temperature')]  >= 1e4) & (obj[('gas', 'temperature')] <= 1e6)"
    elif icm_cut == 'warm':
        icm_mask = "(obj[('gas', 'temperature')]  >= 1e5) & (obj[('gas', 'temperature')] < 1e6)"
    elif icm_cut == 'hot':
        icm_mask = "(obj[('gas', 'temperature')] >= 1e6)"
    elif icm_cut == 'hot_icm':
        icm_mask = "(obj[('gas', 'particle_H_nuclei_density')] < 0.1) & (obj[('gas', 'temperature')] >= 1e6)"
    elif icm_cut == 'hot_icm2':
        icm_mask = "(obj[('gas', 'particle_H_nuclei_density')] < 0.01) & (obj[('gas', 'temperature')] >= 1e6)"


    
    if yfield[1] == 'metallicity':
        if icm_mask:
            icm_mask  += "& (obj[('gas', 'metallicity')] > 0)"
        else:
            icm_mask =  "(obj[('gas', 'metallicity')] > 0)"


    if icm_mask == None:
        icm = sp
    else:
        icm = sp.cut_region(icm_mask)

    ph = yt.PhasePlot(icm, xfield, yfield, zfield, weight_field = weight_field, \
                      fractional = fractional, x_bins = xbins, y_bins = ybins)
    
    for field in [xfield, yfield, zfield]:
        print(field)
        if field[1] != 'xray_emissivity':
            ph.set_log(field, ytf.preferred_log(field))
            ph.set_unit(field, ytf.preferred_unit(field))

    if ylim:
        ph.set_ylim(ylim[0], ylim[1])
    if xlim:
        ph.set_xlim(xlim[0], xlim[1])
    profile = ph.profile
    ph.save()
    
    outfile_name = '/nobackup/ibutsky/data/YalePaper/romulusC.%06d_phase_data_%s_%s_%s'\
                   %(output, xfield[1], yfield[1], zfield[1])
    if weight_field:
        outfile_name += '_%s'%(weight_field[1])
    if icm_cut:
        outfile_name += '_%s'%(icm_cut)
    outfile = h5.File(outfile_name+'.h5', 'w')

    outfile.create_dataset(xfield[1], data = profile.x)
    outfile.create_dataset(yfield[1], data = profile.y)
    outfile.create_dataset(zfield[1], data = profile[zfield])
    outfile.create_dataset('weight_field', data = str(weight_field))
    outfile.flush()
 



output = int(sys.argv[1])
icm_cut = sys.argv[2]

if icm_cut == 'None':
    icm_cut = None
#icm_cut = None
#icm_cut = 'hot_icm2'


xfield = ('gas', 'spherical_position_radius')
yfield = ('gas', 'metallicity')
zfield = ('gas', 'mass')
#zfield = ('gas', 'xray_emissivity')
weight_field = None
fractional = True
xlim = (0, 3100)
ylim = (1e-5, 15)


#weight_field = ('gas', 'xray_emissivity_0.5_7.0_keV')

#xfield = ('gas', 'particle_H_nuclei_density')
#yfield = ('gas', 'temperature')
#zfield = ('gas', 'metallicity')
#zfield = ('gas', 'xray_luminosity_0.5_7.0_keV')
#zfield = ('gas', 'xray_intensity')
#weight_field = ('Gas', 'Mass')
#fractional = False
#xlim = (5e-9, 5e2)
#ylim = (5e2, 1e10)
#icm_cut = None

nbins = 256
generate_phase_plot_data(output, xfield, yfield, zfield, icm_cut = icm_cut, weight_field = weight_field, \
                         fractional = fractional, xbins = nbins, ybins = nbins, ylim = ylim, xlim = xlim)
