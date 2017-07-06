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




def getRadarAlerts(headerLib,radarLib,plot_on,threshold):
    CONUS_RADAR_Fetch.fetchRadar(False)
    location=[float(headerLib['latitude']),float(headerLib['longitude'])]
    rData=CONUS_RADAR_Parse.runRadarCheck(location,float(headerLib['radius']),plot_on,threshold)
    
    tZ=calcTime.convertTimeZone(int(headerLib['time_zone']))
    fFile=open(rTime,'r')
    lastTime=fFile.read().splitlines()[-1]
    fFile.close()
    utc=datetime.datetime.strptime(lastTime[:8]+'_'+lastTime[9:13],'%Y%m%d_%H%M')
    local=calcTime.utcToLocal(utc,tZ)
    nAlert=NCR_Alert.createCONUSAlert(rData,local)
    return nAlert


def runDemo():
    threshold=50
    radarLib={'radar_name': 'KMSX', 'radar_on': '1'}
    headerLib={'alert_name': 'Alert',
 'alert_time': '2017-06-29 17:45:43',
 'carrier': 'NaN',
 'email': 'fsweather1@usa.com',
 'expires_after': '24',
 'latitude': '30.6945',
 'limit': '0',
 'longitude': '-88.0399',
 'phone': 'NaN',
 'radius': '12',
 'time_zone': '2'}

    headerLib2={'alert_name': 'Alert',
     'alert_time': '2017-06-21 09:26:37',
     'carrier': 'NaN',
     'email': 'fsweather1@usa.com',
     'expires_after': '24',
     'latitude': '42.748',
     'limit': '0',
     'longitude': '-94.258',
     'phone': 'NaN',
     'radius': '12',
     'time_zone': '2'}
    
    a=getRadarAlerts(headerLib,radarLib,True,threshold)
    print a

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




