# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:47:27 2017

@author: tanner
"""


"""
CC is the model cycle runtime 
FF is the forecast hour

http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl?
file=hrrr.t12z.wrfsfcf12.grib2
&lev_10_m_above_ground=on&lev_2_m_above_ground=on
&lev_entire_atmosphere=on&var_REFC=on&var_RH=on
&var_TMP=on&var_UGRD=on&var_VGRD=on&var_WIND=on
&leftlon=0&rightlon=360&toplat=90
&bottomlat=-90&dir=%2Fhrrr.20170605

"""
import datetime
import urllib2
import glob
import os


def buildURL(simHour,fetchHour):
    baseUrl='http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl'
    
#    simHour='12'
#    fetchHour='12'
    
    uFile='?file=hrrr.t'+str(simHour)+'z.wrfsfcf'+str(fetchHour)+'.grib2'
    mid='''&lev_10_m_above_ground=on&lev_2_m_above_ground=on\
&lev_entire_atmosphere=on&var_REFC=on&var_RH=on\
&var_TMP=on&var_UGRD=on&var_VGRD=on&var_WIND=on\
&leftlon=0&rightlon=360&toplat=90\
&bottomlat=-90&dir=%2Fhrrr.'''
    
    simDay=datetime.datetime.utcnow().strftime('%Y%m%d')
    
    URL=baseUrl+uFile+mid+simDay
    return URL
    

def getForecast(URL):
    dataDir='/media/tanner/vol2/HRRR/grib/'
    forecastFile=dataDir+URL[URL.find("file=")+5:URL.find(".grib2")]+".grib2"
    response=urllib2.urlopen(URL)
    output=open(forecastFile,'wb')
    output.write(response.read())
    output.close()

def cleanHRRRDir():
    gZ=glob.glob('/media/tanner/vol2/HRRR/grib/*.grib2')
    for i in range(len(gZ)):
        os.remove(gZ[i])

timeList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18']

sixHourTimeList=['00', '01', '02', '03', '04', '05', '06']

def runFetchHRRR(tList):
    #get pretty close to most recent simulation time for now
    simHour=str(datetime.datetime.utcnow().hour-2)   
    for time in tList:
        url = buildURL(simHour,time)
        getForecast(url)


















