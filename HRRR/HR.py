# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:16:10 2017

@author: tanner
"""

import gdal
import numpy

class reflectivity:
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
class temperature:
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
    units='C' #Default, can also be F
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)
class RH:
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
class Wind:
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
    units='mph' #Default, can also be mps
    rasterBand=gdal.Band
    rasterArray=numpy.array(0)

class Empty:
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
    
class wxStruct:
    lat=0.0
    lon=0.0
    covfefe=[0.0,0.0]
    radius=int(0)
    dataForms=['reflectivity','temperature','RH','uWind','vWind','Wind']
    variables=['reflectivity','temperature','RH','Wind']
#    wxData=[reflectivity,temperature,RH,Wind]    
    
    
