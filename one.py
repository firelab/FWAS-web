#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:55:23 2017

@author: tanner

(used to be called 1.0.py)
PRIMARY RUN SCRIPT FOR RAWS AND HRRR
"""
#System Libraries
import ConfigParser
from geopy.distance import great_circle
import math
import datetime
import dateutil
import pint
import numpy
import sys
#My Mesowest Library
import mwlatest
#Local Core Libraries
import send
import calcTime
import calcUnits
import createAlert
#Local RAWS specific Libraries
import RAWS_comparator as comparator
import station
from station import printStation
#HRRR Libraries
import HRRR_Fetch
import HRRR_Run
import HRRR_Alert
#Precip Libraries
import PRECIP_Run
#NEXRAD Libraries (Maybe?)

from pympler import asizeof

#import unifiedAlert

def getRAWSData(Lat,Lon,Radius,limit,spdUnits,tempUnits):
    """
    Internal RAWS fetcher. Uses Mesowest API
    """
    url=mwlatest.latlonBuilder(mwlatest.dtoken,str(Lat),str(Lon),str(Radius),"","relative_humidity,air_temp,wind_speed,wind_direction,wind_gust","",str(spdUnits),str(tempUnits))
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
    forecastDict={}
    precipDict={}
    radarDict={}
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
    options=cfg.options(cfg.sections()[3])
    section=cfg.sections()[3]
    for i in range(len(options)):
        forecastDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[4])
    section=cfg.sections()[4]
    for i in range(len(options)):
        precipDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[5])
    section=cfg.sections()[5]
    for i in range(len(options)):
        radarDict[options[i]]=cfg.get(section,options[i])
    return [headerDict,thresholdDict,unitDict,forecastDict,precipDict,radarDict]

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
    """
    Sets cfg file to the one that is currently being read
    """
#    argFile=str(sys.argv[1])
#    cfgLoc[0]=argFile
    cfgLoc[0]=Threshold
#    if argFile=='':
#        cfgLoc[0]=='/home/tanner/src/FWAS/ui/threshold.cfg'

def runFWAS():
    """
    General Run Function 
    """
    print 'Reading Thresholds for: '+str(cfgLoc[0])
    thresholds=readThresholds()
    headerLib=thresholds[0]
    thresholdsLib=thresholds[1]
    unitLib=thresholds[2]
    HRRRLib=thresholds[3]
    precipLib=thresholds[4]

    print 'Setting Limits...'
    zoneStr=calcTime.convertTimeZone(float(headerLib['time_zone']))
    setGlobalVars(float(headerLib['latitude']),float(headerLib['longitude']),float(headerLib['radius']),zoneStr,int(headerLib['limit']))
    setLimits(float(thresholdsLib['temperature']),float(thresholdsLib['wind_speed']),0,0,float(thresholdsLib['relative_humidity']),float(thresholdsLib['wind_gust']))
    setLimitUnits(calcUnits.getWindSpdUnits(float(unitLib['wind_speed_units'])),calcUnits.getTempUnits(float(unitLib['temperature_units'])))

    pUnits=calcUnits.getPrecipUnits(int(precipLib['precip_units']))

    print 'Fetching RAWS Data...'
    wxData=getRAWSData(Location[0],Location[1],radius[0],numLimit[0],calcUnits.unitSystemFlag['wind'],calcUnits.unitSystemFlag['temp'])

    print 'Checking RAWS Data...'
    wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)
    
    print 'Cleaning WxStations...'
    wxStations=comparator.cleanStations(wxStationsA)
    
    print 'Checking HRRR Options...'
    hList=HRRR_Run.forecastOptions(HRRRLib)
    h_Alert=['','','','','','']
    if hList[0]==True:
        HLib=HRRR_Run.checkForNaN(thresholdsLib)
        localUnits=calcUnits.getUnitFlag()
        specVals=HRRR_Run.checkUnits(localUnits,HLib)
        genVals=HRRR_Run.getRHandReflec(HLib)
        print 'Running HRRR Threshold Checks...'
        fCastRuns=HRRR_Run.run_HRRR(int(headerLib['radius']),float(headerLib['latitude']),
                           float(headerLib['longitude']),float(genVals[0]),
                            float(specVals[1]),float(genVals[1]),float(specVals[0]),False)
        HRRR_Run.returnUserUnits(fCastRuns,localUnits)
        HRRR_Run.returnPrecipUnits(fCastRuns,pUnits)

        
        print 'Creating HRRR Alert...'
        h_Alert=HRRR_Alert.createVarAlert(fCastRuns,headerLib,unitLimits,HLib)
        if precipLib['precip_on']=='0':
            h_Alert[4]=''
            
    p_Alert=''
    print 'Checking Precip...'
    if precipLib['precip_on']=='1':
        p_Alert=PRECIP_Run.doPrecip(pUnits,headerLib,timeZone[0])
    
    print 'Locating WxStations...'
    wxLoc=createAlert.getStationDirections(Location,wxStations)

    print 'Creating System Alert...'
    Alert=createAlert.createSysAlert(headerLib,thresholdsLib,unitLimits,wxStations,h_Alert,p_Alert,timeZone[0])

    if wxStations or any(h_Alert):
        print "Thresholds Met!"
        send.sendEmailAlert(Alert,configureNotifications(headerLib),headerLib['alert_name'])
    if not wxStations and not any(h_Alert):
        print "No Thresholds Met: Not Sending Alert!"


#    Alert=createAlert.makeSystemAlert(thresholdsLib,unitLimits,wxStations)
#    if wxStations:
#        send.sendEmailAlert(Alert,configureNotifications(headerLib),headerLib['alert_name'])
#    if not wxStations:
#        print "No Thresholds Met: Not Sending Alert!"
# cfgLoc[0]='/home/tanner/src/FWAS/ui/thresholds/threshold-USERNAME-2017-05-24_11-24-29.cfg'


#wxS=[x for x in wxS if not x.is_empty]

def runInitialFWAS():
    """
    Alert creation run Function
    """
    thresholds=readThresholds()
    headerLib=thresholds[0]
    thresholdsLib=thresholds[1]
    unitLib=thresholds[2]
    HRRRLib=thresholds[3]
    precipLib=thresholds[4]
    radarLib=thresholds[5]


    zoneStr=calcTime.convertTimeZone(float(headerLib['time_zone']))
    setGlobalVars(float(headerLib['latitude']),float(headerLib['longitude']),float(headerLib['radius']),zoneStr,int(headerLib['limit']))
    setLimits(float(thresholdsLib['temperature']),float(thresholdsLib['wind_speed']),0,0,float(thresholdsLib['relative_humidity']),float(thresholdsLib['wind_gust']))
    setLimitUnits(calcUnits.getWindSpdUnits(float(unitLib['wind_speed_units'])),calcUnits.getTempUnits(float(unitLib['temperature_units'])))

    pUnits=calcUnits.getPrecipUnits(int(precipLib['precip_units']))

    wxData=getRAWSData(Location[0],Location[1],radius[0],numLimit[0],calcUnits.unitSystemFlag['wind'],calcUnits.unitSystemFlag['temp'])

    wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)

    wxStations=comparator.cleanStations(wxStationsA)

    print 'Checking HRRR Options...'
    hList=HRRR_Run.forecastOptions(HRRRLib)
    h_Alert=['','','','','','']
    if hList[0]==True:
#        HRRR_Fetch.cleanHRRRDir() #We don't Do this for instant Alerts because it would just destroy everything!
#        HRRR_Fetch.fetchHRRR()  #We don't Do this for instant Alerts because it would just destroy everything!
    #    HRRR_Fetch.runFetchHRRR(HRRR_Fetch.sixHourTimeList)
        HLib=HRRR_Run.checkForNaN(thresholdsLib)
        localUnits=calcUnits.getUnitFlag()
        specVals=HRRR_Run.checkUnits(localUnits,HLib)
        genVals=HRRR_Run.getRHandReflec(HLib)
        print 'Running HRRR Threshold Checks...'
        fCastRuns=HRRR_Run.run_HRRR(int(headerLib['radius']),float(headerLib['latitude']),
                           float(headerLib['longitude']),float(genVals[0]),
                            float(specVals[1]),float(genVals[1]),float(specVals[0]),False)
        HRRR_Run.returnUserUnits(fCastRuns,localUnits)
        HRRR_Run.returnPrecipUnits(fCastRuns,pUnits)

        h_Alert=HRRR_Alert.createVarAlert(fCastRuns,headerLib,unitLimits,HLib)
        if precipLib['precip_on']=='0':
            h_Alert[4]=''
            
    p_Alert=''
    print 'Checking Precip...'
    if precipLib['precip_on']=='1':
        p_Alert=PRECIP_Run.doPrecip(pUnits,headerLib,timeZone[0])

    wxLoc=createAlert.getStationDirections(Location,wxStations)
    
    Alert=createAlert.createSysAlert(headerLib,thresholdsLib,unitLimits,wxStations,h_Alert,p_Alert,timeZone[0])

#    Alert=createAlert.makeSystemAlert(thresholdsLib,unitLimits,wxStations)

    iniAlert="""You have successfully created a Fire Weather Alert!
