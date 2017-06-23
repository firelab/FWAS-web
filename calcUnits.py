# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:19:04 2017

@author: tanner


UNITS UTILITY FOR FWAS
"""

import mwlatest
import ConfigParser
import station
from geopy.distance import great_circle
import math
import datetime
import dateutil
import pint

u=pint.UnitRegistry()

"""
Need to convert to Factory Units (Metric)
and then back to
Preferred Units to Print

Assume All Metric for Now

"""

unitFlag={'wind':False,'temp':False} #True if using english units
unitSystemFlag={'wind':"",'temp':""}

def getWindSpdUnits(spdInt):
    """
    Sets units for wind speed, ABV is abbreviation, not alcohol by volume
    """
    spdStr=[""]
    spdAbv=[""]
    if spdInt==1:
       spdStr[0]="meters_per_second"
       spdAbv[0]="mps"
       unitSystemFlag['wind']="default"
    if spdInt==2:
       spdStr[0]="miles_per_hour"
       spdAbv[0]="mph"
       unitFlag['wind']=True
       unitSystemFlag['wind']="english"
#    else:
#       spdStr[0]="meters_per_second"
#       spdAbv[0]="mps"
       
    return [spdStr[0],spdAbv[0]]

def getTempUnits(tInt):
    """
    Sets units for temperature, both full name and abbreviation
    """
    TStr=[""]
    Tabv=[""]
    if tInt==1:
       TStr[0]="Celcius"
       Tabv[0]="C"
       unitSystemFlag['temp']="default"
    if tInt==2:
       TStr[0]="Farenheit"
       Tabv[0]="F"
       unitFlag['temp']=True
       unitSystemFlag['temp']="english"

#    else:
#       TStr[0]="Celcius"
#       Tabv[0]="C"
       
    return [TStr[0],Tabv[0]]

#def addThresholdUnits(thresholds):

def getUnitFlag():
    """
    Returns unit system flag (english or metric)
    """
    return unitFlag


def getPrecipUnits(pInt):
    """
    Returns units of precip in a more meaningful way than 1 or 2, which is specified by the cfg file
    """
    pStr=''
    pAbv=''
    pFlag=''
    if pInt==1:
        pStr='millimeters'
        pAbv='mm'
        pFlag='metric'
    if pInt==2:
        pStr='inches'
        pAbv='in'
        pFlag='english'
    return[pStr,pAbv,pFlag]
"""
Bueno
"""

def windSpeedETM(wind_speed):
    """
    Converts Wind speed from Enlgish (miles/hour) to Metric, (meters/second)
    """
    wSpd=wind_speed*u.miles/u.hour
    wSpd=wSpd.to(u.meters/u.second)
    return wSpd.magnitude

def windSpeedMTE(wind_speed):
    """
    Converts Wind sppeed from mps to mph
    """
    wSpd=wind_speed*u.meters/u.second
    wSpd=wSpd.to(u.miles/u.hour)
    return wSpd.magnitude

def tempETM(temperature):
    """
    Converts Temp from F To C
    """
    tempQ=u.Quantity
    fTemp=tempQ(temperature,u.degF)
    cTemp=fTemp.to(u.degC)
    return cTemp.magnitude

def tempMTE(temperature):
    """
    Converts temp from C To F
    """
    tempQ=u.Quantity
    cTemp=tempQ(temperature,u.degC)
    fTemp=cTemp.to(u.degF)
    return fTemp.magnitude
    
def precipToE(kg): #Converst kg/m^2/s to in/hour
    """
    ConvertsPrecip from kg/m^2/s to inches/hour
    """
    pRate=kg*0.040*u.kg/(u.m**2.*u.second)
    rhoWater=1000.0*u.kg/u.m**3
    pLen=pRate/(rhoWater)
    pLen=pLen.to(u.inch/u.hour)
    return pLen.magnitude

def precipToM(kg): #Converts kg/m^2/s to mm/hour
    """
    Converts Precip from kg/m^2/s to mm/hour
    """
    pRate=kg*0.040*u.kg/(u.m**2.*u.second)
    rhoWater=1000.0*u.kg/u.m**3
    pLen=pRate/(rhoWater)
    pLen=pLen.to(u.mm/u.hour)
    return pLen.magnitude

#def checkThresholdUnits(limits):
#    if unitFlag['wind']==True:
#        









