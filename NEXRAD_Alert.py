# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:56:52 2017

@author: tanner
"""

import datetime

import NEXRAD_radarStation
from HRRR_Alert import getQualRadar
import calcTime

#tZ='America/Denver'
#sName='KMSX'

#d=NEXRAD_radarStation.radarStation()
#d.radar_lat=47.0410003662
#d.radar_lon=-113.986221313
#d.gate_lat=47.2938780227
#d.gate_lon=-113.915427808
#d.gate_dist=27.2593981783
#d.gate_bearing=18.5051615773
#d.gate_cardinal='NNE'
#d.gate_val=32.5
#d.gate_thresh=30.0
#d.date='2017-06-21'
#d.time='16:36:35'
#d.is_empty=False
#d.check=True


def createLocalTime(rS,tz):
    tObj=datetime.datetime.strptime(rS.date+' '+rS.time,'%Y-%m-%d %H:%M:%S')
    lTime=calcTime.utcToLocal(tObj,tz)
    return lTime

def createHeader():
    #line='NEXRAD RADAR ALERT:\n'
    line='THUNDERSTORM RADAR ALERT:\n'
    return line


def createAlert(rS,rLib,tz):
    if rS.is_empty==True:
        return ''
    line=str(rLib['radar_name'])+' reported weather conditions of:'+\
    ' '+str(getQualRadar(rS.gate_val))+' at: '+str(round(rS.gate_dist,1))+\
    ' miles '+str(rS.gate_cardinal)+' of your location. at: '+str(createLocalTime(rS,tz))+'\n'
    return createHeader()+line
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    