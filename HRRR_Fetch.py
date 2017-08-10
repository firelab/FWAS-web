# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 14:47:27 2017

@author: tanner

FETCHES CURRENT HRRR DATA FOR NEXT SIX HOURS IDEALLY

NOW WITH MULTIPROCESSING!
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
from multiprocessing.dummy import Pool as ThreadPool 
import time

def buildURL(simHour,fetchHour):
    """
    Builds the most recent URL for HRRR Data
    """
    baseUrl='http://nomads.ncep.noaa.gov/cgi-bin/filter_hrrr_2d.pl'
    
#    simHour='12'
#    fetchHour='12'
    
    uFile='?file=hrrr.t'+str(simHour)+'z.wrfsfcf'+str(fetchHour)+'.grib2'
#    mid='''&lev_10_m_above_ground=on&lev_2_m_above_ground=on\
#&lev_entire_atmosphere=on&var_REFC=on&var_RH=on\
#&var_TMP=on&var_UGRD=on&var_VGRD=on&var_WIND=on\
#&leftlon=0&rightlon=360&toplat=90\
#&bottomlat=-90&dir=%2Fhrrr.'''
    mid='''&lev_surface=on&lev_10_m_above_ground=on&lev_2_m_above_ground=on\
&lev_entire_atmosphere=on&var_REFC=on&var_RH=on\
&var_TMP=on&var_PRATE=on&var_LTNG=on&var_WIND=on\
&leftlon=0&rightlon=360&toplat=90\
&bottomlat=-90&dir=%2Fhrrr.'''
    
    simDay=datetime.datetime.utcnow().strftime('%Y%m%d')
    
    URL=baseUrl+uFile+mid+simDay
    return URL
    

def getForecast(URL):
    """
    Fetches HRRR data!
    """
#    dataDir='/home/tanner/src/breezy/HRRR/grib/'
    dataDir='/home/ubuntu/fwas_data/HRRR/grib/'
    forecastFile=dataDir+URL[URL.find("file=")+5:URL.find(".grib2")]+".grib2"
    response=urllib2.urlopen(URL)
    output=open(forecastFile,'wb')
    output.write(response.read())
    output.close()

def backupHRRRDir():
    """
    Backs up data in case we want it, doesn't do anything right now
    """
#    gZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
    gZ=glob.glob('/home/ubuntu/fwas_data/HRRR/grib/*.grib2')
    for i in range(len(gZ)):
#        os.rename(gZ[i],'/home/tanner/src/breezy/HRRR/past/'+gZ[i][35:])
 	os.rename(gZ[i],'/home/ubuntu/fwas_data/HRRR/shiit/'+gZ[i][35:])
    
def cleanHRRRDir():
    """
    deletes old HRRR data!
    """
    print "Deleting old HRRR Files..."
#    gZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
    gZ=glob.glob('/home/ubuntu/fwas_data/HRRR/grib/*.grib2')
    for i in range(len(gZ)):
        os.remove(gZ[i])

timeList = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
            '11', '12', '13', '14', '15', '16', '17', '18']

#sixHourTimeList=['00', '01', '02', '03', '04', '05', '06']
sixHourTimeList=['01', '02', '03', '04', '05', '06','07']
fiveHourTimeList=['01', '02', '03', '04', '05','06']

def OLDrunFetchHRRR(tList,recent):
    """
    Runs HRRR for a time List
    """
    print "Fetching HRRR grib files...."
    #get pretty close to most recent simulation time for now
    simHour=str(datetime.datetime.utcnow().hour-recent)
    simHour=simHour.zfill(2)
    for xT in tList:
        url = buildURL(simHour,xT)
#	print url
        getForecast(url)
        print "Forecast Acquired, downloading..."
        
def runFetchHRRR(tList,recent):
    """
    Runs HRRR for a time List
    """
    print "Fetching HRRR grib files...."
    #get pretty close to most recent simulation time for now
    simHour=str(datetime.datetime.utcnow().hour-recent)
    simHour=simHour.zfill(2)
    uList=[]
    for xT in tList:
        url = buildURL(simHour,xT)
        uList.append(url)
    pool = ThreadPool(6) #Because there are 6 forecasts this is the fastest!
    results=pool.map(getForecast,uList)
    pool.close()
    pool.join()
    
    
#cleanHRRRDir()

def fetchHRRR():
    """
    Runs HRRR With error handling! If you can't get most recent 6 hour data, tries 5 hour data, and then tries last hours data!
    """
    start=time.time()
    try:
        print 'Trying Most Recent HRRR Data, 6 Hour Forecast'
        runFetchHRRR(sixHourTimeList,1)
    except:
        print 'Could not get six hour Forecasts. Trying Five Hour'
        pass
        try:
            runFetchHRRR(fiveHourTimeList,1)
        except:
            print 'Could not get Five Hour Forecasts. Fetching Last Hours 6 Hour Forecast'
            pass
            try:
                runFetchHRRR(sixHourTimeList,2)
            except:
                print 'DAMN! DAMN! COAL BURNING DING! DING!'
                raise
    end=time.time()
    print 'HRRR GRIB FETCHED IN:',end-start,'SECONDS...'

#
#cleanHRRRDir()
#fetchHRRR()


simHour=str(datetime.datetime.utcnow().hour-1)   
print simHour
