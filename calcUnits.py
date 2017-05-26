# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:19:04 2017

@author: tanner
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

"""
None of these are used right now
"""

def windSpeedETM(wind_speed):
    wSpd=wind_speed*u.miles/u.hour
    wSpd=wSpd.to(u.meters/u.second)
    return wSpd.magnitude

def windSpeedMTE(wind_speed):
    wSpd=wind_speed*u.meters/u.second
    wSpd=wSpd.to(u.miles/u.hour)
    return wSpd.magnitude

def tempETM(temperature):
    tempQ=u.Quantity
    fTemp=tempQ(temperature,u.degF)
    cTemp=fTemp.to(u.degC)
    return cTemp.magnitude

def tempMTE(temperature):
    tempQ=u.Quantity
    cTemp=tempQ(temperature,u.degC)
    fTemp=cTemp.to(u.degF)
    return fTemp.magnitude


#def checkThresholdUnits(limits):
#    if unitFlag['wind']==True:
#        









