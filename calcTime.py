# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:05:55 2017

@author: tanner

DATETIME UTIL for FWAS
"""

import mwlatest
import ConfigParser
import station
from geopy.distance import great_circle
import math
import datetime
import dateutil
#import send
import pytz
import pint
import glob

#timeInt=2

def convertTimeZone(timeInt):
    """
    converts Number from Shiny App to Time Zone STring
    """
    validTimes=[1,2,3,4,5,6,7]
    validStringTimes=['America/Los_Angeles','America/Denver','US/Arizona','America/Chicago','America/New_York','Pacific/Honolulu','America/Anchorage']
    timeString=''  
    for i in range(len(validTimes)):
        if timeInt==validTimes[i]:
            timeString=validStringTimes[i]
    return timeString

#A=convertTimeZone(timeInt)
#print A

def calcExpirationDate(start,dur):
    """
    uses datetime library to add alert duration to when the alert started
    """
    startObj=datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
    dObj=datetime.timedelta(hours=int(dur))
    expObj=startObj+dObj
    return expObj

def calcForecastTimes():
    """
    Returns Timelist of forecasts in UTC
    """
#    cZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
    cZ=glob.glob('/home/ubuntu/fwas_data/HRRR/grib/*.grib2')
    cZ.sort()
    dwnHour=cZ[0][39:41]
#    dwnHour=cZ[0][40:42] #Temporary until shit stops httpsing the fan
    off=[]    
    for i in range(len(cZ)):
        oHour=int(cZ[i][50:52])
#        oHour=int(cZ[i][51:53]) #Temporary until shit stops httpsing the fan! 
        off.append(oHour)
    simDay=datetime.datetime.utcnow().strftime('%Y%m%d')
    simDate=datetime.datetime.strptime(simDay+dwnHour,'%Y%m%d%H')
    tList=[]
    for i in range(len(off)):
        rTime=simDate+datetime.timedelta(hours=off[i])
        tList.append(rTime)
    return tList


def utcToLocal(time,localZone):
    """
    Returns time in Local Time based on user settings
    """
    from_zone=dateutil.tz.gettz('UTC')
    to_zone=dateutil.tz.gettz(localZone)
    
    time=time.replace(tzinfo=from_zone)
    localTime=time.astimezone(to_zone)    
    return localTime
    

#cZ=glob.glob('/home/ubuntu/src/HRRR/grib/*.grib2')
#cZ.sort()
#dwnHour=cZ[0][33:35]
#offsetHour=cZ[0][44:46]
#
#hrs=[]
#off=[]
#
#for i in range(len(cZ)):
#    dHour=int(cZ[i][33:35])
#    oHour=int(cZ[i][44:46])    
#    hrs.append(dHour+oHour)
#    off.append(oHour)
#
#simDay=datetime.datetime.utcnow().strftime('%Y%m%d')
#simDate=datetime.datetime.strptime(simDay+dwnHour,'%Y%m%d%H')
#
#tList=[]
#for i in range(len(off)):
#    rTime=simDate+datetime.timedelta(hours=off[i])
#    tList.append(rTime)
#
#for i in range(len(tList)):
#    if tList[i]>datetime.datetime.now()-datetime.timedelta(minutes=30):
#        print True,tList[i],i
#    else:
#        print False,tList[i],i
#    
    






















