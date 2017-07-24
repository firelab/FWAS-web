# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:16:10 2017

@author: tanner

Class for HRRR Data storage (its essentially a structure)
"""

import gdal
import numpy

class reflectivity:
    """
    HRRR reflectivity Structure, stores stuff like limits, units and location of closest pixel
    """
    limit=0.0
    limBool=False
    check=False
    raw=[]
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='dBZ' #Default, Don't Change this one
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
    eDist=0.0
    eBearing=0.0
    fBear=''    
    eVal=0.0
    obs_max=0.0
    time_max=0.0
    
class temperature:
    """
    HRRR temperature Structure, stores stuff like limits units and average value
    """
    limit=0.0
    limBool=False
    check=False
    raw=[] #Stays in degC!
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='C' #Default, can also be F
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
    eDist=0.0
    eBearing=0.0 
    fBear=''    
    eVal=0.0
    obs_max=0.0
    time_max=0.0


class RH:
    """
    HRRR relative humitidy structure, stores useful stuff
    """
    limit=0.0
    limBool=False
    check=False
    raw=[]
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='%' #Default, Don't Change this one
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
    eDist=0.0
    eBearing=0.0
    fBear=''    
    eVal=0.0
    obs_min=0.0
    time_min=0.0

class Wind:
    """
    HRRR wind structure
    """
    limit=0.0
    limBool=False
    check=False 
    raw=[] #Stays in MPS!
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='mps' #Default, can also be mph
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
    eDist=0.0
    eBearing=0.0 
    fBear=''   
    eVal=0.0
    obs_max=0.0
    time_max=0.0


class Ltng:
    """
    HRRR lightning structure
    """
    limit=1.0 #Hard Coded Limit on Lightning
    limBool=False
    check=False
    raw=[]
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='flashes/km^2/5min'
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
    eDist=0.0
    eBearing=0.0
    fBear=''    
    eVal=0.0
    obs_max=0.0
    time_max=0.0

class Precip:
    """
    HRRR Precipitation structure
    """
    limit=0.001 #
    limBool=False
    check=False
    raw=[]
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='kg/m^2/s'
    eDist=0.0
    eBearing=0.0
    fBear=''
    eVal=0.0
    obs_max=0.0
    time_max=0.0

class Empty:
    """
    In case there is a variable that we don't want yet, but exists in dataeset 
    """
    limit=0.0
    limBool=False
    check=False
    raw=[]
    average=0.0
    stDev=0.0
    exceedX=0.0
    exceedY=0.0
    exceedQuad=''
    pctCovered=0.0
    units='NONE'
    eDist=0.0
    eBearing=0.0 
    fBear=''   
    eVal=0.0
    obs_max=0.0
    time_max=0.0

class wxStruct:
    """
    stores metadata for HRRR Run
    """
    lat=0.0
    lon=0.0
    covfefe=[0.0,0.0]
    radius=int(0)
    dataForms=['reflectivity','temperature','RH','Ltng','Precip','Wind']
    variables=['reflectivity','temperature','RH','Wind']
#    wxData=[reflectivity,temperature,RH,Wind]    
    
    
