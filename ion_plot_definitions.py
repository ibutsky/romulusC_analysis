import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import numpy as np
import h5py as h5
import sys
import os.path

def return_ylims(ion):
    if ion == 'H I':
        ylims = (1e11, 1e21)
    elif ion == 'O VI':
        ylims = (1e10, 1e17)
    elif ion == 'Mg II':
        ylims = (1e2, 1e17)
    elif ion == 'C II':
        ylims = (1e5, 1e19)
    elif ion == 'C III':
        ylims = (1e7, 1e17)
    elif ion == 'C IV':
        ylims = (1e7, 1e16)
    elif ion == 'Si II':
        ylims = (1e2, 1e17)
    elif ion == 'Si III':
        ylims = (1e5, 1e16)
    elif ion == 'Si IV':
        ylims = (1e5, 1e16)
    else:
        ylims = (1e5, 1e20)
    return ylims 

def column_romulus25_ylims(ion):
    ion = ion.replace(" ", "")
    if ion == 'HI':
        ylims = (1e13, 1e17)
    elif ion == 'CIV':
        ylims = (1e11, 1e15)
    elif ion == 'OVI':
        ylims = (1e13, 1e16)
    return ylims

def column_plot_ylims(ion):
        ion = ion.replace(" ", "")
        if ion == 'HI':
                ylims = (3e12, 1e15)
        elif ion == 'OVI':
                ylims = (1e12, 7e14)
        elif ion == 'MgII':
                ylims = (1e2, 1e15)
        elif ion == 'CII':
                ylims = (8e4, 1e11)
        elif ion == 'CIII':
                ylims = (9e7, 1e12)
        elif ion == 'CIV':
                ylims = (2e10, 1e13)
        elif ion == 'SiII':
                ylims = (1e2, 9e6)
        elif ion == 'SiIII':
                ylims = (1e5, 8e11)
        elif ion == 'SiIV':
                ylims = (1e7, 9e10)
        else:
                ylims = (1e5, 1e15)
        return ylims


def return_observational_threshold(ion):
    ion = ion.replace(" ", "")
    if ion == 'HI':
        return np.power(10, 13)
    elif ion == 'OVI': 
        return np.power(10, 13.3)
    elif ion == 'SiII': 
        return np.power(10, 13) 
    elif ion == 'SiIII': 
        return np.power(10, 13)
    elif ion == 'SiIV': 
        return np.power(10, 13.3) 
    elif ion == 'CII': 
        return np.power(10, 13.5)
    elif ion == 'CIII':
        return np.power(10, 13)
    elif ion == 'CIV':
        return np.power(10,13.1)
    else:
        print("WARNING OBSERVATIONAL THRESHOLD NOT SET")
        return None


def return_ion_prefix(ion):
    if ion == 'H I':
        field = 'H_p0'
    elif ion == 'O VI':
        field = 'O_p5'
    elif ion == 'Si II':
        field = 'Si_p1'
    elif ion == 'Si III':
        field = 'Si_p2'
    elif ion == 'Si IV':
        field = 'Si_p3'
    elif ion == 'C II':
        field = 'C_p1'
    elif ion == 'C III':
        field = 'C_p2'
    elif ion == 'C IV':
        field = 'C_p3'
    elif ion == 'Mg II':
        field = 'Mg_p1'
    return field

def return_field_name(ion, field, full_name = True):
    ion_prefix = return_ion_prefix(ion)
    field_name = "%s_%s"%(ion_prefix, field)
    if full_name:
        field_name = ('gas', field_name)
    return field_name

def generate_ion_field_list(ion_list, field, full_name = True):
    field_name_list = []
    for ion in ion_list:
        field_name_list.append(return_field_name(ion, field, full_name))
    return field_name_list
                        
