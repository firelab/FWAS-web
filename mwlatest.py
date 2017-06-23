# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 10:53:00 2016

@author: tanner

RAWS FETCHER
"""

import urllib2
import json
import csv

baseurl="http://api.mesowest.net/v2/stations/latest?"
dtoken="33e3c8ee12dc499c86de1f2076a9e9d4"

def stationUrlBuilder(token,stid,svar,within,spdUnits,tempUnits):
    tokfull="&token="+token
    stidfull="stid="+stid
    svarfull="&vars="+svar
    if svar=="":
        print "urlBuilder: downloading all variables for station"
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    url=baseurl+stidfull+svarfull+timesand+tokfull
    return url
def radiusUrlBuilder(token,stid,radius,limit,svar,within):
    tokfull="&token="+token
    stidfull="&radius="+stid+","+radius
    svarfull="&vars="+svar
    if svar=="":
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
    limiter="&limit="+limit
    url=baseurl+stidfull+svarfull+limiter+timesand+tokfull
    return url
def latlonBuilder(token,lat,lon,radius,limit,svar,within,spdUnits,tempUnits):
    tokfull="&token="+token
    stidfull="&radius="+lat+","+lon+","+radius
    svarfull="&vars="+svar
    if svar=="":
        svarfull=""
    timesand="&within="+str(within)
    if within=="":
        timesand=""
#    limiter="&limit="+limit
    unitsBase="&units="
    units=""
    if spdUnits=="english":
        units=units+"speed|mph,"
    if tempUnits=="english":
        units=units+"temp|F,"
#    if precipUnits=="english":
#        units=units+"precip|in"
    units=unitsBase+units+"metric"
  
    url=baseurl+stidfull+svarfull+"&status=active"+"&network=1,2"+units+timesand+tokfull
    return url
    
def readData(url):
    new=urllib2.urlopen(url)
    response=new.read()
    json_string=response
    a=json.loads(json_string)
    return a
    
def writeToCSV(dictData,csvName):
    r"""
    Writes a CSV of weather data for a dataset, special for WindNinja
    
    Arguments:
    ----------
    dictData:
        A dictionary of the data is required, json_interpret creates a dicitonary
    from the json data downloaded (use it)
    
    csvName: 
        NAME YOUR FILE!

    """
    lib=dictData
    datLen=len(lib['STATION'])
    with open(csvName,'wb') as csvfile:
        blue=csv.writer(csvfile,delimiter=',')
        for j in range(datLen):
            header=list()
            obsRow=list()
            dictKey=lib['STATION'][j]['OBSERVATIONS'].keys()
            keyLen=len(dictKey)
            
#            obsLen=len(lib['STATION'][j]['OBSERVATIONS']['date_time'])
            stationInfo=[lib['STATION'][j]['NAME'],lib['STATION'][j]['LATITUDE'],
                         lib['STATION'][j]['LONGITUDE'],lib['STATION'][j]['TIMEZONE'],
                         lib['STATION'][j]['STID']]   
            for ex in range(keyLen):
                header.append(dictKey[ex])        
            
            blue.writerow(stationInfo)
            blue.writerow(header)
            for k in range(1):
                obsRow=list()
                for i in range(keyLen):
                    obsRow.append( lib['STATION'][j]['OBSERVATIONS'][dictKey[i]][k])            
                blue.writerow((obsRow))    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     