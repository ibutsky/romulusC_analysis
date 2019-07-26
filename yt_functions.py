import yt
from yt.units.yt_array import YTQuantity
from yt import YTArray
from yt.units import *
import trident
import numpy as np

import romulus_analysis_helper as rom

def _H_nuc(field, data):
    return data["H_nuclei_density"]

def _metallicity2(field, data):
    return data[('gas', 'metallicity')].in_units('Zsun')

def _metal_mass(field, data):
    return data[('Gas', 'metallicity')] * data[('Gas', 'Mass')].in_units('Msun')

def _radial_velocity(field, data):
    bv = data.get_field_parameter('bulk_velocity')
    cen = data.get_field_parameter('center')
    print(bv, cen)

    x = (data[('gas', 'x')] - cen[0].in_units('kpc')).d
    y = (data[('gas', 'y')] - cen[1].in_units('kpc')).d
    z = (data[('gas', 'z')] - cen[2].in_units('kpc')).d
    pos = np.column_stack((x,y,z))
    pos_mag = np.linalg.norm(pos, axis = 1)

    vx = (data[('gas', 'velocity_x')] - bv[0]).in_units('km/s').d
    vy = (data[('gas', 'velocity_y')] - bv[1]).in_units('km/s').d
    vz = (data[('gas', 'velocity_z')] - bv[2]).in_units('km/s').d
    vel = np.column_stack((vx, vy, vz))
    vel_mag = np.linalg.norm(vel, axis = 1)

    cos_theta = np.sum(pos * vel, axis = 1) / (pos_mag * vel_mag)
    
    return YTArray(vel_mag * cos_theta, 'km/s')


def _CRPressure(field, data):
    crgamma = 4./3.
    return (crgamma - 1.) * data[('Gas', 'CREnergy')].d * data[('Gas', 'density')].in_units('g/cm**3').d

def _Pressure(field, data):
    gamma = 5./3.
    m_p = 1.6726219e-24  # mass of proton in grams                                                                             
    mu = 1.2
    kb = 1.38e-16 #boltzmann constant cgs                                                                                      
    u = data[('Gas', 'Temperature')].d * kb / (mu*m_p * (gamma-1.))
    return u * data[('Gas','density')].in_units('g/cm**3').d * (gamma-1.)


def _CRBeta(field, data):
    gamma = 5./3.
    m_p = 1.6726219e-24  # mass of proton in grams                                                                             
    mu = 1.2
    kb = 1.38e-16 #boltzmann constant cgs                                                                                      
    u = data[('Gas','Temperature')].d * kb / (mu*m_p * (gamma-1.))
    pressure = u * data[('Gas', 'density')].in_units('g/cm**3').d * (gamma-1.)

    crgamma = 4./3.
    return data[('gas', 'CRPressure')]/ data[('gas', 'pressure')]


def _primordial_cooling_time(field, data):
# taken from https://arxiv.org/pdf/astro-ph/9809159.pdf, equation 11
    C1 = YTQuantity(3.88e11, 's/K**(1/2)/cm**3')
    C2 = YTQuantity(5e7, 'K')
    mu = 0.6
    mH = YTQuantity(1.6726219e-24, 'g')
    fm = 0.03
    T = data[('gas', 'temperature')]
    num = C1 * mu * mH * T**(1./2.)
    denom = data[('gas', 'density')]* (1 + C2*fm/T)
    return num / denom

def _solar_cooling_time(field, data):
    C1 = YTQuantity(3.88e11, 's/K**(1/2)/cm**3')
    C2 = YTQuantity(5e7, 'K')
    mu = 0.6
    mH = YTQuantity(1.6726219e-24, 'g')
    fm = 1.0
    T = data[('gas', 'temperature')]
    num = C1 * mu * mH * T**(1./2.)
    denom = data[('gas', 'density')]* (1 + C2*fm/T)
    return num / denom


def _metal_cooling_time(field, data):
    C1 = YTQuantity(3.88e11, 's/K**(1/2)/cm**3')
    C2 = YTQuantity(5e7, 'K')
    mu = 0.6
    mH = YTQuantity(1.6726219e-24, 'g')
    T = data[('gas', 'temperature')]
    Z = data[('gas', 'metallicity')].in_units('Zsun')
    fm = 1 + 0.14*np.log(Z.d)
