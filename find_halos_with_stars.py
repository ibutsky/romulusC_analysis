import matplotlib
matplotlib.use('Agg')
import tangos 
import numpy as np
import pylab as plt
import h5py as h5


#in romulusC
#12 = 636, z = 3.0, t = 2.15 Gyr
#16 = 960, z = 2.03, t = 3.24 Gyr
#49 - = 3035, z = 0.3
#56 = 3360, z = 0.2
#61 = 3697, z = 0.1
#71 - z = 0


#in romulus25
#104 = 6069, z = 0.31
#110 = 6656, z = 0.21
#116 = 7394, z = 0.1


def find_halos_with_stars(timestep, output):
    halos = tangos.get_simulation("h1.cosmo50").timesteps[timestep].halos
    #halos = tangos.get_simulation("cosmo25").timesteps[110].halos

    halo_id = []
    Rvir = []
    dist_to_cluster = []
    Mvir = []
    Mstar = []
    Mgas = []
    MColdGas = []
    MHIGas = []
    Rvir = []
    center = []

    cluster_center = halos[0]['shrink_center']

    for i in range(len(halos[:1000])):
        halo = halos[i]
    
        mstar = halo['Mstar']
        mgas = halo['Mgas']
        if i%50 == 0:
            print(i)
        if mstar > 1e8:
            print(i, mstar/1e12)
            halo_id.append(i)
            Rvir.append(halo['max_radius'])
            center.append(halo['shrink_center'])
            dist_to_cluster.append(np.linalg.norm(np.subtract(halo['shrink_center'], cluster_center)))
            Mvir.append(halo['Mvir'])
            Mstar.append(mstar)
            Mgas.append(mgas)
            MColdGas.append(halo['MColdGas'])
            MHIGas.append(halo['MHIGas'])


    h5file = h5.File('/nobackup/ibutsky/data/romulusC_halo_data_%i'%(output), 'w')
    

    h5file.create_dataset('halo_id', data = np.array(halo_id))
    h5file.create_dataset('rvir', data = np.array(Rvir))
    h5file.create_dataset('mvir', data = np.array(Mvir))
    h5file.create_dataset('mstar', data =  np.array(Mstar))
    h5file.create_dataset('mgas', data = np.array(Mgas))
    h5file.create_dataset('mcoldgas', data = np.array(MColdGas))
    h5file.create_dataset('mhigas', data = np.array(MHIGas))
    h5file.create_dataset('center', data = np.array(center))
    h5file.create_dataset('dist_to_cluster', data = np.array(dist_to_cluster))
    h5file.flush()


timestep_list = [12, 13, 14, 15, 16]
output_list = [636, 672, 768, 864, 960]
                               
for timestep, output in zip(timestep_list, output_list):
    find_halos_with_stars(timestep, output)