def phase_median_frequency_profile(x, y, z, confidence = 0.682, xmin = None, xmax = None, nbins = 50, centered = True):
    if xmin == None:
        xmin = x.min()
    if xmax == None:
        xmax = x.max()

    xbins           = np.linspace(xmin, xmax, nbins+1)
    centered_x_bins = (xbins + (xmax/nbins/2.0))
    median          = np.zeros(nbins)
    avg             = np.zeros(nbins) 
    lowlim          = np.zeros(nbins)
    uplim           = np.zeros(nbins)
    for i in range(nbins):
        mask = (x >= xbins[i]) & (x < xbins[i+1])
        sample        = np.ndarray.sum(z[mask], axis = 0)
        sum_sample    = np.sum(sample)
        cumsum_sample = np.cumsum(sample)
        med_array = np.where(cumsum_sample > 0.5 * sum_sample)[0]
        low_array = np.where(cumsum_sample > (1.0 - confidence/2.0)*sum_sample)[0]
        up_array  = np.where(cumsum_sample > (confidence/2.0)*sum_sample)[0]
        if med_array.size != 0:
            median[i] = y[med_array[0]]
            avg[i]    = np.average(y, weights = sample)
            lowlim[i] = y[low_array[0]]
            uplim[i]  = y[up_array[0]]
    if centered:
        xbins = centered_x_bins
    return xbins[:-1], median, avg, lowlim, uplim

    

def median_profile(x_arr, y_arr, r_max = 300, n_bins = 100):
    r_bins = np.linspace(0, r_max, n_bins)
    bin_ids = np.digitize(x_arr, r_bins)
    median = np.zeros(len(r_bins))
    std = np.zeros(len(r_bins))
    for i in np.arange(n_bins):
        bin_id = i + 1
        sample = y_arr[bin_ids == bin_id]
        median[i] = np.median(sample)
        std[i] = np.std(sample)

    return r_bins, median, std

def covering_fraction_profile(ion, r_arr, cdens_arr, r_max = 300, n_bins = 100, threshold = None):
    r_bins = np.linspace(0, r_max, n_bins)
    centered_r_bins = r_bins + (r_max/n_bins/2.0)
    if threshold == None:
        threshold = return_observational_threshold(ion)
    print("%s observational threshold: %e"%(ion, threshold))
    bin_ids = np.digitize(r_arr, r_bins)
    covering_fraction_profile_data = np.zeros(len(r_bins))
    for i in np.arange(n_bins):
        bin_id = i + 1
        sample = cdens_arr[bin_ids == bin_id]
        above_threshold = sample[sample > threshold]
        covering_fraction_profile_data[i] = len(above_threshold) / len(sample)
    return centered_r_bins, covering_fraction_profile_data

def median_and_cfrac_profiles(ion, r_arr, cdens_arr, r_max = 300, n_bins = 100, threshold = None):
    if threshold == None:
        threshold = return_observational_threshold(ion)
    print("%s observational threshold: %e"%(ion, threshold))
    r_bins = np.linspace(0, r_max, n_bins)
    centered_r_bins = r_bins + (r_max/n_bins/2.0)
    bin_ids = np.digitize(r_arr, r_bins)
    median = np.zeros(len(r_bins))
    std = np.zeros(len(r_bins))
    covering_fraction_profile_data = np.zeros(len(r_bins))
    for i in np.arange(n_bins):
        bin_id = i + 1
        sample = cdens_arr[bin_ids == bin_id]
        median[i] = np.median(sample)
        std[i] = np.std(sample)
        above_threshold = sample[sample > threshold]
        if (len(sample)) > 0:
            covering_fraction_profile_data[i] = len(above_threshold) / len(sample)
        else:
            covering_fraction_profile_data[i] = 0
    return centered_r_bins, median, std, covering_fraction_profile_data


