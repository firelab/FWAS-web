#!/usr/bin/env python

import datetime
import urllib2

# Fetches all 18 timesteps in forecast initialized on the current day at 1000 UTC
# There is no checking for file existance, so this script must be executed at a 
# reasonable time so that all files are available (0600 MDT?)

#===============================================================================
#     Build the url.
#===============================================================================
def buildUrl(timeStep):
    date = datetime.datetime.now().strftime('%Y%m%d')
    initHour = '10' #0400 MDT
    #timeStep = '01'
    url = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl?file=hrrr.t%sz.wrfprsf%s.grib2&all_lev=on&all_var=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%%2Fhrrr.%s' % (initHour, timeStep, date) 
    print 'url = ', url
    return url

#===============================================================================
#     Fetch the forecast. 
#===============================================================================

def fetchForecast(url):
    print 'Downloading the forecast...'
    dataDir = '/media/tanner/vol2/HRRR/'
    fcastFile = dataDir + url[url.find("file=")+5:url.find(".grib2")] + ".grib2"
    fin = urllib2.urlopen(url)    
    output = open(fcastFile,'wb')
    output.write(fin.read())
    output.close()
    print 'Download complete!'
        

timeList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18']


for time in timeList:
    url = buildUrl(time)
#    fetchForecast(url)
