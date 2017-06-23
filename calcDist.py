# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 09:19:59 2017

@author: tanner
"""

from geopy.distance import great_circle
import math
import numpy

def getBearing(lat1,lon1,lat2,lon2):
    """
    Generic Bearing Calculator
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

def degToCompass(num):
    """
    converts Degrees to cardinal Directions
    """
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
#    print arr[(val % 16)]
    return arr[(val % 16)]

def getSpatial(location,remote):
    """
    Gets the distance from you to the station and its direction
    """
    lat1=location[0]
    lon1=location[1]
    lat2=remote[0]
    lon2=remote[1]
    distance=great_circle([lat1,lon1],[lat2,lon2]).miles #Miles is harded coded for the moment
    bearing=getBearing(lat1,lon1,lat2,lon2)
    cardinal=degToCompass(bearing)
    return [distance,bearing,cardinal]    
    
    
def kiloSpatial(location,remote):
    """
    Gets the distance from you to the station and its direction IN KILOMETERS!
    """
    lat1=location[0]
    lon1=location[1]
    lat2=remote[0]
    lon2=remote[1]
    distance=great_circle([lat1,lon1],[lat2,lon2]).kilometers #Miles is harded coded for the moment
    bearing=getBearing(lat1,lon1,lat2,lon2)
    cardinal=degToCompass(bearing)
    return [distance,bearing,cardinal]    