#    fm = np.array(fm)
#    fm[fm < 0.03] = 0.03
    num = C1 * mu * mH * T**(1./2.)
    denom = data[('gas', 'density')]* (1 + C2*fm/T)
    return num / denom

def _metal_primordial_ratio(field, data):
    return data[('gas', 'metal_cooling_time')] / data[('gas', 'primordial_cooling_time')]

def _cooling_freefall_ratio(field, data):
    return data[('gas', 'primordial_cooling_time')] / data[('gas', 'dynamical_time')]


def load_romulusC(output, ions = []): 
    ds = yt.load('/nobackup/ibutsky/simulations/romulusC/romulusC.%06d'%output)
    ad = ds.all_data()
    cen = YTArray(rom.get_romulus_center('romulusC', output), 'kpc')
    bv = rom.get_romulusC_bulk_velocity(output)
    ad.set_field_parameter('center', cen)
    ad.set_field_parameter('bulk_velocity', bv)
    add_thermal_fields(ds)
    if len(ions) > 0:
        trident.add_ion_fields(ds, ions = ions)
    return ds


def add_cr_fields(ds):
    # todo
    return 

def add_thermal_fields(ds):
    ds.add_field(("gas", "particle_H_nuclei_density"), function = _H_nuc, \
             particle_type = True, force_override = True, units = "cm**(-3)")
    ds.add_field(('gas', 'metallicity2'), function = _metallicity2, units = 'Zsun', \
             display_name = '$\mathrm{Metallicity}$', particle_type = True)
    ds.add_field(('gas', 'primordial_cooling_time'),function = _primordial_cooling_time, \
             display_name = 'Primordial Cooling Time', particle_type = True, units = 's')
    ds.add_field(('gas', 'solar_cooling_time'),function = _solar_cooling_time, \
             display_name = 'Solar Metallicity Cooling Time', particle_type = True, units =\
 's')
    ds.add_field(('gas', 'metal_cooling_time'),function = _metal_cooling_time, \
             display_name = 'Metal Cooling Time', particle_type = True, units = 's')
#    ds.add_field(('gas', 'cooling_freefall_ratio'), function = _cooling_freefall_ratio, \
 #                display_name = '$t_{cool} / t_{ff}$', particle_type = True, units = '')
    ds.add_field(('gas', 'metal_mass'), function = _metal_mass, \
                 display_name = 'Metal Mass', particle_type = True, units =  'Msun')
    ds.add_field(('gas', 'metal_primordial_cooling_time_ratio'), function = _metal_primordial_ratio, \
                 particle_type = True)
    ds.add_field(('gas', 'radial_velocity'), function = _radial_velocity, particle_type = True, units = 'km/s', display_name = 'Radial Velocity')
#    ds.add_field(('gas', 'pressure'), function=_Pressure)


def preferred_unit(field):
    if len(field) > 1:
        fname = field[1]
    else:
        fname = field

    if fname.__contains__('radius') or fname.__contains__('position'):
        unit =  'kpc'
    elif fname.__contains__('mass') or fname.__contains__('Mass'):
        unit =  'Msun'
    elif fname.__contains__('emperature'):  # to account for temperature and Temperature
        unit = 'K'
    elif fname.__contains__('time'):
        unit = 'yr'
        if fname.__contains__('ratio'):
            unit = ''
    elif fname.__contains__('ensity'):
        unit = 'g/cm**3'
        if fname.__contains__('nuclei'):
            unit = 'cm**-3'
    elif fname.__contains__('metallicity'):
        unit = 'Zsun'
    elif fname.__contains__('elocity'):
        unit = 'km/s'
    return unit


def preferred_log(field):
    if len(field) > 1:
        fname = field[1]
    else:
        fname = field

    if fname.__contains__('radius') or fname.__contains__('position'):
        return False
    elif fname in ['velocity_x', 'velocity_y', 'velocity_z']:
        return False
    else: 
        return True

def setup_phase_axes(ph, field_list, unit_list = [None, None, None], \
                     log_list = [None, None, None]):

    for field, unit, log in zip(field_list, unit_list, log_list):
        if unit:
            ph.set_unit(field, unit)
        else:
            ph.set_unit(field, preferred_unit(field))
     #   if log:
      #      ph.set_log(field, log)
      #  else:
       #     ph.set_log(field, preferred_log(field))

    
