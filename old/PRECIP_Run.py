# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 10:52:40 2017

@author: tanner

RAWS PRECIP MODULE
"""

import mwlatest
import datetime
import calcDist
import calcUnits
import calcTime

class precip_station:
    """
    class that represents wxStation precip Ddata
    """
    stid=''
    lat=0.0
    lon=0.0
    dist_from_loc=0.0
    bearing=0.0
    cardinal=''
    precip_1_hour=0.0
    precip_3_hour=0.0
#    dateObj1=datetime.datetime.now()
    utcTime=datetime.datetime.now()
    locTime=datetime.datetime.now()
    precip_units=''
    precip_abv=''
    utc_offset=''
    is_empty=True

def precipUrl(token,lat,lon,radius,limit,pUnits):
    """
    gets Precip with custom URL
    """
    svar="precip_accum_one_hour,precip_accum_one_minute,precip_accum_ten_minute,precip_accum_fifteen_minute,precip_accum_30_minute,precip_accum_three_hour"
#    svar=""    
    within=""
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
    if pUnits=="english":
        units=units+"precip|in,"
    #    if tempUnits=="english":
    #        units=units+"temp|F,"
    #    if precipUnits=="english":
    #        units=units+"precip|in"
    units=unitsBase+units+"metric"
      
    url=mwlatest.baseurl+stidfull+svarfull+"&status=active"+"&network=1,2"+units+timesand+tokfull
    return url

def fetchData(lat,lon,radius,units):
    """
    Fetches precip data from mesowest
    """
    data=mwlatest.readData( precipUrl(mwlatest.dtoken,str(lat),str(lon),str(radius),'',str(units)))
    return data

def sortData(data,lat,lon,units,timeZone):
    """
    Sorts and checks thresholds of data from mesowest
    """
    utc=datetime.datetime.utcnow()
    dObj=datetime.timedelta(hours=1)
    

    if data['SUMMARY']['RESPONSE_MESSAGE']!='OK':
        print 'no RAWS PRECIP data in the area, checking HRRR!'
        return []  
        
    pStations=[]

    for i in range(len(data['STATION'])):
       pStat=precip_station()
       dTime=datetime.datetime.strptime(data['STATION'][i]['OBSERVATIONS']['precip_accum_one_hour_value_1']['date_time'],'%Y-%m-%dT%H:%M:%SZ')
    #   if dTime==utc:
    #       print True,dTime
       if dTime>(utc-dObj):
           print 'Precip Exists! ',dTime
           pStat.stid=data['STATION'][i]['STID']
           pStat.lat=float(data['STATION'][i]['LATITUDE'])
           pStat.lon=float(data['STATION'][i]['LONGITUDE'])
           pStat.precip_1_hour=float(data['STATION'][i]['OBSERVATIONS']['precip_accum_one_hour_value_1']['value'])
           pStat.utcTime=dTime
           pStat.locTime=calcTime.utcToLocal(dTime,timeZone)
           pStat.precip_units=units[0]
           pStat.precip_abv=units[1]
           pStat.is_empty=False
           pStat.dist_from_loc,pStat.bearing,pStat.cardinal=calcDist.getSpatial([float(lat),float(lon)],[pStat.lat,pStat.lon])      
           pStations.append(pStat)
       else:
           print 'No Recent Precip ',utc-dTime
           pStations.append('')
    return pStations
       
def createPrecipAlert(pStations):
    """
    Creates part of alert pertaining to raws precip!
    """
    head=''    
    line=''
    if any(pStations):
#        head='PRECIP ALERT:\n'
        for i in range(len(pStations)):
            if pStations[i]=='':
                line=''
            else:     
                line+='Station '+pStations[i].stid+', '+str(round(pStations[i].dist_from_loc,1))+' miles at '+str(round(pStations[i].bearing,1))+' degrees '+str(pStations[i].cardinal)+\
                ' from your location reported '+str(pStations[i].precip_1_hour)+' '+str(pStations[i].precip_units)+' of liquid precip within the last hour.\n'
    return line

#precipLib={'precip_on': '1', 'precip_units': '2'}
#headerLib={'alert_name': 'Alert',
# 'alert_time': '2017-06-15 13:02:07',
# 'carrier': 'NaN',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '47.92',
# 'limit': '0',
# 'longitude': '-122.1',
# 'phone': 'NaN',
# 'radius': '12',
# 'time_zone': '2'}
#
#tZ=['America/Denver']



def doPrecip(pUnits,headerLib,timeZone):
    """
    Runs precip module!
    """
#    pUnits=calcUnits.getPrecipUnits(int(precipLib['precip_units']))
    pData=fetchData(headerLib['latitude'],headerLib['longitude'],headerLib['radius'],pUnits[2])    
    pStations=sortData(pData,headerLib['latitude'],headerLib['longitude'],pUnits,timeZone)
    pAlert=createPrecipAlert(pStations)
    return pAlert
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    






