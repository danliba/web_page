# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 16:59:15 2021

@author: danli
"""
#1, 20, 60, 100, 140 y 180
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import functools 
import os 
from oceans.colormaps import cm

path0='D:\\CIO\\pg_web\\'
dir_list=os.listdir('D:\\CIO\\pg_web\\'); check= 't'
buoy_list = [idx for idx in dir_list if idx[0].lower() == check.lower()]

for kk in range(len(buoy_list)):
    fn=buoy_list[kk]
    print(fn)
    #fn='t0n110w_dy.cdf'
    data=Dataset(path0+fn)
    
    lat = data.variables['lat'][:]
    lon = data.variables['lon'][:]
    depth = data.variables['depth'][:]
    time = data.variables['time'][:]
    
    starting_date = data.variables['time'].units[11:21]
    
    
    temp = data.variables['T_20'][:][:,:,0,0]
    creation_day=data.variables['time'].units; yy=int(creation_day[11:15]); mm=int(creation_day[16:18]); dd=int(creation_day[19:21])
    fecha=time+np.array(date.toordinal(date(yy,mm,dd)))
    temp=np.array(temp,dtype='float32').T
    
    #start=2020
    yrst=2020; most=1; dast=1
    date_start=np.array(date.toordinal(date(yrst,most,dast)))
    find_stdate=np.where(fecha==date_start)
    fdt=functools.reduce(lambda sub, ele: sub * 10 + ele, find_stdate)
    if len(fdt)==0 :
        print("Starting date is out of range")
        continue
    
    indx_date=int(fdt)
    fecha_inicio=fecha[indx_date:]; 
        
    ending_date = date.fromordinal(int(fecha_inicio[-1])) 
    date_range = pd.date_range(start= starting_date, end=ending_date)
        
    temp[temp==1.0000000e+35] = np.nan; sst=temp[:,indx_date:]
    #plot
    plt.figure(figsize=(11.69,8.27))
    vmin=8; vmax=32; step=2;#colorscale
    
    cs = plt.pcolormesh(date_range[indx_date:], -depth, sst, vmin=vmin, vmax=vmax, cmap=cm.avhrr, shading='flat')
    plt.yticks(list(range(0,-300-20,-20)))
    #plt.hold(True)
    contours= plt.contour(date_range[indx_date:], -depth, sst,levels=[10,11,12,15,20,25,28,30],colors='black',linewidths=0.5)
    plt.clabel(contours, inline=True,fmt = '%2.0f',fontsize=10)
    plt.ylim([-300,0])
    cb = plt.colorbar(cs, pad=0.02, orientation='vertical', fraction=0.1)
    cb.ax.locator_params(nbins=len(list(range(vmin,vmax,step))))
    cb.ax.tick_params(direction='out')
    cb.set_label('Temperature ($^\circ$C)')
    plt.title('Daily Subsurface Temperature Buoy '+fn[1]+'º'+fn[2]+fn[3:6]+'º'+fn[6])
    plt.text(0.8, 0.05, str(ending_date),fontsize=10, transform=plt.gcf().transFigure)
    plt.text(0.07, 0.05, 'DALB',fontsize=10, transform=plt.gcf().transFigure)
    plt.tight_layout()
    
    plt.savefig('D:\\CIO\\pg_web\\ST_boya'+fn[1:7]+'.png',
    format='png', dpi=600, transparent=False)
    plt.show()