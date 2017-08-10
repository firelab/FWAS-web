# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 11:32:55 2017

@author: tanner

PARSES HRRR DATA
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
from createAlert import degToCompass
import calcDist
#import netCDF4

gdal.UseExceptions()

forecastFile=['']
#rasterBands=list()
#rasterArrays=list()
#cDS=[gdal.Dataset]

def setRadius(wxInfo,radius):
    """
    Sets the radius for HRRR checking
    """
    wxInfo.radius=float(radius)

def setLatLon(wxInfo,lat,lon):
    """
    Sets Latitude and Longitude in wxStruct
    """
    wxInfo.lat=lat
    wxInfo.lon=lon

def setLimits(wxData,reflec,temp,rh,Wind):
    """
    Sets limits on HRRR Data
    """
    wxData[0].limit=reflec
    wxData[1].limit=temp
    wxData[2].limit=rh
    wxData[5].limit=Wind
    
def setForecastFile(filePath):
    """
    Sets Forecast Path DEPRECATED
    """
    forecastFile[0]=filePath
    
def getDiskFiles():
    """
    Fetches Grib Files on Disk
    """
#    dZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
    dZ=glob.glob('/home/ubuntu/fwas_data/HRRR/grib/*.grib2')
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
    """
    opens grib file
    """
#    cZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
    cZ=glob.glob('/home/ubuntu/fwas_data/HRRR/grib/*.grib2')
    cZ.sort()
    fFile=cZ[futureTime]
#    print fFile
    ds=gdal.Open(fFile)
    return ds
        
    
def getRasterBands(dataset):
    """
    Converts grib dataset into raster bands and arrays and sorts them into a sensible format
    """
    rasterBands=[]
    rasterArrays=[]
    rasterBaster=[]
    rasterAaster=[]
    for i in range(1,8):  
        band=dataset.GetRasterBand(i)
        bandArray=band.ReadAsArray()
        rasterBaster.append(band)
        rasterAaster.append(bandArray)
        
    rasterBands.append(rasterBaster[0])
    rasterBands.append(rasterBaster[3])
    rasterBands.append(rasterBaster[4])
    rasterBands.append(rasterBaster[1])
    rasterBands.append(rasterBaster[6])
    rasterBands.append(rasterBaster[5])

    rasterArrays.append(rasterAaster[0])
    rasterArrays.append(rasterAaster[3])
    rasterArrays.append(rasterAaster[4])
    rasterArrays.append(rasterAaster[1])
    rasterArrays.append(rasterAaster[6])
    rasterArrays.append(rasterAaster[5])   
        
    return [rasterBands,rasterArrays]

def convertLatLonToProj(wxInfo,dataset):
    """
    Does what it says, takes lat lon and turns it into pixels to be used
    """
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

def projToLatLon(pxList):
    """
    Goes Backwards (pixels to lat lon)
    """
    
    dataset=getDataset(0)
    
    raster_wkt=dataset.GetProjection()
    spatial_ref=osr.SpatialReference()
    spatial_ref.ImportFromWkt(raster_wkt)
    
    oldCS=osr.SpatialReference()    
    newCS=osr.SpatialReference()
    
    oldCS.ImportFromEPSG(4326)
    newCS.ImportFromWkt(spatial_ref.ExportToWkt())
    
    back=osr.CoordinateTransformation(newCS,oldCS)
    gt=dataset.GetGeoTransform()

    x=pxList[0]*gt[1]+gt[0]
    y=pxList[1]*gt[5]+gt[3]
    
    lon,lat,z=back.TransformPoint(x,y)   
    
    return [lat,lon]    
    

def plotRaster(bandArray):
    """
    Simple Plotting of raster Band
    """
    pyplot.imshow(bandArray)

def calcAverage(data):
    """
    Calculates an arithmetic mean
    """
    avg=numpy.average(data)
    return avg

def calcStDev(data):
    """
    Calculates the population StDev
    """
    stDev=numpy.std(data)
    return stDev

def getBoxValues(wxInfo,rasterBand):
    """
    Converts coords and radius into box and zooms band into box
    """
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
    """
    Plotting for Debugging, plots box
    """
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
    """
    Calculates where the hgihest pixels are
    """
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
    """
    How much of the domain is covered by exceeding pixels
    """
    tVal=getBoxValues(wxInfo,rasterBand)
    totalArea=tVal.size
    affectedArea=len(data)
    pctAffected=float(affectedArea)/float(totalArea)
    return pctAffected

