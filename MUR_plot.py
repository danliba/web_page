# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 17:25:56 2021

@author: danli
"""
import os
from netCDF4 import Dataset
from datetime import date
import numpy as np
from oceans.colormaps import cm
import matplotlib.pyplot as plt



path0='D:\\CIO\\pg_web\\mur\\'
dir_list=os.listdir('D:\\CIO\\pg_web\\mur\\'); check= '2'
mur_list = [idx for idx in dir_list if idx[0].lower() == check.lower()]

fn=mur_list[0]
print(fn)
data=Dataset(path0+fn)
    
lat = data.variables['lat'][:]
lon = data.variables['lon'][:]
time = (data.variables['time'][:])/86400
  
creation_day = data.variables['time'].units[14:24]; yy=int(creation_day[:4]); mm=int(creation_day[5:7]); dd=int(creation_day[8:10])  
fecha=date.fromordinal(int(time+np.array(date.toordinal(date(yy,mm,dd)))))

temp=data.variables['analysed_sst'][:][0,:,:]
sst=temp-273.15
sst_anom=data.variables['sst_anomaly'][:]

#plot
plt.figure(figsize=(11.69,8.27))
cs = plt.pcolormesh(lon, lat, sst, vmin=20, vmax=32, cmap='jet', shading='flat')
cb = plt.colorbar(cs, pad=0.02, orientation='vertical', fraction=0.1)
plt.xlim([-90,-70]); plt.ylim([-5,5])
plt.show()

#plt.contourf(lon,lat,sst,60, norm=None)


