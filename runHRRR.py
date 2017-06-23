# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 09:23:36 2017

@author: tanner
"""

#import sys
#sys.path.insert(0,'/home/tanner/src/FWAS/HRRR/')
#import parseHRRR as ph

import calcUnits
import calcTime
import numpy

timeList=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18']

sixHourTimeList=['00', '01', '02', '03', '04', '05', '06']

"""
Fetch Data Files
"""
#fh.runFetchHRRR(sixHourTimeList)
#Don't Need Right Now
#fh.cleanHRRRDir()
#Don't Use YET
"""
Mess With them
"""

unitLib={'temperature_units': '2', 'wind_speed_units': '2'}
thresholdsLib={'relative_humidity': '75',
 'temperature': '5',
 'wind_gust': '10',
 'wind_speed': '2'}
headerLib={'alert_name': 'Alert',
 'alert_time': '2017-06-06 19:50:01',
 'carrier': 'NaN',
 'email': 'fsweather1@usa.com',
 'expires_after': '24',
 'latitude': '46.92',
 'limit': '0',
 'longitude': '-114.1',
 'phone': 'NaN',
 'radius': '12',
 'time_zone': '2'}
HRRRLib={'forecast_on': '1',
 'reflectivity': '1',
 'relative_humidity': '1',
 'temperature': '1',
 'wind_speed': '1'}

unitFlag={'wind':True,'temp':True}

def checkForNaN(thresholdsLib):
    datLib=thresholdsLib
    for i in range(len(datLib)):
        if datLib[datLib.keys()[i]]=='NaN':
            datLib[datLib.keys()[i]]=numpy.nan
#        else:
#            print "no NaNs"
    return datLib
    

def checkUnits(unitFlag,thresholdsLib):
    """
    HRRRRRRRRRRRRRRRRRRRRRrr1! requires metric units 
    """
    if unitFlag['wind']==True:
        wSpd=calcUnits.windSpeedETM(float(thresholdsLib['wind_speed']))
    if unitFlag['wind']==False:
        wSpd=float(thresholdsLib['wind_speed'])
    if unitFlag['temp']==True:
        temp=calcUnits.tempETM(float(thresholdsLib['temperature']))
    if unitFlag['temp']==False:
        temp=float(thresholdsLib['temperature'])
    return [wSpd,temp]

def getRHandReflec(thresholdsLib):
    refec=20 #Hard Coded for now
    rh=thresholdsLib['relative_humidity']
    return [refec,rh]

HLib=checkForNaN(thresholdsLib)
specVals=checkUnits(unitFlag,HLib)
genVals=getRHandReflec(HLib)












#fCastNum=18
#fCastRadius=20
#fCastLat=46.926183
#fCastLon=-114.092779
#fReflec=20
#fTemp=20
#fRH=57
#fWind=5
#mFCast=[]
#
#tSteps=ph.getDiskFiles()
#for i in range(len(tSteps)):
#    sfcast=ph.setControls(i,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)
#    mFCast.append(sfcast)
#
##for i in range(len(mFCast)):
##    print mFCast[i][1].average











































