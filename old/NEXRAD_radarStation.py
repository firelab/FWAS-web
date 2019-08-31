# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:11:18 2017

@author: tanner
"""

class radarStation:
    rType='reflectivity'
    radar_lat=0.0
    radar_lon=0.0
    gate_lat=0.0
    gate_lon=0.0
    gate_dist=0.0
    gate_bearing=0.0
    gate_cardinal=''
    gate_val=0.0
    gate_thresh=0.0
    date=''
    time=''
    utc_offset=''
    is_empty=True
    check=False
    

def viewStation(r):
    print 'RADAR STATION INFO'
    print 'type: ',r.rType
    print 'lat: ',r.radar_lat
    print 'lon: ',r.radar_lon
    print 'GATE INFO'
    print 'lat: ',r.gate_lat
    print 'lon: ',r.gate_lon
    print 'dist: ',r.gate_dist
    print 'gate_bearing: ',r.gate_bearing
    print 'direction: ',r.gate_cardinal
    print 'gate_val: ',r.gate_val
    print 'threshold: ',r.gate_thresh
    print 'Date,Time: ',r.date,r.time
    print r.is_empty,r.check