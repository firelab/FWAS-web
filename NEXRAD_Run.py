# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:08:45 2017

@author: tanner
"""

import NEXRAD_Fetch
import NEXRAD_Parse
import NEXRAD_Alert
#import NEXRAD_radarStation

#def readRadarThresholds()

def runNEXRAD(headerLib,rLib,timeZone,plot):
    stid=rLib['radar_name']
    loc=[headerLib['latitude'],headerLib['longitude']]
    fileLoc=NEXRAD_Fetch.fetchStation(stid)
    rStation=NEXRAD_Parse.checkRadar(fileLoc,False,loc,plot)
    alert=NEXRAD_Alert.createAlert(rStation,rLib,timeZone)
    return alert

def runDemo():
    headerLib={'alert_name': 'Alert',
     'alert_time': '2017-06-21 09:26:37',
     'carrier': 'NaN',
     'email': 'fsweather1@usa.com',
     'expires_after': '24',
     'latitude': '46.92',
     'limit': '0',
     'longitude': '-114.1',
     'phone': 'NaN',
     'radius': '12',
     'time_zone': '2'}
    
    radarLib={'radar_name': 'KMSX', 'radar_on': '1'}
    tZ='America/Denver'
    
    runNEXRAD(headerLib,radarLib,tZ,True)












































