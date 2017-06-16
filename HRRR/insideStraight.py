# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 13:14:07 2017

@author: tanner
"""

import gdal
from osgeo import osr
import ogr
import matplotlib.pyplot as pyplot
from mpl_toolkits.basemap import Basemap
import numpy
import math
import netCDF4

gdal.UseExceptions()


#ds=gdal.Open('/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2') #Will Change!
#dataset=ds

ffP='/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2'

variables=['reflectivity','temperature','RH','uWind','vWind','Wind']
forecastFile=['']
rasterBands=[]
rasterArrays=[]
cDS=[gdal.Dataset]
coords=[0,0]
covfefe=[0,0]
gRad=[20]
"These Will be Replaced by limits"
#refMax=20.0 #DBZ 
#tmpMax=25.0 #C
#rhMax=25.0 #%
localLimits={'reflectivity':0.0,'temperature':0.0,'RH':0.0,'Wind':0.0}

limBool={'reflectivity':False,'temperature':False,'RH':False,'Wind':False}
exceedX={'reflectivity':0.0,'temperature':0.0,'RH':0.0,'Wind':0.0}
exceedY={'reflectivity':0.0,'temperature':0.0,'RH':0.0,'Wind':0.0}
exceedQuad={'reflectivity':'','temperature':'','RH':'','Wind':''}

#raster_wkt = ds.GetProjection()
#spatial_ref = osr.SpatialReference()
#spatial_ref.ImportFromWkt(raster_wkt)
#print spatial_ref.ExportToPrettyWkt()
def setRadius(radius):
    gRad[0]=radius
def setLimits(reflec,temp,rh,Wind):
    localLimits['reflectivity']=float(reflec)
    localLimits['temperature']=float(temp)
    localLimits['RH']=float(rh)
    localLimits['Wind']=float(Wind)

def setForecastFile(filePath):
    forecastFile[0]=filePath
    
def readForecastFile():
    ds=gdal.Open(forecastFile[0])
    cDS[0]=ds
#    return dataset
    
def getRasterBands(dataset):
#    numBands=5 #May Change?!
    for i in range(1,7):
        band=dataset.GetRasterBand(i)
        bandArray=band.ReadAsArray()
        rasterBands.append(band)
        rasterArrays.append(bandArray)
    
def setLatLon(lat,lon):
    coords[0]=lat
    coords[1]=lon

def convertLatLonToProj():
    z=0
    raster_wkt= cDS[0].GetProjection()
    spatial_ref=osr.SpatialReference()
    spatial_ref.ImportFromWkt(raster_wkt)
    
    oldCS=osr.SpatialReference()    
    newCS=osr.SpatialReference()
    
    oldCS.ImportFromEPSG(4326)
    newCS.ImportFromWkt(spatial_ref.ExportToWkt())
    
    transform=osr.CoordinateTransformation(oldCS,newCS)
    
    x,y,z=transform.TransformPoint(coords[1],coords[0])
    gt=cDS[0].GetGeoTransform()
    px=int((x-gt[0])/gt[1])
    py=int((y-gt[3])/gt[5])
    covfefe[0]=px
    covfefe[1]=py
#    return [px,py]
    
def plotRaster(bandArray):
    pyplot.imshow(bandArray)

def getBoxValues(boxRad,rasterBand):
#    boxRad=20
    centerX=covfefe[0]
    centerY=covfefe[1]
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
    LL=[leftSide,bottomSide]
    UL=[leftSide,topSide]
    LR=[rightSide,bottomSide]
    UR=[rightSide,topSide]
    boxSet=rasterBand.ReadAsArray(UL[0],UL[1],boxRad*2,boxRad*2)
    return boxSet

def checkThresholds(variable):
    datList=[]
    if variable=='reflectivity':
        refVal=getBoxValues(gRad[0],rasterBands[0])
        exceed=numpy.where(refVal>localLimits[variable])
        if exceed[0].size==0:
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(refVal[exceed[0][i]][exceed[1][i]])
            exceedX[variable]=numpy.average(exceed[0])
            exceedY[variable]=numpy.average(exceed[1])
            limBool[variable]=True
            return datList
    if variable=='temperature':
        tmpVal=getBoxValues(gRad[0],rasterBands[1])
        exceed=numpy.where(tmpVal>localLimits[variable])
        if exceed[0].size==0:
#            return [False,False]
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(tmpVal[exceed[0][i]][exceed[1][i]])
            exceedX[variable]=numpy.average(exceed[0])
            exceedY[variable]=numpy.average(exceed[1])
            limBool[variable]=True
            return datList
#            return [tmpVal,exceed]
    if variable=='RH':
        rhVal=getBoxValues(gRad[0],rasterBands[2])
        exceed=numpy.where(rhVal<localLimits[variable])
        if exceed[0].size==0:
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(rhVal[exceed[0][i]][exceed[1][i]])
            exceedX[variable]=numpy.average(exceed[0])
            exceedY[variable]=numpy.average(exceed[1])
            limBool[variable]=True
            return datList
#            return [False,False]
#        else:
#            return [rhVal,exceed]
    if variable=='Wind':
        windVal=getBoxValues(gRad[0],rasterBands[5])
        exceed=numpy.where(windVal>localLimits['Wind'])
        if exceed[0].size==0:
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(windVal[exceed[0][i]][exceed[1][i]])
            exceedX[variable]=numpy.average(exceed[0])
            exceedY[variable]=numpy.average(exceed[1])
            limBool[variable]=True
            return datList
#            return [False,False]
#        else:
#            return [windVal,exceed]
    
    
#def newCheckThresholds(variable):
#    datList=[]    
#    genVar=''
#    genInt=0
#    if variable=='reflectivity':
#        genVar=variable
#        genInt=0
#    if variable=='temperature':
#        genVar=variable
#        genInt=1
#    if variable=='RH':
#        genVar=variable
#        genInt=2
#    if variable=='Wind':
#        genVar=variable
#        genInt=5
#    datVal=getBoxValues(gRad[0],rasterBands[genInt])
#    exceed=numpy.where(datVal)
        

    
   
    

    
def calcAverage(data):
    avg=numpy.average(data)
    return avg

def calcStDev(data):
    stDev=numpy.std(data)
    return stDev
def calcQuadrant(variable):
    X=exceedX[variable]
    Y=exceedY[variable]
    oX=gRad[0]
    oY=gRad[0]
    if X>oX:
        LR='E'
    if X<oX:
        LR='W'
    if Y>oY:
        UD='S'
    if Y<oY:
        UD='N'
    quad=UD+LR
    return quad
    

def calcPercentCovered(data):
    tVal=getBoxValues(gRad[0],rasterBands[0])
    totalArea=tVal.size
    affectedArea=len(data)
    pctAffected=float(affectedArea)/float(totalArea)
    return pctAffected
    
setLimits(20,20,57,5)    
    

setForecastFile(ffP)
readForecastFile()
getRasterBands(cDS[0])

lat=46.926183
lon=-114.092779

setLatLon(lat,lon)
setRadius(20)
convertLatLonToProj()

rawDat=[]
avDat=[]
stDat=[]

for i in range(len(localLimits)):
    sk=checkThresholds(localLimits.keys()[i])
    rawDat.append(sk)
    sk2=calcAverage(rawDat[i])
    avDat.append(sk2)
    sk3=calcStDev(rawDat[i])
    stDat.append(sk3)
    print calcPercentCovered(rawDat[i])

#for i in range(len(localLimits)):
    

a=localLimits.keys()
#print a
#print ska



rhVal=getBoxValues(gRad[0],rasterBands[2])
exceed=numpy.where(rhVal<localLimits['RH'])
#for i in range(len(exceed[0])):
##    print rhVal[exceed[0][i]][exceed[1][i]]
#    ska.append(rhVal[exceed[0][i]][exceed[1][i]])
#    
    
    
        
    