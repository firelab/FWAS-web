# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:25:57 2017

@author: tanner
"""
import datetime

import calcTime
import CONUS_RADAR_Fetch
import CONUS_RADAR_Parse
import NCR_Alert

#tZ='America/Denver'

#hDir='/media/tanner/vol2/CONUS_RADAR/'
hDir='/home/ubuntu/fwas_data/CONUS_RADAR/'

gifName=hDir+'conus_radar.gif'
rTime=hDir+'rTimes.txt'




def getRadarAlerts(storm_on,headerLib,radarLib,plot_on,threshold,precip_on,precip_threshold):
    """
    Delegates out radar checks...
    """
    CONUS_RADAR_Fetch.fetchRadar(False)
    location=[float(headerLib['latitude']),float(headerLib['longitude'])]
    nAlert=''            
    tZ=calcTime.convertTimeZone(int(headerLib['time_zone']))
    fFile=open(rTime,'r')
    lastTime=fFile.read().splitlines()[-1]
    fFile.close()
    utc=datetime.datetime.strptime(lastTime[:8]+'_'+lastTime[9:13],'%Y%m%d_%H%M')
    local=calcTime.utcToLocal(utc,tZ)
    #    print local.strftime('%H:%M, %Y-%m-%d')
    nAlert=''                
    if storm_on==True:   
        rData=CONUS_RADAR_Parse.runRadarCheck(location,float(headerLib['radius']),plot_on,threshold)
        nAlert=NCR_Alert.createCONUSAlert(rData,local.strftime('%H:%M, %m/%d/%Y'))
    pAlert=''
    if precip_on==True:
        pData=CONUS_RADAR_Parse.runRadarCheck(location,float(headerLib['radius']),plot_on,precip_threshold)  
        pAlert=NCR_Alert.createPRECIPAlert(pData,local.strftime('%H:%M, %m/%d/%Y'))
    nAlert+=pAlert
    return nAlert
    
    


#def runDemo():
#    threshold=30
#    radarLib={'radar_name': 'KMSX', 'radar_on': '1'}
#    headerLib={'alert_name': 'Alert',
# 'alert_time': '2017-06-29 17:45:43',
# 'carrier': 'NaN',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '30.6945',
# 'limit': '0',
# 'longitude': '-88.0399',
# 'phone': 'NaN',
# 'radius': '12',
# 'time_zone': '2'}
#
#    headerLib2={'alert_name': 'Alert',
#     'alert_time': '2017-06-21 09:26:37',
#     'carrier': 'NaN',
#     'email': 'fsweather1@usa.com',
#     'expires_after': '24',
#     'latitude': '42.748',
#     'limit': '0',
#     'longitude': '-94.258',
#     'phone': 'NaN',
#     'radius': '12',
#     'time_zone': '2'}
#    
#    a=getRadarAlerts(headerLib,radarLib,True,threshold)
#    print a

#runDemo()





#radarLib={'radar_name': 'KMSX', 'radar_on': '1'}
#headerLib={'alert_name': 'Alert',
# 'alert_time': '2017-06-29 17:45:43',
# 'carrier': 'NaN',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '30.6945',
# 'limit': '0',
# 'longitude': '-88.0399',
# 'phone': 'NaN',
# 'radius': '12',
# 'time_zone': '2'}
#
#getRadarAlerts(headerLib,radarLib,True,40)





