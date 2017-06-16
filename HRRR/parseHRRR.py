# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:32:55 2017

@author: tanner
"""

import gdal
from osgeo import osr
import osgeo
import matplotlib.pyplot as pyplot
#from mpl_toolkits.basemap import Basemap
import numpy
import math
import HR
import sys
import glob
#import netCDF4

gdal.UseExceptions()

forecastFile=['']
#rasterBands=list()
#rasterArrays=list()
#cDS=[gdal.Dataset]

def setRadius(wxInfo,radius):
    wxInfo.radius=float(radius)

def setLatLon(wxInfo,lat,lon):
    wxInfo.lat=lat
    wxInfo.lon=lon

def setLimits(wxData,reflec,temp,rh,Wind):
    wxData[0].limit=reflec
    wxData[1].limit=temp
    wxData[2].limit=rh
    wxData[5].limit=Wind
    
def setForecastFile(filePath):
    forecastFile[0]=filePath
    
def getDiskFiles():
    dZ=glob.glob('/media/tanner/vol2/HRRR/grib/*.grib2')
    dZ.sort()
    return dZ
    
#def assignForecast(futureTime):
#    cZ=getDiskFiles()
#    cZ.sort()
#    fFile=cZ[futureTime]
#    setForecastFile(fFile)    
#    
#def readForecastFile():
#    ds=gdal.Open(forecastFile[0])
#    cDS[0]=ds      
    
def getDataset(futureTime):
    cZ=glob.glob('/media/tanner/vol2/HRRR/grib/*.grib2')
    cZ.sort()
    fFile=cZ[futureTime]
#    print fFile
    ds=gdal.Open(fFile)
    return ds
        
    
def getRasterBands(dataset):
    rasterBands=[]
    rasterArrays=[]
    for i in range(1,7):  
        band=dataset.GetRasterBand(i)
        bandArray=band.ReadAsArray()
        rasterBands.append(band)
        rasterArrays.append(bandArray)
    return [rasterBands,rasterArrays]

def convertLatLonToProj(wxInfo,dataset):
    z=0
    raster_wkt= dataset.GetProjection()
    spatial_ref=osr.SpatialReference()
    spatial_ref.ImportFromWkt(raster_wkt)
    
    oldCS=osr.SpatialReference()    
    newCS=osr.SpatialReference()
    
    oldCS.ImportFromEPSG(4326)
    newCS.ImportFromWkt(spatial_ref.ExportToWkt())
    
    transform=osr.CoordinateTransformation(oldCS,newCS)
    
#    x,y,z=transform.TransformPoint(coords[1],coords[0])
    x,y,z=transform.TransformPoint(wxInfo.lon,wxInfo.lat)
    gt=dataset.GetGeoTransform()
    px=int((x-gt[0])/gt[1])
    py=int((y-gt[3])/gt[5])
    wxInfo.covfefe[0]=px
    wxInfo.covfefe[1]=py
#    covfefe[0]=px
#    covfefe[1]=py

def plotRaster(bandArray):
    pyplot.imshow(bandArray)

def calcAverage(data):
    avg=numpy.average(data)
    return avg

def calcStDev(data):
    stDev=numpy.std(data)
    return stDev

def getBoxValues(wxInfo,rasterBand):
    boxRad=int(wxInfo.radius)
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]
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

def plotRasterBox(wxInfo,rasterBand):
    boxRad=int(wxInfo.radius)
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
#    LL=[leftSide,bottomSide]
    UL=[leftSide,topSide]
#    LR=[rightSide,bottomSide]
#    UR=[rightSide,topSide]
    pyplot.imshow(rasterBand.ReadAsArray(UL[0],UL[1],boxRad*2,boxRad*2))
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()

def calcQuadrant(wxInfo,wxData,n):
    X=wxData[n].exceedX
    Y=wxData[n].exceedY
    oX=wxInfo.radius
    oY=wxInfo.radius
    radBuff=float(wxInfo.radius)/(4.0)
    UD=''
    LR=''
    if X>(oX+radBuff):
        LR='E'
    if X<(oX-radBuff):
        LR='W'
    if Y>(oY+radBuff):
        UD='S'
    if Y<(oY-radBuff):
        UD='N'
    quad=UD+LR
    return quad

def calcPercentCovered(wxInfo,data,rasterBand):
    tVal=getBoxValues(wxInfo,rasterBand)
    totalArea=tVal.size
    affectedArea=len(data)
    pctAffected=float(affectedArea)/float(totalArea)
    return pctAffected
    
def thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands):        
    datList=[]
    datVal=getBoxValues(wxInfo,rasterBands[genInt])
    exceed=numpy.where(datVal>wxData[genInt].limit)
    if exceed[0].size==0:
        wxData[genInt].check=True
        datList.append(False)
        return datList
    else:
        for i in range(len(exceed[0])):
            datList.append(datVal[exceed[0][i]][exceed[1][i]])
        wxData[genInt].raw=datList
        wxData[genInt].exceedX=numpy.average(exceed[0])
        wxData[genInt].exceedY=numpy.average(exceed[1])
        wxData[genInt].limBool=True
        wxData[genInt].check=True
        wxData[genInt].average=calcAverage(datList)
        wxData[genInt].stDev=calcStDev(datList)
        wxData[genInt].exceedQuad=calcQuadrant(wxInfo,wxData,genInt)
        wxData[genInt].pctCovered=calcPercentCovered(wxInfo,datList,rasterBands[genInt])    
    
def checkThresholds(wxInfo,wxData,variable,rasterBands):
    datList=[]
    if variable=='reflectivity':
        genVar=variable
        genInt=0
        thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands)
    if variable=='temperature':
        genVar=variable
        genInt=1
        thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands)
    if variable=='Wind':
        genVar=variable
        genInt=5
        thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands)
    if variable=='RH':
        datVal=getBoxValues(wxInfo,rasterBands[2])
        exceed=numpy.where(datVal<wxData[2].limit)
        if exceed[0].size==0:
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(datVal[exceed[0][i]][exceed[1][i]])
            wxData[2].raw=datList
            wxData[2].exceedX=numpy.average(exceed[0])
            wxData[2].exceedY=numpy.average(exceed[1])
            wxData[2].limBool=True
            wxData[2].average=calcAverage(datList)
            wxData[2].stDev=calcStDev(datList)
            wxData[2].exceedQuad=calcQuadrant(wxInfo,wxData,2)
            wxData[2].pctCovered=calcPercentCovered(wxInfo,datList,rasterBands[2])
            wxData[2].check=True
#    if variable=='reflectivity' or 'temperature' or 'Wind' or 'RH':

#        
def locationSanityCheck(wxInfo,wxData,varNum,rasterBands,rasterArrays):
    """
    Good To Run if you get lost
    """
    boxRad=int(wxInfo.radius)
    a=varNum

    print wxData[varNum]
    print wxData[varNum].exceedX,wxData[varNum].exceedY
    print wxData[varNum].exceedQuad
    print wxData[varNum].pctCovered
    
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]    
    
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
    UL=[leftSide,topSide]
    
    pyplot.figure(1)
    bA=osgeo.gdal_array.BandReadAsArray(rasterBands[a],UL[0],UL[1],boxRad*2,boxRad*2)
    pyplot.imshow(bA,vmin=rasterArrays[a].min(),vmax=rasterArrays[a].max())
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()
    pyplot.show()
    
    pyplot.figure(2)
    pyplot.imshow(rasterArrays[a])
    pyplot.plot(477,177,'mo',markersize=6)
    pyplot.axis([rightSide,leftSide,bottomSide,topSide])
    #pyplot.xlim(0,1799)
    #pyplot.ylim(0,1059)
    #pyplot.gca().invert_yaxis()
    pyplot.gca().invert_xaxis()
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()
    pyplot.show()        

    pyplot.figure(3)
    pyplot.imshow(rasterArrays[a])
    pyplot.plot(wxInfo.covfefe[0],wxInfo.covfefe[1],'mo',markersize=6)
    #pyplot.axis([rightSide,leftSide,bottomSide,topSide])
    pyplot.xlim(0,1799)
    pyplot.ylim(0,1059)
    pyplot.gca().invert_yaxis()
    #pyplot.gca().invert_xaxis()
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.show()        
       
    
def setControls(fCastNum,radius,Lat,Lon,limReflec,limTemp,limRH,limWind,runSanityCheck):
    wxInfo=HR.wxStruct()
    wxData=[HR.reflectivity(),HR.temperature(),HR.RH(),HR.Empty(),HR.Empty(),HR.Wind()]
    
#    assignForecast(fCastNum)
#    readForecastFile()
    ds=getDataset(fCastNum)
    rasterBands,rasterArrays=getRasterBands(ds)

    setRadius(wxInfo,radius)
    setLatLon(wxInfo,Lat,Lon)
    convertLatLonToProj(wxInfo,ds)
    setLimits(wxData,limReflec,limTemp,limRH,limWind)
    
    for i in range(len(wxData)):
        checkThresholds(wxInfo,wxData,wxInfo.dataForms[i],rasterBands)     
        if runSanityCheck==True:
            locationSanityCheck(wxInfo,wxData,i,rasterBands,rasterArrays)
#    aList.append(wxData)
#    return aList
#    print wxData[1].average
    return wxData





#def runLoop(numTimes,radius,Lat,Lon,limReflec,limTemp,limRH,limWind,runSanityCheck):
#    aList=[]
#    for i in range(numTimes):
#        wxx=setControls(fCastNum,radius,Lat,Lon,limReflec,limTemp,limRH,limWind,runSanityCheck)
#        aList.append(wxx)
#    return aList


    
fCastNum=5
fCastRadius=20
fCastLat=46.926183
fCastLon=-114.092779
fReflec=20
fTemp=20
fRH=57
fWind=5
a=setControls(fCastNum,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)

#for i in range(6):
##    print a[1].limBool
##    print a[1].pctCovered
#    b.append(a)
#    print b[i][1].average

#q=setControls(0,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)


#b=setControls(12,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)


#print a[1].average==b[1].average
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    