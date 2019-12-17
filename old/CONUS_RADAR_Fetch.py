# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:25:28 2017

@author: tanner
"""

import glob
import urllib2

#hDir='/media/tanner/vol2/CONUS_RADAR/'
hDir='/home/ubuntu/fwas_data/CONUS_RADAR/'

def fetchRadar(fetchGFW):
    """
    Fetches CONUS Base Reflectivity Data as a gif. If for some reason we don't have a gfw
    it can get that too.
    """
    print 'Fetching CONUS RADAR and TimeList...'
    gfwRadar='https://radar.weather.gov/ridge/Conus/RadarImg/latest_radaronly.gfw'
    gifRadar='https://radar.weather.gov/ridge/Conus/RadarImg/latest_radaronly.gif'
    timeRadar='https://radar.weather.gov/ridge/Conus/RadarImg/mosaic_times.txt'

    gifName='conus_radar.gif'
    gfwName='conus_radar.gfw'
    tName='rTimes.txt'

    gifResponse=urllib2.urlopen(gifRadar)
    gifOut=open(str(hDir+gifName),'wb')
    gifOut.write(gifResponse.read())
    gifOut.close()

    tResponse=urllib2.urlopen(timeRadar)
    tOut=open(str(hDir+tName),'wb')
    tOut.write(tResponse.read())
    tOut.close()

    if fetchGFW==True:
        print 'Fetching new GFW File...'
        gfwResponse=urllib2.urlopen(gfwRadar)
        gfwOut=open(str(hDir+gfwName),'wb')
        gfwOut.write(gfwResponse.read())
        gfwOut.close()

