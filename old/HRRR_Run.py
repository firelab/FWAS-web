# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 20:39:03 2017

@author: tanner


RUN HRRR PARSE
"""

import HRRR_Parse
import calcUnits
import calcTime
import numpy

#unitLib={'temperature_units': '2', 'wind_speed_units': '2'}
#thresholdsLib={'relative_humidity': '75',
# 'temperature': '5',
# 'wind_gust': '10',
# 'wind_speed': '2'}
#headerLib={'alert_name': 'Alert',
# 'alert_time': '2017-06-06 19:50:01',
# 'carrier': 'NaN',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '46.92',
# 'limit': '0',
# 'longitude': '-114.1',
# 'phone': 'NaN',
# 'radius': '12',
# 'time_zone': '2'}
#HRRRLib={'forecast_on': '1',
# 'reflectivity': '1',
# 'relative_humidity': '1',
# 'temperature': '1',
# 'wind_speed': '1'}

unitFlag={'wind':False,'temp':False}

def run_HRRR(hrrr_ds,radius,lat,lon,reflec,temp,rh,wind,sanityCheck):
    """
    Runs HRRR checker for all timeSteps on Disk
    """
    mFCast=[]    
    hrrr_ds.sort()
    
#    tSteps=HRRR_Parse.getDiskFiles()
    
    for i in range(len(hrrr_ds)):
        sfcast=HRRR_Parse.setControls(hrrr_ds[i],radius,lat,lon,reflec,temp,rh,wind,sanityCheck)
        mFCast.append(sfcast)
    return mFCast        

def checkForNaN(thresholdsLib):
    """
    Checks to see if the user doesn't want some of the variables
    """
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
    """
    Sets variables for Reflectivity and RH, rh is user set, REFLECTIVITY IS SET HERE AND CAN BE CHANGED HERE!
    """
    refec=30 #Hard Coded for now
    rh=thresholdsLib['relative_humidity']
    return [refec,rh]

def returnUserUnits(fCast,unitsFlag):
    """
    converst HRRR units back into the units the user wants ie C to F and mps to MPH
    """
    for i in range(len(fCast)):
        if unitsFlag['temp']==True: #User Wants English
            MBtmp=calcUnits.tempMTE(fCast[i][1].limit)
            MCtmp=calcUnits.tempMTE(fCast[i][1].eVal)
            MAtmp=calcUnits.tempMTE(fCast[i][1].average)
            MStmp=calcUnits.tempMTE(fCast[i][1].stDev)
            MDtmp=calcUnits.tempMTE(fCast[i][1].obs_max)
#            print fCast[i][1].average,MAtmp
            fCast[i][1].limit=MBtmp
            fCast[i][1].eVal=MCtmp
            fCast[i][1].units='F'
            fCast[i][1].average=MAtmp
            fCast[i][1].stDev=MStmp      
            fCast[i][1].obs_max=MDtmp
        if unitsFlag['wind']==True: #User Wants English 
            MAwSpd=calcUnits.windSpeedMTE(fCast[i][5].average)
            MSwSpd=calcUnits.windSpeedMTE(fCast[i][5].stDev)
            MBwSpd=calcUnits.windSpeedMTE(fCast[i][5].limit)
            MCwSpd=calcUnits.windSpeedMTE(fCast[i][5].eVal)
            MDwSpd=calcUnits.windSpeedMTE(fCast[i][5].obs_max)
            
            fCast[i][5].units='mph'
            fCast[i][5].average=MAwSpd
            fCast[i][5].stDev=MSwSpd
            fCast[i][5].limit=MBwSpd
            fCast[i][5].eVal=MCwSpd
            fCast[i][5].obs_max=MDwSpd
        
#        print fCast[i][1].units,fCast[i][5].units
#    return fCast

def returnPrecipUnits(fCasts,pUnits):
    """
    Returns Precip in a more understandable set of units
    """
    for i in range(len(fCasts)):
        if pUnits[2]=='english':           
            fCasts[i][4].limit=calcUnits.precipToE(fCasts[i][4].limit)
            fCasts[i][4].eVal=calcUnits.precipToE(fCasts[i][4].eVal)
            fCasts[i][4].average=calcUnits.precipToE(fCasts[i][4].average)
            fCasts[i][4].stDev=calcUnits.precipToE(fCasts[i][4].stDev)
            fCasts[i][4].units='inches/hour'
        if pUnits[2]=='metric':
            fCasts[i][4].limit=calcUnits.precipToM(fCasts[i][4].limit)
            fCasts[i][4].eVal=calcUnits.precipToM(fCasts[i][4].eVal)
            fCasts[i][4].average=calcUnits.precipToM(fCasts[i][4].average)
            fCasts[i][4].stDev=calcUnits.precipToM(fCasts[i][4].stDev)
            fCasts[i][4].units='mm/hour'
    
def forecastOptions(fCastLib):
    """
    Determines if the HRRR checker should be run for this user.
    """
    if fCastLib['forecast_on']=='1':
        go=True
    if fCastLib['forecast_on']=='0':
        go=False
    dur=int(fCastLib['forecast_duration'])
    return [go,dur]    


    

#HLib=checkForNaN(thresholdsLib)
#specVals=checkUnits(unitFlag,HLib)
#genVals=getRHandReflec(HLib)
##
#fCastRuns=run_HRRR(int(headerLib['radius']),float(headerLib['latitude']),float(headerLib['longitude']),float(genVals[0]),float(specVals[1]),float(genVals[1]),float(specVals[0]),False)
#                    
#returnUserUnits(fCastRuns,unitFlag)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    



    