# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 12:55:27 2017

@author: tanner
"""

import NCR_Fetch
import NCR_Parse
import NCR_Alert

#radarLib={'radar_name': 'KMSX', 'radar_on': '1'}
#headerLib={'alert_name': 'Alert',
# 'alert_time': '2017-06-21 09:26:37',
# 'carrier': 'NaN',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '46.92',
# 'limit': '0',
# 'longitude': '-114.1',
# 'phone': 'NaN',
# 'radius': '12',
# 'time_zone': '2'}

def getRadarAlerts(headerLib,radarLib):
    location=[float(headerLib['latitude']),float(headerLib['longitude'])]
    rLoc=NCR_Fetch.fetchRadar(radarLib['radar_name'])
    rData=NCR_Parse.runRadarCheck(rLoc,location,float(headerLib['radius']),False)
    nAlert=NCR_Alert.createAlert(rData,radarLib)
    return nAlert