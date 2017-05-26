# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:47:28 2017

@author: tanner
"""

import station

timeZone=['']
radius=[0.0]
Location=[0.00,0.00]
numLimit=[0]   
unitLimits={'temp':'','tempABV':'','spd':'','spdABV':''}
limits={'temp':0,'spd':0,'dir':0,'rain':0,'rh':0,'gust':0}

cfgLoc=['']

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


cfgLoc[0]='/home/tanner/src/FWAS/ui/thresholds/threshold-USERNAME-2017-05-24_13-6-59.cfg'

s1=station.Station
s1.wind_speed_units='mph'
s1.rh_units='%'
s1.temperature_units='F'

thresholds=readThresholds()
headerLib=thresholds[0]
thresholdsLib=thresholds[1]
unitLib=thresholds[2]

def getThresholdUnits(key,wxStat):
    unit=""
    if key=='wind_speed' or key=='wind_gust':
        unit=wxStat.wind_speed_units
    if key=='temperature':
        unit=wxStat.temperature_units
    if key=='relative_humidity':
        unit=wxStat.rh_units
    return str(unit)

def headerB(thresholds):
    thStr=""
    for i in range(len(thresholds)):
        if thresholds[thresholdsLib.keys()[i]]!='NaN':
            thStr=thStr+thresholds.keys()[i]+\
            ": "+thresholds[thresholds.keys()[i]]+\
            " "+getThresholdUnits(thresholds.keys()[i],s1)+". "
    headerB="Set thresholds are:\n"+thStr+"\n"
    return headerB
    

    
hB=headerB(thresholdsLib)    

print hB    
    
#pan=""
#for i in range(len(thresholdsLib)):
#    if thresholdsLib[thresholdsLib.keys()[i]]!='NaN':
#        pan=pan+thresholdsLib.keys()[i]+\
#        ": "+thresholdsLib[thresholdsLib.keys()[i]]+" "
#
#print pan
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    