#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:55:23 2017

@author: tanner

(used to be called 1.0.py)
"""

import mwlatest
import ConfigParser
import station
from geopy.distance import great_circle
import math
import datetime
import dateutil
import send
import checker
import pint
import calcTime
import calcUnits
import comparator
import createAlert
from station import printStation
import numpy
import sys

def getRAWSData(Lat,Lon,Radius,limit,spdUnits,tempUnits):
    """
    Internal RAWS fetcher. Uses Mesowest API
    """
    url=mwlatest.latlonBuilder(mwlatest.dtoken,str(Lat),str(Lon),str(Radius),"","relative_humidity,air_temp,wind_speed,wind_direction,precip_accum_one_hour,wind_gust","",str(spdUnits),str(tempUnits))
    response=mwlatest.readData(url)
    return response
timeZone=['']
radius=[0.0]
Location=[0.00,0.00]
numLimit=[0]
unitLimits={'temp':'','tempABV':'','spd':'','spdABV':''}
limits={'temp':0,'spd':0,'dir':0,'rain':0,'rh':0,'gust':0}

cfgLoc=['']

print "Fire Weather Alert System"

def setLimits(temp,spd,direction,Precip,RH,Gust):
    """
    Internally Sets Thresholds that are provided by user
    """
    limits['temp']=temp
    limits['spd']=spd
    limits['dir']=direction
    limits['rain']=Precip
    limits['rh']=RH
    limits['gust']=Gust

def setGlobalVars(Lat,Lon,Radius,TZ,stationLimit):
    """
    Sets Things that do not change for run
    """
    Location[0]=Lat
    Location[1]=Lon
    timeZone[0]=TZ
    radius[0]=Radius
    numLimit[0]=stationLimit

def setLimitUnits(spd,temp):
    """
    Sets Units on Thresholds
    """
    unitLimits['temp']=temp[0]
    unitLimits['tempABV']=temp[1]
    unitLimits['spd']=spd[0]
    unitLimits['spdABV']=spd[1]


def readThresholds():
    """
    Reads In Thresholds from File, which come from Shiny App
    """
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc[0])
    headerDict={}
    thresholdDict={}
    unitDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        headerDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[1])
    section=cfg.sections()[1]
    for i in range(len(options)):
        thresholdDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[2])
    section=cfg.sections()[2]
    for i in range(len(options)):
        unitDict[options[i]]=cfg.get(section,options[i])
    return [headerDict,thresholdDict,unitDict]

def checkThresholds(thresholds,units):
    """
    Doesn't work, may be needed in the future
    """
    needKeys=['wind_speed','relative_humiditiy','temperature']
    needUnits=['wind_speed_units','temperature_units']
    return [needKeys,needUnits]

def configureNotifications(header):
    """
    Figures out email or text message
    """
    sendTo=''
    valid=createAlert.listSMSGateways()
    if header['email']=='NaN':
        gateway=createAlert.getSMSGateway(header['carrier'],valid)
        sendTo=header['phone']+'@'+gateway
    if header['phone']=='NaN':
        sendTo=header['email']
    return sendTo

def ascertainCfg(Threshold):
#    argFile=str(sys.argv[1])
#    cfgLoc[0]=argFile
    cfgLoc[0]=Threshold
#    if argFile=='':
#        cfgLoc[0]=='/home/tanner/src/FWAS/ui/threshold.cfg'

def runFWAS():
    thresholds=readThresholds()
    headerLib=thresholds[0]
    thresholdsLib=thresholds[1]
    unitLib=thresholds[2]

    zoneStr=calcTime.convertTimeZone(float(headerLib['time_zone']))
    setGlobalVars(float(headerLib['latitude']),float(headerLib['longitude']),float(headerLib['radius']),zoneStr,int(headerLib['limit']))
    setLimits(float(thresholdsLib['temperature']),float(thresholdsLib['wind_speed']),0,0,float(thresholdsLib['relative_humidity']),float(thresholdsLib['wind_gust']))
    setLimitUnits(calcUnits.getWindSpdUnits(float(unitLib['wind_speed_units'])),calcUnits.getTempUnits(float(unitLib['temperature_units'])))

    wxData=getRAWSData(Location[0],Location[1],radius[0],numLimit[0],calcUnits.unitSystemFlag['wind'],calcUnits.unitSystemFlag['temp'])

    wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)

    wxStations=comparator.cleanStations(wxStationsA)

#    for i in range(len(wxStations)):
#        station.printStation(wxStations[i])

    wxLoc=createAlert.getStationDirections(Location,wxStations)
#
    Alert=createAlert.makeSystemAlert(thresholdsLib,unitLimits,wxStations)
#    print Alert
    send.sendEmailAlert(Alert,configureNotifications(headerLib),headerLib['alert_name'])

# cfgLoc[0]='/home/tanner/src/FWAS/ui/thresholds/threshold-USERNAME-2017-05-24_11-24-29.cfg'


#wxS=[x for x in wxS if not x.is_empty]

def runInitialFWAS():
    thresholds=readThresholds()
    headerLib=thresholds[0]
    thresholdsLib=thresholds[1]
    unitLib=thresholds[2]

    zoneStr=calcTime.convertTimeZone(float(headerLib['time_zone']))
    setGlobalVars(float(headerLib['latitude']),float(headerLib['longitude']),float(headerLib['radius']),zoneStr,int(headerLib['limit']))
    setLimits(float(thresholdsLib['temperature']),float(thresholdsLib['wind_speed']),0,0,float(thresholdsLib['relative_humidity']),float(thresholdsLib['wind_gust']))
    setLimitUnits(calcUnits.getWindSpdUnits(float(unitLib['wind_speed_units'])),calcUnits.getTempUnits(float(unitLib['temperature_units'])))

    wxData=getRAWSData(Location[0],Location[1],radius[0],numLimit[0],calcUnits.unitSystemFlag['wind'],calcUnits.unitSystemFlag['temp'])

    wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)

    wxStations=comparator.cleanStations(wxStationsA)

#    for i in range(len(wxStations)):
#        station.printStation(wxStations[i])

    wxLoc=createAlert.getStationDirections(Location,wxStations)
#
    Alert=createAlert.makeSystemAlert(thresholdsLib,unitLimits,wxStations)

    iniAlert="""This message shows that you have successfully created a Fire Weather Alert!
Below are the current conditions and what an alert will look like\n
"""
    firstAlert=iniAlert+Alert

    send.sendEmailAlert(firstAlert,configureNotifications(headerLib),headerLib['alert_name'])
