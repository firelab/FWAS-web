# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:37:53 2017

@author: tanner

CHECKER FOR RAWS DATA
"""

import station
import datetime
import dateutil
import numpy
import dateutil.tz


def getObsTime(obs,data,timezone,i):
    """
    Gets the time that the observation was taken
    """
    obsTime=data['STATION'][i]['OBSERVATIONS'][obs]['date_time']
    obsD=obsTime[0:10]
    obsT=obsTime[11:19]
    from_zone=dateutil.tz.gettz('UTC')
    to_zone=dateutil.tz.gettz(timezone)
    utc=datetime.datetime.strptime(obsD+' '+obsT,'%Y-%m-%d %H:%M:%S')
    utc=utc.replace(tzinfo=from_zone)
    local=utc.astimezone(to_zone)
    local=str(local)
    localD=local[0:10]
    localT=local[11:19]
    localOffset=local[19:]
    return [localD,localT,localOffset]
    
def getDateTimeObj(obs,data,timezone,i):
    obsTime=data['STATION'][i]['OBSERVATIONS'][obs]['date_time']
    obsD=obsTime[0:10]
    obsT=obsTime[11:19]
    from_zone=dateutil.tz.gettz('UTC')
    to_zone=dateutil.tz.gettz(timezone)
    utc=datetime.datetime.strptime(obsD+' '+obsT,'%Y-%m-%d %H:%M:%S')
    utc=utc.replace(tzinfo=from_zone)
    local=utc.astimezone(to_zone)
    return local

def getReadableDates(date_str):
    """
    Takes 2017-07-19 and turns it into 07-19-2017
    """
    year=date_str[:4]
    month=date_str[5:7]
    day=date_str[8:]
    newDate=month+'-'+day+'-'+year    
#    print newDate
    return newDate
    
def checkData(stationData,limits,timeZone,unitLimits):
    """
    Checks data to see if it exceeds set thresholds
    """
    warn=[]
    if stationData['SUMMARY']['RESPONSE_MESSAGE']!='OK':
        print 'no RAWS data in the area, checking HRRR!'
        return [station.Station()]
    timeObj=''
    
    for i in range(len(stationData['STATION'])):
        s1=station.Station()
        stid=stationData['STATION'][i]['STID']
        sRH=stationData['STATION'][i]['OBSERVATIONS']['relative_humidity_value_1']['value']
        sSpd=stationData['STATION'][i]['OBSERVATIONS']['wind_speed_value_1']['value']
        sDir=stationData['STATION'][i]['OBSERVATIONS']['wind_direction_value_1']['value']
        sTmp=stationData['STATION'][i]['OBSERVATIONS']['air_temp_value_1']['value']
        sGust=stationData['STATION'][i]['OBSERVATIONS']['wind_gust_value_1']['value']        
        
#        sPr=stationData['STATION'][i]['OBSERVATIONS']['wind_direction_value_1']['value']
#        print stid, sRH
        if sRH<=limits['rh']:
#        if sRH<limits['rh'] or  or 
#            print 'spike!'
            s1.lat=float(stationData['STATION'][i]['LATITUDE'])
            s1.lon=float(stationData['STATION'][i]['LONGITUDE'])
            s1.stid=stid
            s1.name=stationData['STATION'][i]['NAME']
            s1.mnet_id=stationData['STATION'][i]['MNET_ID']
            s1.rh=sRH
            s1.rh_units='%'
            localObsT=getObsTime('relative_humidity_value_1',stationData,timeZone,i)
            timeObj=getDateTimeObj('relative_humidity_value_1',stationData,timeZone,i)            
            s1.date=getReadableDates(localObsT[0])
            s1.time=localObsT[1]
            s1.utc_offset=localObsT[2]
            s1.is_empty=False
#            warn.append(s1)
        if sSpd>=limits['spd']:
            s1.lat=float(stationData['STATION'][i]['LATITUDE'])
            s1.lon=float(stationData['STATION'][i]['LONGITUDE'])
            s1.stid=stid
            s1.name=stationData['STATION'][i]['NAME']
            s1.mnet_id=stationData['STATION'][i]['MNET_ID']
            s1.wind_speed=sSpd
            s1.wind_speed_units=unitLimits['spdABV']
            s1.wind_direction=sDir
            localObsT=getObsTime('wind_speed_value_1',stationData,timeZone,i)
            timeObj=getDateTimeObj('wind_speed_value_1',stationData,timeZone,i)            
            s1.date=getReadableDates(localObsT[0])
            s1.time=localObsT[1]
            s1.utc_offset=localObsT[2]
            s1.is_empty=False            
        if sTmp>=limits['temp']:
#            print sTmp
            s1.lat=float(stationData['STATION'][i]['LATITUDE'])
            s1.lon=float(stationData['STATION'][i]['LONGITUDE'])
            s1.stid=stid
            s1.name=stationData['STATION'][i]['NAME']
            s1.mnet_id=stationData['STATION'][i]['MNET_ID']
            s1.temperature=sTmp
            s1.temperature_units=unitLimits['tempABV']
            localObsT=getObsTime('air_temp_value_1',stationData,timeZone,i)
            timeObj=getDateTimeObj('air_temp_value_1',stationData,timeZone,i)            
            s1.date=getReadableDates(localObsT[0])
            s1.time=localObsT[1]
            s1.utc_offset=localObsT[2]
            s1.is_empty=False
        if sGust>=limits['gust'] and timeObj:
            gustTime=getDateTimeObj('wind_gust_value_1',stationData,timeZone,i)
            if gustTime==timeObj:
                s1.wind_gust=sGust             
        warn.append(s1)
    return warn
    
def cleanStations(uncleanWx):
    """
    Cleans Up data to get rid of zeros and empty stations
    """
    wxS=[x for x in uncleanWx if not x.is_empty]
#    for i in range(len(wxS)):
#        if wxS[i].is_empty==True:
#            del wxS[i]
    for i in range(len(wxS)):
        if wxS[i].rh==0:
            wxS[i].rh=numpy.nan
        if wxS[i].wind_speed==0:
            wxS[i].wind_speed=numpy.nan
            wxS[i].wind_direction=numpy.nan
        if wxS[i].temperature==0:
            wxS[i].temperature=numpy.nan
        if wxS[i].wind_gust==0:
            wxS[i].wind_gust=numpy.nan
            
    return wxS

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
