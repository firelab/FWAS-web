# -*- coding: utf-8 -*-
"""
Created on Fri May 12 09:18:10 2017

@author: tanner
"""
class Station:
    """
    Object that stores all the good weather stuff from a station
    """
    stid=''
    lat=0.0
    lon=0.0
    distance_from_point=0.0
    bearing=0
    cardinal=''
    rh=0.0
    rh_units=''
    wind_speed=0.0
    wind_gust=0.0
    wind_speed_units=''
    wind_direction=0.0
    temperature=0.0
    temperature_units=''
    date=''
    time=''
    utc_offset=''
    is_empty=True

def printStation(station):
    """
    for debugging: prints station info to the screen
    """
    print "STID: ", station.stid
    print "LAT: ", station.lat
    print "LON: ", station.lon
    print "DFP: ", station.distance_from_point
    print "BRNG: ", station.bearing
    print "CARD: ", station.cardinal
    print "RH: ", station.rh," ",station.rh_units
    print "WNDSPD: ", station.wind_speed," ",station.wind_speed_units
    print "WNDDIR: ", station.wind_direction
    print "TMP: ", station.temperature," ",station.temperature_units
    print "DATE: ", station.date
    print "TIME: ", station.time