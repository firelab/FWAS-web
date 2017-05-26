# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:05:53 2017

@author: tanner
"""

from geopy.distance import great_circle
import math
import numpy


def getBearing(lat1,lon1,lat2,lon2):
    """
    Calculates where the station is in proximity to your Location
    """
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
    
def listSMSGateways():
    """
    provides a list of all SMS Gateways
    """
    gate={'att':'txt.att.net','verizon':'vtext.com','tmobile':'tmomail.net','virgin':'vmobl.com','sprint':'messaging.sprintpcs.com'}
    return gate

def getSMSGateway(carrier,gateways):
    """
    converts input from shiny to SMS Gateway
    """
    gateway=gateways[str(carrier)]
    return gateway

def degToCompass(num):
    """
    converts Degrees to cardinal Directions
    """
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
#    print arr[(val % 16)]
    return arr[(val % 16)]

def getSpatial(location,Station):
    """
    Gets the distance from you to the station and its direction
    """
    lat1=location[0]
    lon1=location[1]
    lat2=Station.lat
    lon2=Station.lon
    distance=great_circle([lat1,lon1],[lat2,lon2]).miles #Miles is harded coded for the moment
    bearing=getBearing(lat1,lon1,lat2,lon2)
    cardinal=degToCompass(bearing)
    return [distance,bearing,cardinal]    

def getStationDirections(location,listStations):
    """
    unifying function that puts everything above toghther
    """
    relLocation=[]
    for i in range(len(listStations)):
        ind=getSpatial(location,listStations[i])
        listStations[i].distance_from_point=ind[0]
        listStations[i].bearing=ind[1]
        listStations[i].cardinal=ind[2]
        relLocation.append(ind)
    return relLocation

def getThresholdUnits(key,units):
    unit=""
    if key=='wind_speed' or key=='wind_gust':
        unit=units['spdABV']
    if key=='temperature':
        unit=units['tempABV']
    if key=='relative_humidity':
        unit='%'
    return str(unit)

def headerThresh(thresholds,units):
    thStr=""
    for i in range(len(thresholds)):
        if thresholds[thresholds.keys()[i]]!='NaN':
            thStr=thStr+thresholds.keys()[i]+\
            ": "+thresholds[thresholds.keys()[i]]+\
            " "+getThresholdUnits(thresholds.keys()[i],units)+". "
#            print thStr
    headerB="Set thresholds are:\n"+thStr+"\n"
    return headerB
    
def createHeader(thresholds,units,listStations):
    """
    creates the Header for the Alert
    """
    stids=""
#    thStr=""
    for i in range(len(listStations)):
        stids=stids+str(listStations[i].stid)+" "   
#    for i in range(len(thresholds)):
#        thStr=thStr+thresholds.keys()[i]+": "+thresholds[thresholds.keys()[i]]+" "

    title="Fire Weather Alert:\n\n"    
    headerA="The Following Stations have exceeded set thresholds: "+stids+".\n"
    headerB=headerThresh(thresholds,units)
#    headerB="Set thresholds are:\n"+thStr+"\n"
#    headerC="wind_speed ("+str(units['spdABV'])+"), relative_humidity (%), temperature ("+str(units['tempABV'])+")\n\n"
    return title+headerA+headerB+"\n"
#    print title+headerA+headerB+headerC
def createLine(wxStation,Units):
    """
    creates a single station Alert that is then combined with the header
    """
    rhList=[]
    spdList=[]
    gustList=[]
    dirList=[]
    tList=[]
    obsList=[]
    obsDict={}
    if numpy.isfinite(wxStation.rh)==True:
        rhList.append('relative_humidity of:')
        rhList.append(str(wxStation.rh))
        rhList.append(str(wxStation.rh_units))
    if numpy.isfinite(wxStation.wind_speed)==True:
        spdList.append('wind_speed of:')
        spdList.append(str(wxStation.wind_speed))
        spdList.append(str(wxStation.wind_speed_units))
        if numpy.isfinite(wxStation.wind_gust):
            gustList.append(' gust of:')
            gustList.append(str(wxStation.wind_gust))
            gustList.append(str(wxStation.wind_speed_units))
#        dirList.append('wind_direction')
        dirList.append(str(wxStation.wind_direction))
    if numpy.isfinite(wxStation.temperature)==True:
        tList.append('temperature of:')
        tList.append(str(wxStation.temperature))
        tList.append(str(wxStation.temperature_units))
        
    rhStr=' '.join(rhList)+";"
    spdStr=' '.join(spdList)+' '.join(gustList)+" at "+' '.join(dirList)+' degrees;'
    tStr=' '.join(tList)+"."
    if rhStr==';':
        rhStr=' '
    if spdStr==' at  degrees;':
        spdStr=' '
    if tStr==';':
        tStr=' '
    
#   l3="Recorded at: "+s1.date+"_"+s1.time+" UTC "+s1.utc_offset
    dateStr=" Observations Recorded at: "+wxStation.date+"_"+wxStation.time+" UTC"+wxStation.utc_offset
    
    line="Station "+str(wxStation.stid)+", "+str(round(wxStation.distance_from_point,1))+" miles at "+str(round(wxStation.bearing,1))+" degrees "
    line2=str(wxStation.cardinal)+" from your location has a "+rhStr+" "+spdStr+" "+tStr+dateStr+"\n\n"
    return line+line2    
    
def makeSystemAlert(thresholds,units,wxStations):
    """
    Makes the Alert
    """
    fullAlert=[]
    
    header=createHeader(thresholds,units,wxStations)
    stationLines=[]
    for i in range(len(wxStations)):
        stationLine=createLine(wxStations[i],units)
        stationLines.append(stationLine)
    fullAlert=header+''.join(stationLines) #Possibly reverse these/swtich them around
    return fullAlert
    
    
    
    
    
    
    
    
    
    