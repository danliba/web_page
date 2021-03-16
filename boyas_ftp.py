# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 01:20:25 2021

@author: danli
"""
###codigo para descargar todas las boyas de la NOAA de temperatura subsuperficial##########
import ftplib

ftp = ftplib.FTP('ftp.pmel.noaa.gov')
ftp.login('user', 'pswd')

#savedir = '/mnt/d/CIO/Kelvin-cromwell/boyas/pg_web'
#os.chdir(savedir)

ftp.cwd('/cdf/sites/daily')
print(ftp.cwd)
dir_list = []
ftp.dir(dir_list.append)

#latitudes=[0,2,5,8,9]
latitudes=[0]
for ff in range(len(latitudes)):
    lat=latitudes[ff]; 
    buoy_list=[95,110,125,140,155,170,180]
    for jj in range(0,len(buoy_list)):
        pattern= 't%dn%dw_dy.cdf' % (lat,buoy_list[jj])#north-west
        pattern2= 't%ds%dw_dy.cdf' % (lat,buoy_list[jj])#south-west
        for ii in range (1,len(dir_list)):
            dir_list_end=dir_list [ii][56:]
            #north-west
            if dir_list_end==pattern:
                file = open(dir_list_end, 'wb')
                ftp.retrbinary('RETR ' + dir_list_end, file.write)
                file.close()
                print(dir_list_end)
            #south-west
            if  dir_list_end==pattern2:
                file = open(dir_list_end, 'wb')
                ftp.retrbinary('RETR ' + dir_list_end, file.write)
                file.close()
                print(dir_list_end)
                
    
    buoy_list=[137,147,156,165]
    for jj in range(0,len(buoy_list)):
        pattern= 't%dn%de_dy.cdf' % (lat,buoy_list[jj])#north-east
        pattern2= 't%ds%de_dy.cdf' % (lat,buoy_list[jj])#south-east
        for ii in range (1,len(dir_list)):
            dir_list_end=dir_list [ii][56:]
            if dir_list_end==pattern:#north-east
                file = open(dir_list_end, 'wb')
                ftp.retrbinary('RETR ' + dir_list_end, file.write)
                file.close()
                print(dir_list_end)
            if dir_list_end==pattern2:#south-east
                file = open(dir_list_end, 'wb')
                ftp.retrbinary('RETR ' + dir_list_end, file.write)
                file.close()
                print(dir_list_end)