def plot_hist2d(ax, r_arr, cdens_arr, rmax,  ylims, cmap='GnBu', nbins = 400, vmin=1, vmax_factor = 1.0, vmax=None, rmin = 0):
    xbins = np.linspace(rmin, rmax, nbins)
    ybins = 10**np.linspace(np.log10(ylims[0]), np.log10(ylims[1]), nbins)
    counts, x_edge, y_edge = np.histogram2d(r_arr, cdens_arr, bins=(xbins, ybins))
    x_bin_center = ((x_edge[1:] + x_edge[:-1]) / 2).reshape(nbins-1,1)
    # normalize counts in x-space to remove out linear increase in counts with 
    # radius due to circles of constant impact parameter
    counts /= x_bin_center 
    ax.set_yscale('log')
    #im = ax.pcolormesh(xbins, ybins, counts.T, vmin=counts.min(), vmax=counts.max(), cmap='magma', norm=LogNorm())
    print(counts.max())
    if vmax == None:
        vmax = counts.max()
    im = ax.pcolormesh(xbins, ybins, counts.T, vmin=vmin, vmax=vmax*vmax_factor, cmap=cmap, norm=LogNorm())
    return im

def generate_cluster_centered_r(axis, center, rvir, res = 800):
    cluster_center = [1747.17816336, 80.1641512, -1805.57513129]
    xstart = center[0] - cluster_center[0] - rvir
    xend = center[0] - cluster_center[0] + rvir
    ystart = center[1] - cluster_center[1] - rvir
    yend = center[1] - cluster_center[1] + rvir
    zstart = center[2] - cluster_center[2] - rvir
    zend = center[2] - cluster_center[2] + rvir
    
    if axis == 'x':
        py, pz = np.mgrid[ystart:yend:res*1j, zstart:zend:res*1j]
        radius = (py**2 + pz**2)**0.5
    elif axis == 'y':
        pz, px = np.mgrid[zstart:zend:res*1j, xstart:xend:res*1j]
        radius = (px**2 + pz**2)**0.5
    elif axis == 'z':
        px, py = np.mgrid[xstart:xend:res*1j, zstart:zend:res*1j]
        radius = (px**2 + py**2)**0.5
    return radius.ravel()
        

def load_r_cdens(fname, ion, underscore = False, space = True, rname = 'radius'):
    r_arr = []
    cdens_arr = []
    if os.path.isfile(fname):
        frb = h5.File(fname, 'r')
    else:
        print("WARNING: %s is not a file"%(fname))
        sys.stdout.flush()
        return r_arr, cdens_arr
    if space == False:
        ion = ion.replace(" ", "")
    for axis in ['x', 'y', 'z']:
            if underscore:
                cname = "%s_%s"%(ion, axis)
            else:
                cname = "%s %s" % (ion, axis)
            if cname in frb.keys():
                r_arr = np.concatenate((r_arr, frb[rname][:]))
                cdens_arr = np.concatenate((cdens_arr, frb[cname][:]))
            else:
                print("WARNING: %s not in %s"%(cname, fname))
                sys.stdout.flush()

    return r_arr, cdens_arr


def make_projection(ds, axis, ion_fields, center, width, res = 800):
    p = ds.proj(ion_fields, axis, weight_field=None, center=center, method='integrate')
    return p.to_frb(width, res, center=center)


def add_cluster_observations(ax, ion, color = 'black', zorder = 10):
    ion = ion.replace(' ', '')
    datafile = '/nobackup/ibutsky/data/YalePaper/burchett_observations.dat'
    if ion == 'HI':
        columns = (1, 8, 9)
    elif ion == 'OVI':
        columns = (1, 10, 11)
    impact, col, colerr = np.loadtxt(datafile, unpack=True, skiprows=1, usecols=columns, delimiter = '|')
    col = np.power(10, col)

#    lowlim = (colerr == -99.0)
    uplim =  (abs(colerr) ==  99.0)
    normal = (abs(colerr) < 99.0)

    ax.scatter(impact[normal], col[normal], marker = 's', zorder = zorder, c = color, linewidths = 0.5, edgecolors = 'black')
    ax.errorbar(impact[normal],col[normal], colerr[normal],zorder= zorder,color = color)
    ax.scatter(impact[uplim],  col[uplim],  marker = 'v', zorder = zorder, c = color, linewidths = 0.5, edgecolors = 'black')


