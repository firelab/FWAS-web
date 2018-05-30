#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 11:29:39 2018

@author: tanner

Uses timezonefinder to detect time zone for a user
and returns the ID number for updating in the GUIs of
FWAS 
and
RAWS Locator
"""

import timezonefinder
import sys

tzID=[1,2,3,4,5,6,7]
tzName=['America/Los_Angeles','America/Denver','America/Phoenix','America/Chicago','America/New_York','Pacific/Honolulu','America/Anchorage']


def getTZ(lat,lon):
    tf=timezonefinder.TimezoneFinder()
    return tf.timezone_at(lng=lon,lat=lat)
    
def getZoneID(lat,lon):
    for i in range(len(tzName)):
        if tzName[i]==getTZ(lat,lon):
            return tzID[i]

def setID(lat,lon):
    non_qc_id=getZoneID(lat,lon)
    if non_qc_id==None:
	print "A"
        return 2
    else:
        return non_qc_id

arg_lat=float(sys.argv[1])
arg_lon=float(sys.argv[2])

print setID(arg_lat,arg_lon)
