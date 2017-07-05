# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:16:30 2017

@author: tanner
"""

#import datetime
#import calcTime
#The Hey Rube! of cross import
from HRRR_Alert import getQualRadar
from NEXRAD_Alert import createHeader

#rData=[[8.800755281614371, 29.815845102899264, 'NNE'], 30]
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


def createAlert(rData,radarLib):
    if not any(rData):
        return ''
    line=str(radarLib['radar_name'])+' reported potential storm conditions of: '+\
    ''+str(getQualRadar(rData[1]))+'. dBZ greater than: '+str(rData[1])+'. at: '+str(round(rData[0][0],1))+\
    ' miles '+str(rData[0][2])+' of your location within the last 15 minutes.\n'
    return createHeader()+line
    
def createCONUSAlert(rData,time):
    if not any(rData):
        return ''
    line='Potential storm conditions of: '+\
    ''+str(getQualRadar(rData[1]))+' detected. dBZ greater than: '+str(rData[1])+'. at: '+str(round(rData[0][0],1))+\
    ' miles '+str(rData[0][2])+' at: '+str(time)+'\n'
    return createHeader()+line
    


