def digitize(xarr, yarr, xmin = 0, xmax = None, nbins = 20):
    if xmax == None:
        xmax = np.max(xarr)
    
    x_bins = np.linspace(xmin, xmax, nbins)
    print()
    bin_ids = np.digitize(xarr, x_bins)
    y_bins = np.zeros(len(x_bins))
    
    for i in np.arange(nbins):
        bin_id = i
        sample = yarr[bin_ids == bin_id]
        y_bins[i] = np.sum(sample)
        
    return x_bins, y_bins

def interleave(x, trim):
    if trim == 0:
        c = np.vstack((x, x)).reshape((-1,), order = 'F')
        return c[1:]
    else:
        a = x[:-trim]
        b = x[trim:]
        c = np.vstack((a,b)).reshape((-1,),order='F')
        c = np.insert(c, 0, x[0])
        return c
    
def normalize_digitized_arrays(array_list):
    nbins = len(array_list[0])
    print(nbins)
    for i in np.arange(nbins):
        temp_sum = 0
        for array in array_list:
            temp_sum += array[i]
        for array in array_list:
            if temp_sum != 0:
                array[i] /= temp_sum


def crop_imshow(image, x1, x2, y1, y2):
    """                                                                             
    Return the cropped image at the x1, x2, y1, y2 coordinates                      
    """
    if x2 == -1:
        x2=image.shape[1]-1
    if y2 == -1:
        y2=image.shape[0]-1

    mask = np.zeros(image.shape)
    mask[y1:y2+1, x1:x2+1]=1
    m = mask>0

    return image[m].reshape((y2+1-y1, x2+1-x1))


def plot_cos_data(ax, ion, zorder = 10, color = 'black'):
# loading in Jessica Werk's data                                                                                          

    outfile = open('/nobackup/ibutsky/data/werk2013.dat', 'r')
    lines = outfile.readlines()

    impact = []
    ions = []
    quality = []
    logN = []
    logNerr = []
    limits = []

    for i in range(len(lines)):
        line = lines[i].split()
        len_line = len(line)

        impact.append(int(line[2]))
        ions.append(line[3]+' '+line[4])
        quality.append(int(line[12]))
        if len(line) > 13:
            if line[-2] == '<' or line[-2] == '>':
                logN.append(float(line[-1]))
                limits.append(line[-2])
                logNerr.append(0.0)

            else:
                logN.append(float(line[-2]))
                logNerr.append(float(line[-1]))
                limits.append(-1)
        else:
            if line[-3] == '<' or line[-3] == '>':
                logN.append(float(line[-2]))
                limits.append(line[-3])
                logNerr.append(0.0)
            else:
                logN.append(float(line[-3]))
                limits.append(-1)
                logNerr.append(float(line[-2]))

    ions = np.array(ions)
    impact = np.array(impact)
    quality = np.array(quality)
    logN = np.array(logN)
    Nion = np.power(10, logN)
    logNerr = np.array(logNerr)
    Nerr = np.power(10, logNerr)
    limits = np.array(limits)

    ion_mask = (ions == ion) & (logNerr > 0)
    ion_up_mask = (ions == ion) & (limits == '<')
    ion_low_mask = (ions == ion) & (limits == '>')
    
    ax.scatter(impact[ion_mask], Nion[ion_mask], marker = 's', c = color, zorder = zorder, \
               linewidths = 0.5, edgecolors = 'black')
    ax.scatter(impact[ion_up_mask], Nion[ion_up_mask], marker = 'v', c = color, zorder = zorder, \
               linewidths = 0.5, edgecolors = 'black')
    ax.scatter(impact[ion_low_mask], Nion[ion_low_mask], marker = '^', c = color, zorder = zorder, \
               linewidths = 0.5, edgecolors = 'black')


def plot_box(ax, xmin, xmax, ymin, ymax, color = 'black', linestyle = 'dashed'):
    ax.plot([xmin, xmax], [ymin, ymin], color = color, linestyle = linestyle)
    ax.plot([xmin, xmax], [ymax, ymax], color = color, linestyle = linestyle)
    ax.plot([xmin, xmin], [ymin, ymax], color = color, linestyle = linestyle)
    ax.plot([xmax, xmax], [ymin, ymax], color = color, linestyle = linestyle)