def getClosestPixel(wxInfo,exceed,datVal):
    """"
    gets closest Pixel to your location that exceeds thresholds
    """
    potential=numpy.array([exceed[0],exceed[1]])
    centerPoint=numpy.array([wxInfo.radius,wxInfo.radius])
    arrPix=[]
    for i in range(len(potential[0])):
        pixel=numpy.array([centerPoint[0]-potential[0][i],centerPoint[1]-potential[1][i]])
        arrPix.append(numpy.linalg.norm(pixel))
    arrPix=numpy.array(arrPix)
    minDist=arrPix.min()
    minLoc=arrPix.argmin()    
    
    x=centerPoint[0]-potential[0][minLoc]
    y=centerPoint[0]-potential[1][minLoc]
    
    xGlobal=wxInfo.covfefe[0]-x 
    yGlobal=wxInfo.covfefe[1]-y

    laX,loY=projToLatLon([xGlobal,yGlobal])    
#    print 'locLat,locLon: ',wxInfo.lat,wxInfo.lon
#    print 'Global Coords: ', wxInfo.covfefe[0],wxInfo.covfefe[1]
#    print 'Local Coords: ',centerPoint[0],centerPoint[0]
#    print 'threshPoints: ', potential[0][minLoc],potential[1][minLoc] 
#    print 'diff: ',x,y
#    print 'Global+diff: ',wxInfo.covfefe[0]-x,wxInfo.covfefe[1]-y
#    print 'Lat,Lon: ',laX,loY
    
    spatialInfo=calcDist.getSpatial([wxInfo.lat,wxInfo.lon],[laX,loY])    
        
    angle=math.degrees(math.atan2(y,x))
    angle-=90 #Corrects for messsed up projection system        
    if angle<90:
        angle+=360#print 'value: ',datVal[exceed[0][aa],exceed[1][aa]]
    
    cVal=datVal[exceed[0][minLoc],[exceed[1][minLoc]]]
#    print angle,'\n\n'
#    print minDist,angle
#    print spatialInfo
#    return [minDist,angle,cVal]
    return[spatialInfo[0],spatialInfo[1],cVal]

def thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands):        
    """
    Checks thresholds of all the normal variables, excluding RH, returns lots of good Info
    """
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
        wxData[genInt].eDist,wxData[genInt].eBearing,wxData[genInt].eVal=getClosestPixel(wxInfo,exceed,datVal)
        wxData[genInt].fBear=degToCompass(wxData[genInt].eBearing)
        wxData[genInt].obs_max=max(datList)
        
def checkThresholds(wxInfo,wxData,variable,rasterBands):
    """
    Checks the thresholds of all variables, all the normal ones go to Thresholds II RH is checked here because its special
    """
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
    if variable=='Ltng':
        genVar=variable
        genInt=3
        thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands)
    if variable=='Precip':
        genVar=variable
        genInt=4
        thresholdsII(wxInfo,wxData,variable,genInt,genVar,rasterBands)
    if variable=='RH':
        datVal=getBoxValues(wxInfo,rasterBands[2])
        exceed=numpy.where(datVal<wxData[2].limit)
        
        if exceed[0].size==0 or not any(exceed[0]):
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
            wxData[2].eDist,wxData[2].eBearing,wxData[2].eVal=getClosestPixel(wxInfo,exceed,datVal)
            wxData[2].fBear=degToCompass(wxData[2].eBearing)
            wxData[2].obs_min=min(datList)

#            wxData[2].eVal=            
            
#print 'value: ',datVal[exceed[0][aa],exceed[1][aa]]

#    if variable=='reflectivity' or 'temperature' or 'Wind' or 'RH':

