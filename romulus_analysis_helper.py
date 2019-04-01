import yt
import h5py as h5

def load_romulus_halo_props(sim, output):
    return h5.File('/nobackup/ibutsky/data/%s_halo_data_%i'%(sim, output), 'r')

def get_romulus_center(sim, output):
    halo_props = load_romulus_halo_props(sim, output)
    centers = halo_props['center'].value
    return centers[0]
    
def get_romulus_yt_center(sim, output, ds): 
    physical_center = get_romulus_center(sim, output)
    yt_center = (physical_center / ds.length_unit).d
    return yt_center

def get_romulus_rvir(sim, output):
    halo_props = load_romulus_halo_props(sim, output)
    rvirs = halo_props['rvir'].value
    return rvirs[0]


def get_romulusC_r200(output):
    if output == 3035:
        return 810.0
    elif output == 3360:
        return 955.3
    elif output == 3697:
        return 1014.7 