def plot_phase(xfield, yfield, zfield, profile = False, profile_color = 'black', profile_alpha = 0.3,\
               xlabel = None, ylabel = None, xlim = None, ylim = None, zlim = None, nbins = 50,\
               cmap = 'viridis', xscale = 'log', yscale = 'log', show_cbar = True, cbar_label = None, \
               fig = None, ax = None, output = 3035, data_cut = ''):

    plot_data = h5.File('/nobackup/ibutsky/data/YalePaper/romulusC.%06d_phase_data_%s_%s_%s%s.h5'\
                        %(output, xfield, yfield, zfield, data_cut), 'r')

    x = plot_data[xfield].value
    y = plot_data[yfield].value
    z = plot_data[zfield].value

    res = 256
    px, py = np.mgrid[x.min():x.max():res*1j, y.min():y.max():res*1j]
    zravel = z.T.ravel()
    xravel = px.ravel()

    print(z.min(), z.max())

    if fig == None:
        fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize=(6, 5))

    if xlabel == None:
        ax.set_xlabel(xfield)
    else:
        ax.set_xlabel(xlabel)

    if ylabel == None:
        ax.set_ylabel(yfield)
    else:
        ax.set_ylabel(ylabel)

    if xlim:
        ax.set_xlim(xlim[0], xlim[1])
    if ylim:
        ax.set_ylim(ylim[0], ylim[1])
    if zlim == None:
        zlim = (z.min(), z.max())

    ax.set_xscale(xscale)
    ax.set_yscale(yscale)

    im = ax.pcolormesh(x, y, z.T, norm = LogNorm(), cmap = cmap, vmin = zlim[0], vmax = zlim[1])
    if profile:
        append_median_profile(ax, x, y, z, color = profile_color, alpha = profile_alpha, nbins = nbins)

    if show_cbar:
        cbar = fig.colorbar(im, ax = ax, orientation = 'vertical', pad = 0)
        if cbar_label == None:
            cbar.set_label(zfield)
        else:
            cbar.set_label(cbar_label)
    #cbax.xaxis.set_ticks_position('top')          
    #cbax.xaxis.set_label_position('top')    
    if zlim == None:
        zlim = (z.min(), z.max())
    fig.tight_layout()
    return fig, ax, im, cbar



def append_median_profile(ax, x, y, z, color = 'black', fill_color = None, linestyle = 'dashed', label = None,\
                          alpha = 0.3, confidence = 0.682, xmin = None, xmax = None, nbins = 50, centered = True):
    xbins, med, avg, lowlim, uplim = phase_median_frequency_profile(x, y, z, centered = centered,\
                            confidence = confidence, xmin = xmin, xmax = xmax, nbins = nbins)
    if fill_color == None:
        fill_color = color
    ax.plot(xbins, med, color = color, linestyle = linestyle, label = label)
    ax.fill_between(xbins, lowlim, uplim, color = fill_color, alpha = alpha, zorder = 10)


def annotate_ion_name(ax, ion_name, fontsize = 18, x_factor = 0.85, y_factor = 0.88, color = 'black'):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    if ion_name.replace(' ', '') == 'OVI':
        x_factor *= 0.95

    if ax.get_xscale() == 'log':
        log_xrange = np.log10(xlim[1]) - np.log10(xlim[0])
        x = np.power(10, np.log10(xlim[0]) + x_factor*log_xrange)
    else:
        x_range = xlim[1] - xlim[0]
        x = xlim[0] + x_factor * x_range

    if ax.get_yscale() == 'log':
        log_yrange = np.log10(ylim[1]) - np.log10(ylim[0])
        y = np.power(10, np.log10(ylim[0]) + y_factor*log_yrange)
    else:
        y_range = ylim[1] - ylim[0]
        y = ylim[0] + y_factor * y_range

    ax.annotate(ion_name, xy = (x,y), fontsize = fontsize, color = color)