#        
def locationSanityCheck(wxInfo,wxData,varNum,rasterBands,rasterArrays):
    """
    Good To Run if you get lost. Plots the Local Area and CONUS along with your Lat Lon and other useful stuff
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
    pyplot.plot(20,20,'mo',markersize=6)
    pyplot.plot(15,25,'ro',markersize=6)
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()
    pyplot.xlim(0,40)
    pyplot.ylim(0,40)
    pyplot.gca().invert_yaxis()
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
    """
    Master HRRR checker Function, run for each Forecast Hour
    """
    wxInfo=HR.wxStruct()
    wxData=[HR.reflectivity(),HR.temperature(),HR.RH(),HR.Ltng(),HR.Precip(),HR.Wind()]
    
#    assignForecast(fCastNum)
#    readForecastFile()
#    ds=getDataset(fCastNum)
    ds=fCastNum
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
    
#fCastNum=0
#fCastRadius=20
##fCastLat=46.926183
##fCastLon=-114.092779
#fCastLat=38.38
#fCastLon=-78.34
#fReflec=20
#
#fTemp=20
#fRH=57
#fWind=5
##
#a=setControls(fCastNum,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)
#
#for i in range(len(a)):
#    print a[i].eDist,a[i].eBearing,a[i].fBear


#wxInfo=HR.wxStruct()
##
#ds=getDataset(fCastNum)
#rasterBands,rasterArrays=getRasterBands(ds)
#setLatLon(wxInfo,fCastLat,fCastLon)
#convertLatLonToProj(wxInfo,ds)
#setRadius(wxInfo,fCastRadius)
##
##
#wxData=[HR.reflectivity(),HR.temperature(),HR.RH(),HR.Ltng(),HR.Precip(),HR.Wind()]
#setLimits(wxData,fReflec,fTemp,fRH,fWind)
#
#
#genInt=2
#
#datList=[]
#datVal=getBoxValues(wxInfo,rasterBands[genInt])
#exceed=numpy.where(datVal>wxData[genInt].limit)
#
#
#tP=numpy.array([27,23])
#
#potential=numpy.array([exceed[0],exceed[1]])
#
#cV=numpy.array([fCastRadius,fCastRadius])
#
#ska=[]
#for i in range(len(potential[0])):
#    cP=numpy.array([cV[0]-potential[0][i],cV[1]-potential[1][i]])
#    
##    print potential[0][i],potential[1][i]
##    print numpy.linalg.norm(cP)
#    ska.append(numpy.linalg.norm(cP))
##print min(ska)
#ska=numpy.array(ska)
#print 'min distance ',ska.min()
#print 'min array value ',ska.argmin()
#aa=ska.argmin()
#print 'coords in box: ',exceed[0][aa],exceed[1][aa]
#print 'value: ',datVal[exceed[0][aa],exceed[1][aa]]
#print 'triangle: ',potential[0][aa]-cV[0],potential[1][aa]-cV[1]
#x=cV[0]-potential[0][aa]
#y=cV[0]-potential[1][aa]
#
#ff=math.degrees(math.atan2(y,x))
#ff=ff-90
#if ff<0:
#    ff+=360
##if ff<0:
##    ff=abs(ff)
#print 'Angle:',ff
#
#gJ,bJ=getClosestPixel(wxInfo,exceed)
#print gJ
#print bJ

#locationSanityCheck(wxInfo,wxData,2,rasterBands,rasterArrays)

#if exceed[0].size==0:
#    wxData[genInt].check=True
#    datList.append(False)
#    return datList
#else:
#    for i in range(len(exceed[0])):
#        datList.append(datVal[exceed[0][i]][exceed[1][i]])
#    wxData[genInt].raw=datList
#    wxData[genInt].exceedX=numpy.average(exceed[0])
#    wxData[genInt].exceedY=numpy.average(exceed[1])
#    wxData[genInt].limBool=True
#    wxData[genInt].check=True
#    wxData[genInt].average=calcAverage(datList)
#    wxData[genInt].stDev=calcStDev(datList)
#    wxData[genInt].exceedQuad=calcQuadrant(wxInfo,wxData,genInt)
#    wxData[genInt].pctCovered=calcPercentCovered(wxInfo,datList,rasterBands[genInt])    





    


#for i in range(6):
##    print a[1].limBool
##    print a[1].pctCovered
#    b.append(a)
#    print b[i][1].average

#q=setControls(0,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)


#b=setControls(12,fCastRadius,fCastLat,fCastLon,fReflec,fTemp,fRH,fWind,False)


#print a[1].average==b[1].average
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    