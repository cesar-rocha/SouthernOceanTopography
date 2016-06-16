
# coding: utf-8

# This script makes a 3D plot of the Southern Ocean topography.
#
# The data comes from some geophysiscists at Columbia. The product is "MGDS: Global Multi-Resolution Topography". These folks took all multibeam swath data that they can get their hands on and filled gaps with Smith and Sandwell. See http://www.marine-geo.org/portals/gmrt/ for data covarage.


import numpy as np
import matplotlib.pyplot as plt
# get_ipython().magic('matplotlib inline')

from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

import scipy as sp
import scipy.interpolate
import scipy.io as io
import seawater as sw

from pyspec import spectrum as spec
import cmocean

from mpl_toolkits.mplot3d import Axes3D

plt.close("all")



## select different regions
def subregion_plot(latmin=-64,lonmin=-100,dlat=8,dlon=15):

    latmax = latmin+dlat
    lonmax = lonmin+dlon

    lon = np.array([lonmin,lonmax,lonmax,lonmin,lonmin])
    lat = np.array([latmin,latmin,latmax,latmax,latmin])

    x,y = m(lon,lat)

    return x,y

def extract_topo(lon,lat,latmin=-64,lonmin=-100,dlat=8,dlon=15):

    latmax = latmin+dlat
    lonmax = lonmin+dlon

    flat = (lat>=latmin)&(lat<=latmax)
    flon = (lon>=lonmin)&(lon<=lonmax)

    lont = lon[flon]
    latt = lat[flat]
    topo = z[flat,:]
    topo = topo[:,flon]

    return lont,latt,topo



topo = Dataset('GMRTv3_1_20160124topo.grd')
pf = Dataset('SO_polar_fronts.v3.nc')

lonpf, latpf,latsaf,latsafn = pf['lon'][:], pf['latPF'][:],pf['latSAF'][:], pf['latSAFN'][:]
time = pf['is_aviso_nrt'][:]

latpf = latpf.reshape(time.size,lonpf.size)
latpf = np.nanmean(latpf,axis=0).squeeze()

latsaf = latsaf.reshape(time.size,lonpf.size)
latsaf = np.nanmean(latsaf,axis=0).squeeze()

latsafn = latsafn.reshape(time.size,lonpf.size)
latsafn = np.nanmean(latsafn,axis=0).squeeze()



x = topo['lon'][:]
y = topo['lat'][:]


#z = (topo['z'][:]).reshape(y.size,x.size)
z = topo['altitude'][:]

# get a subset
latmin, latmax = -80., -20
lonmin, lonmax = -180., 180.

flat = (y>=latmin)&(y<=latmax)
flon = (x>=lonmin)&(x<=lonmax)

lat = y[flat]
lon = x[flon]
z = z[flat,:]
z = z[:,flon]

z = np.ma.masked_array(z,z>=0)

x,y = np.meshgrid(lon,lat)

lon,lat = np.meshgrid(lon,lat)

z[z>=0]=0.

fig = plt.figure(figsize=(22,8))
ax = fig.add_subplot(111, projection='3d')



# this controls the quality of the plot
# set to =1 for maximum quality
dec = 10

#ax.contourf(lon[::dec,::dec],lat[::dec,::dec],z[::dec,::dec], [-2000, -1000], cmap=cmocean.cm.bathy_r)
surf =  ax.plot_surface(lon[::dec,::dec],lat[::dec,::dec],z[::dec,::dec],
                linewidth=0, rstride=1, cstride=1, alpha=1, cmap='YlGnBu',
                vmin=-5500,vmax=-500)
ax.contourf(lon[::dec,::dec],lat[::dec,::dec],z[::dec,::dec],[-1.,0],colors='peru')
ax.set_zticks([])
ax.view_init(75, 290)


#ax.plot(xpf,ypf,'w.')
#ax.plot(xsaf,ysaf,'w.')
lonpf[lonpf>180] =  lonpf[lonpf>180]-360

ax.plot(lonpf,latpf,-2000,'w.')
ax.plot(lonpf,latsaf,-2000,'w.')
ax.plot(lonpf,latsafn,-2000,'w.')



fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.745, 0.2, 0.02, 0.4])
fig.colorbar(surf, cax=cbar_ax,label=r'',extend='both')

#plt.savefig('SO3DTopo.pdf',bbox_inches='tight')
plt.savefig('SO3DTopo.png',bbox_inches='tight',dpi=300)
#plt.show()
