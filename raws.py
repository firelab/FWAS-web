# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:56:40 2017

@author: tanner

will need to check Setup Multiple unit Systems
DEPRECATED, NO LONGER NEEDED
"""


import mwlatest
import ConfigParser
import station
from geopy.distance import great_circle
import math
import datetime
import dateutil
import send
"""
Builds a URL at LAT, LON within 12 miles and a limit of 20 stations
"""

def getRAWSData(Lat,Lon,Radius):
    url=mwlatest.latlonBuilder(mwlatest.dtoken,str(Lat),str(Lon),str(Radius),'20',"relative_humidity","")
    response=mwlatest.readData(url)
    return response

timeZone='America/Denver' #These are hard coded in for the moment
myLoc=[46.9,-114.13] #These are hard coded in for the moment
radius=12
wxData=getRAWSData(myLoc[0],myLoc[1],radius)
#print len(wxData['STATION'])


"""
Check for Changes in weather
in
Temperature (C)
Wind Speed (m/s)
Wind Direction (deg)
Accum Precip (mm)
Relative Humidity (%)<- Only One that works right now
"""
warnVar={'temp':0,'spd':0,'dir':0,'rain':0,'rh':0}
limits={'temp':0,'spd':0,'dir':0,'rain':0,'rh':0}

def setLimits(temp,spd,direction,Precip,RH):
    limits['temp']=temp
    limits['spd']=spd
    limits['dir']=direction
    limits['rain']=Precip
    limits['rh']=RH


def readThresholds():
    cfg=ConfigParser.ConfigParser()
    cfg.read('/home/tanner/src/FWAS/ui/threshold.cfg')
    thresholdDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        thresholdDict[options[i]]=cfg.get(section,options[i])
    return thresholdDict

thresholds=readThresholds()

setLimits(0,0,0,0,float(thresholds['relative_humidity']))

def getObsTime(obs,data,timezone,i):
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
    localOffset=local[20:]
    return [localD,localT,localOffset]

def checkRHdata(stationData):
    warn=[]
    for i in range(len(stationData)):
        s1=station.Station()
        stid=stationData['STATION'][i]['STID']
        sRH=stationData['STATION'][i]['OBSERVATIONS']['relative_humidity_value_1']['value']
#        print stid, sRH
        if sRH<limits['rh']:
#            print 'spike!'
            s1.lat=float(stationData['STATION'][i]['LATITUDE'])
            s1.lon=float(stationData['STATION'][i]['LONGITUDE'])
            s1.stid=stid
            s1.rh=sRH
            s1.rh_units='%'
            localObsT=getObsTime('relative_humidity_value_1',stationData,timeZone,i)
            s1.date=localObsT[0]
            s1.time=localObsT[1]
            s1.utc_offset=localObsT[2]
            warn.append(s1)
    return warn

rhWarn=checkRHdata(wxData)

#d=great_circle(myLoc,[rhWarn[1].lat,rhWarn[1].lon]).miles

def getBearing(lat1,lon1,lat2,lon2):
    lat1=math.radians(lat1)
    lon1=math.radians(lon1)
    lat2=math.radians(lat2)
    lon2=math.radians(lon2)
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = math.atan2(y, x)
    brng=math.degrees(brng)
    if brng < 0:
       brng+= 360
    return brng
    
#p=getBearing(myLoc[0],myLoc[1],rhWarn[1].lat,rhWarn[1].lon)

def getSpatial(location,station):
    lat1=location[0]
    lon1=location[1]
    lat2=station.lat
    lon2=station.lon
    distance=great_circle([lat1,lon1],[lat2,lon2]).miles #Miles is harded coded for the moment
    bearing=getBearing(lat1,lon1,lat2,lon2)
    
    return [distance,bearing]    

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
#    print arr[(val % 16)]
    return arr[(val % 16)]
    
  
def createAlert():
    Alert=""
    if len(rhWarn)>0:
        warnLoc=[]    
        for i in range(len(rhWarn)):
            wL=getSpatial(myLoc,rhWarn[i])
            warnLoc.append(wL)
            a= "Station "+str(rhWarn[i].stid)+", "+str(round(warnLoc[i][0],2))+" miles at "+str(round(warnLoc[i][1],1))+" degrees "+str(degToCompass((round(warnLoc[i][1],1))))+" from your location has a "
            b= str(thresholds.keys()[0])+" of "+str(rhWarn[i].rh)+" %. Observation Taken at: "+str(rhWarn[i].date)+" "+str(rhWarn[i].time)+" Local Time"
            component=str(a)+str(b)
#            print a
#            print type(a),type(b)
#            print component
            Alert=Alert+component+"\n"
       
        c="These stations are below the set alert threshold of:"+str(limits['rh'])+'%'
        Alert=Alert+c
    else:
        print "No Alerts"
        Alert="NULL"
    return Alert

A=createAlert()
print A
#send.sendEmailAlert(createAlert(),'fsweather1@usa.com')    
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    