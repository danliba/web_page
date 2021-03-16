# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 22:29:31 2021

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
path0='D:\\CIO\\pg_web\\'
dir_list=os.listdir(); check= 't'
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

    #selecciona las depth donde hay temperatura
    sst_sel=np.multiply(~np.isnan(sst[:,-1]),1)*depth
    selected_depth=sst_sel[sst_sel != 0]
    
    #profundidades_australia=[25, 50, 100, 150, 200]
    profundidades=[]
    cum_depth=[]
   #plot
    plt.figure(figsize=(11.69,8.27))
    if lon > 180:
        
        prof=[0,5,20,60,100,140,180] #Pacifico este
        for jj in range(len(prof)-1):
            a=max(np.where(np.logical_and(selected_depth>=prof[jj], selected_depth<=prof[jj+1])))
            if len(a)==0:
                continue
            else:
                a2=max(a)
                cum_depth.append(a2)
          
        profundidades=selected_depth[cum_depth] #profundidades a plotear
    else: 
        prof=[25, 50, 100, 150, 200] #australia
        for jj in range(len(prof)-1):
          a=max(np.where(np.logical_and(selected_depth>=prof[jj], selected_depth<=prof[jj+1])))
          
          if len(a)==0:
                continue
          else:
                a2=max(a)
                cum_depth.append(a2)
                             
        profundidades=selected_depth[cum_depth] #profundidades a plotear
        
    for ii in range(len(profundidades)):
        find_depth=np.where(depth==profundidades[ii])
        indx0 = functools.reduce(lambda sub, ele: sub * 10 + ele, find_depth) 
        sst2=sst[indx0,:].T
        #plt.plot(fecha_inicio,np.array(sst),linewidth=1,marker='*',markersize=2)
        plt.plot(date_range[indx_date:],np.array(sst2),linewidth=1,marker='*',markersize=2, label=str(int(profundidades[ii]))+'m')
        plt.ylabel('Temperatura ºC')
        plt.title('Daily Subsurface Temperature Buoy '+fn[1]+'º'+fn[2]+fn[3:6]+'º'+fn[6])
        plt.text(0.8, 0.05, str(ending_date),fontsize=10, transform=plt.gcf().transFigure)
        plt.text(0.07, 0.05, 'DALB',fontsize=10, transform=plt.gcf().transFigure)
        # if lon>=180 :
        #     plt.title('Buoy '+str((int(lon)-360)*-1)+'ºW')
        # else:
        #     plt.title('Buoy '+str(int(lon))+'ºE')    
        
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('D:\\CIO\\pg_web\\boya'+fn[1:7]+'.png',
    format='png', dpi=600, transparent=False)
    plt.show()
    

    