Current Weather Conditions:\n
"""
    if wxStations or any(h_Alert):
        firstAlert=iniAlert+Alert
        send.sendEmailAlert(firstAlert,configureNotifications(headerLib),headerLib['alert_name'])
    if not wxStations and not any(h_Alert):
        siniAlert="No Stations Currently Meet Alert Thresholds. Alert has been set and will check hourly!"
        firstAlert=iniAlert+siniAlert
        send.sendEmailAlert(firstAlert,configureNotifications(headerLib),headerLib['alert_name'])
"""
################################################
#                                              #
# Below are functions to be used for debugging #
#                                              #
################################################
"""

#HRRR_Fetch.cleanHRRRDir() #We don't Do this for instant Alerts because it would just destroy everything!
#HRRR_Fetch.fetchHRRR()  #We don't Do this for instant Alerts because it would just destroy everything!
#

#cfgLoc[0]='/home/tanner/src/breezy/fwas/data/threshold-USERNAME-2017-06-21_09-26-37.cfg'
#print 'Reading Thresholds for: '+str(cfgLoc[0])
#thresholds=readThresholds()
#headerLib=thresholds[0]
#thresholdsLib=thresholds[1]
#unitLib=thresholds[2]
#HRRRLib=thresholds[3]
#precipLib=thresholds[4]
#radarLib=thresholds[5]
###
#print 'Setting Limits...'
#zoneStr=calcTime.convertTimeZone(float(headerLib['time_zone']))
#setGlobalVars(float(headerLib['latitude']),float(headerLib['longitude']),float(headerLib['radius']),zoneStr,int(headerLib['limit']))
#setLimits(float(thresholdsLib['temperature']),float(thresholdsLib['wind_speed']),0,0,float(thresholdsLib['relative_humidity']),float(thresholdsLib['wind_gust']))
#setLimitUnits(calcUnits.getWindSpdUnits(float(unitLib['wind_speed_units'])),calcUnits.getTempUnits(float(unitLib['temperature_units'])))
###
#pUnits=calcUnits.getPrecipUnits(int(precipLib['precip_units']))
###
#print 'Fetching RAWS Data...'
###
#wxData=getRAWSData(Location[0],Location[1],radius[0],numLimit[0],calcUnits.unitSystemFlag['wind'],calcUnits.unitSystemFlag['temp'])
###
#print 'Checking RAWS Data...'
###
#wxStationsA=comparator.checkData(wxData,limits,timeZone[0],unitLimits)
###
#print 'Cleaning WxStations...'
###
#wxStations=comparator.cleanStations(wxStationsA)
##
#del wxStationsA




#print 'Checking HRRR Options...'
#hList=HRRR_Run.forecastOptions(HRRRLib)
#h_Alert=['','','','','','']
#if hList[0]==True:
#    HLib=HRRR_Run.checkForNaN(thresholdsLib)
#    localUnits=calcUnits.getUnitFlag()
#    specVals=HRRR_Run.checkUnits(localUnits,HLib)
#    genVals=HRRR_Run.getRHandReflec(HLib)
#    print 'Running HRRR Threshold Checks...'
#    fCastRuns=HRRR_Run.run_HRRR(int(headerLib['radius']),float(headerLib['latitude']),
#                       float(headerLib['longitude']),float(genVals[0]),
#                        float(specVals[1]),float(genVals[1]),float(specVals[0]),False)
#    HRRR_Run.returnUserUnits(fCastRuns,localUnits)
#    HRRR_Run.returnPrecipUnits(fCastRuns,pUnits)
###        
#    print 'Creating HRRR Alert...'
#    h_Alert=HRRR_Alert.createVarAlert(fCastRuns,headerLib,unitLimits,HLib)
#    if precipLib['precip_on']=='0':
#        h_Alert[4]=''
#
#p_Alert=''
#print 'Checking Precip...'
#if precipLib['precip_on']=='1':
#    p_Alert=PRECIP_Run.doPrecip(pUnits,headerLib,timeZone[0])
##
#print 'Locating WxStations...'
#wxLoc=createAlert.getStationDirections(Location,wxStations)
##
#print 'Creating System Alert...'
#Alert=createAlert.createSysAlert(headerLib,thresholdsLib,unitLimits,wxStations,h_Alert,p_Alert,timeZone[0])
##if wxStations or any(h_Alert):
##    print "Thresholds Met!"
##    send.sendEmailAlert(Alert,configureNotifications(headerLib),headerLib['alert_name'])
##if not wxStations and not any(h_Alert):
##    print "No Thresholds Met"in range(len(wxStations)):
###    xx.














