# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:05:53 2017

@author: tanner


RAWS ALERT CREATOR, also combines HRRR & RAWS
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
    provides a list of all SMS Gateways (Acutally we are using MMS due to message sizes)
    """
#    gate={'att':'txt.att.net','verizon':'vtext.com','tmobile':'tmomail.net','virgin':'vmobl.com','sprint':'messaging.sprintpcs.com'}
    #Old SMS Gateways
    # gate={'att':'sms.att.net',
    # 'verizon':'vtext.com',
    # 'tmobile':'tmomail.net',
    # 'virgin':'vmobl.com',
    # 'sprint':'messaging.sprintpcs.com'}
    #MMS Gateways
    gate={'att':'mms.att.net',
    'verizon':'vzwpix.com',
    'tmobile':'tmomail.net',
    'virgin':'vmpix.com',
    'sprint':'pm.sprint.com',
    'boost':'myboostmobile.com',
    'uscellular':'mms.uscc.net',
    'metro':'mymetropcs.com',
    'cricket':'mms.cricketwireless.net',
    'projectfi':'msg.fi.google.com'}
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
    
#def longDegToCompass(num):
#    """
#    converts Degrees to long cardinal directions ie NORTH vs N
#    """
#    val=int((num/22.5)+.5)
#    arr=["North","North,Northeast","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
##    print arr[(val % 16)]
#    return arr[(val % 16)]

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
    """
    Units str from key
    """
    unit=""
    if key=='wind_speed' or key=='wind_gust':
        unit=units['spdABV']
    if key=='temperature':
        unit=units['tempABV']
    if key=='relative_humidity':
        unit='%'
    return str(unit)

def headerThresh(thresholds,units):
    """
    Creates threshold part of header (now Footer!)
    """
    thStr=""
    for i in range(len(thresholds)):
#        if thresholds[thresholds.keys()[i]]!='NaN':
        if numpy.isfinite(float(thresholds[thresholds.keys()[i]])):
            thStr=thStr+thresholds.keys()[i]+\
            ": "+thresholds[thresholds.keys()[i]]+\
            " "+getThresholdUnits(thresholds.keys()[i],units)+". "
#            print thStr
    headerB="Set thresholds are:\n"+thStr+"\n"
    return headerB

def createHeader(thresholds,units,listStations):
    """
    OLD! DONT USE creates the Header for the Alert
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
    OLD, DONT USE! creates a single station Alert that is then combined with the header
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
    OLD: DON'T USE! Makes the Alert
    """
    fullAlert=[]

    header=createHeader(thresholds,units,wxStations)
    stationLines=[]
    for i in range(len(wxStations)):
        stationLine=createLine(wxStations[i],units)
        stationLines.append(stationLine)
    fullAlert=header+''.join(stationLines) #Possibly reverse these/swtich them around
    return fullAlert

"""
Much of the above code is now deprecated!
"""
'Uncomment if you need a demo station'
#import station
#s1=station.Station()
#s1.stid='XYZ123'
#s1.lat=00.00
#s1.lon=00.00
#s1.distance_from_point=10
#s1.bearing=360.00
#s1.cardinal='N'
#s1.rh=50
#s1.rh_units='%'
#s1.wind_speed=3
#s1.wind_speed_units='mph'
#s1.wind_direciton=16.0
#s1.temperature=60
#s1.temperature_units='F'
#s1.date='2017-06-09'
#s1.time='13:28:00'
#s1.utc_offset='-6:00'

def createVarAlert(wxStation,var):
    """
    new Single Line Alert Maker for RAWS
    """
    vDat=[]
    wind_flag=[False]
    gustStr=''
    wind_card=''
    wind_dir=''
    if var=='rh':
        vDat.append('relative humidity')
        vDat.append(wxStation.rh)
        vDat.append(wxStation.rh_units)
    if var=='wind_speed':
        vDat.append('wind speed')
        vDat.append(wxStation.wind_speed)
        vDat.append(wxStation.wind_speed_units)
        if numpy.isnan(wxStation.wind_direction)==False:
            wind_card=degToCompass(wxStation.wind_direction)
            wind_dir=str(int(round(wxStation.wind_direction,0)))
        if numpy.isfinite(wxStation.wind_gust):
            gustStr=' G '+str(int(round(wxStation.wind_gust,0))) #Coarsen the Precision
        wind_flag[0]=True
    if var=='temperature':
        vDat.append('temperature')
        vDat.append(wxStation.temperature)
        vDat.append(wxStation.temperature_units)

#    if str(vDat[1])!=str(numpy.nan):
    if numpy.isfinite(vDat[1]) and wind_flag[0]==False:
        #"Station"+....
