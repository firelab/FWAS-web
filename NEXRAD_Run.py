# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:08:45 2017

@author: tanner
"""

import NEXRAD_Fetch
import NEXRAD_Parse
import NEXRAD_Alert
#import NEXRAD_radarStation

#def readRadarThresholds()

def runNEXRAD(headerLib,rLib,timeZone):
    stid=rLib['radar_name']
    loc=[headerLib['latitude'],headerLib['longitude']]
    fileLoc=NEXRAD_Fetch.fetchStation(stid)
    rStation=NEXRAD_Parse.checkRadar(fileLoc,False,loc)
    alert=NEXRAD_Alert.createAlert(rStation,rLib,timeZone)
    return alert














