#        line=str(wxStation.name.upper())+", "+str(round(wxStation.distance_from_point,1))+" miles at "+str(round(wxStation.bearing,1))+\
#        " degrees "+str(wxStation.cardinal)+" from your location reported a "+str(vDat[0])+\
#        " of "+str(round(vDat[1],0))+gustStr+' '+str(vDat[2])+' at '+wxStation.time[:5]+" "+wxStation.date+" UTC"+wxStation.utc_offset+'\n'
        line=str(wxStation.name.upper())+", "+str(round(wxStation.distance_from_point,1))+" miles "+\
        ""+str(wxStation.cardinal)+" of your location reported a "+str(vDat[0])+\
        " of "+str(int(round(vDat[1],0)))+gustStr+' '+str(vDat[2])+' at '+wxStation.time[:5]+" "+wxStation.date+"\n"#+" UTC"+wxStation.utc_offset+'\n'  
        return line
    if numpy.isfinite(vDat[1]) and wind_flag[0]==True:
        line=str(wxStation.name.upper())+", "+str(round(wxStation.distance_from_point,1))+" miles "+\
        ""+str(wxStation.cardinal)+" of your location reported a "+str(vDat[0])+\
        " of "+str(int(round(vDat[1],0)))+gustStr+' '+str(vDat[2])+' at '+wind_dir+' degrees '+wind_card+' at '+wxStation.time[:5]+" "+wxStation.date+"\n"#+" UTC"+wxStation.utc_offset+'\n'       
        return line
    else:
        line=''
        return line

def createSysAlert(headerLib,thresholdsLib,unitLimits,wxStations,HRRR_Alerts,p_Alert,timeZone):
    """
    New System Alert Maker! combines RAWS AND HRRR
    """
    header='Fire Weather Alert:\n\nThe following thresholds have been reached. All observations were taken within a '+\
    str(headerLib['radius'])+' mile radius of your location, All times are: '+str(timeZone)+'.\n\n'
    footer=headerThresh(thresholdsLib,unitLimits)

    #Part [0] Refec, [1] Temeprature [2] RH,  [3,4] NONE [5] WindSpeed

    varList=['temperature','wind_speed','rh']
    wxList=[] #Dogshit Idea!

    wxTemp=[]
    wxSpd=[]
    wxRh=[]

    wxStations.sort()
#    for j in range(len(varList)):
    for i in range(len(wxStations)):
        wxTemp.append(createVarAlert(wxStations[i],varList[0]))
        wxSpd.append(createVarAlert(wxStations[i],varList[1]))
        wxRh.append(createVarAlert(wxStations[i],varList[2]))

#    return [wxTemp,wxSpd,wxRh]



    tSect=''
    wSpdSect=''
    rhSect=''
    refecSect=''
    ltngSect=''
    precipSect=''

    #Create Temperature Section
#    if any(wxList[0:4]) or HRRR_Alerts[1]: #<----This indexing method was such a bad Idea I can't believe I did this...
    if any(wxTemp) or HRRR_Alerts[1]:#Superior in every whey...
#        tSect='THE TEMPERATURE THRESHOLD HAS BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\n'
        tSect='TEMPERATURE THRESHOLD EXCEEDED:\n'
#        for x in wxList[0:4]:
        for x in wxTemp:
            tSect+=x
        tSect+=HRRR_Alerts[1]+'\n'

#    if any(wxList[4:8]) or HRRR_Alerts[5]:
    if any(wxSpd) or HRRR_Alerts[5]:
        wSpdSect='WIND SPEED THRESHOLD EXCEEDED:\n'
#        wSpdSect='THRESHOLDS FOR WIND SPEED HAVE BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\n'
        for x in wxSpd:
            wSpdSect+=x
        wSpdSect+=HRRR_Alerts[5]+'\n'

#    if any(wxList[8:12]) or HRRR_Alerts[2]:
    if any(wxRh) or HRRR_Alerts[2]:
        rhSect='RELATIVE HUMIDITY THRESHOLD EXCEEDED:\n'
#        rhSect='THRESHOLDS FOR RELATIVE HUMIDITY HAVE BEEN EXCEEDED FROM THE FOLLOWING SOURCES.\n'
        for x in wxRh:
            rhSect+=x
        rhSect+=HRRR_Alerts[2]+'\n'

    if HRRR_Alerts[0]:
        refecSect='THUNDERSTORM FORECAST:\n'+HRRR_Alerts[0]+'\n'

    if HRRR_Alerts[4] or p_Alert:
        precipSect='PRECIP ALERT:\n'+HRRR_Alerts[4]

    if HRRR_Alerts[3]:
        ltngSect='LIGHTNING ALERT:\n'+HRRR_Alerts[3]+'\n'

    wxAlert=header+tSect+wSpdSect+rhSect+refecSect+precipSect+p_Alert+'\n'+ltngSect+footer

    return wxAlert
