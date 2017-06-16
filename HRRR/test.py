# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 14:19:40 2017

@author: tanner
"""

import gdal
from osgeo import osr
import ogr
import osgeo
import matplotlib.pyplot as pyplot
from mpl_toolkits.basemap import Basemap
import numpy
import math
import netCDF4
from gdalconst import *
gdal.UseExceptions()


variables=['reflectivity','temperature','RH','uWind','vWind','Wind']
forecastFile=['']
rasterBands=[]
rasterArrays=[]
cDS=[gdal.Dataset]
coords=[0,0]
covfefe=[0,0]
gRad=[20]


def setRadius(radius):
    gRad[0]=radius

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

def plotRaster(bandArray):
    pyplot.imshow(bandArray)


setForecastFile(ffP)
readForecastFile()
getRasterBands(cDS[0])

lat=46.926183
lon=-114.092779

setLatLon(lat,lon)
setRadius(20)
convertLatLonToProj()



#def getBoxValues(boxRad,rasterBand):
boxRad=20
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

a=1

pyplot.figure(1)
bA=osgeo.gdal_array.BandReadAsArray(rasterBands[a],UL[0],UL[1],40,40)
#pyplot.imshow(bA,vmin=rasterArrays[a].min(),vmax=rasterArrays[a].max())
pyplot.imshow(bA)
pyplot.tick_params(labelbottom='off',labeltop='on')
pyplot.colorbar()

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

pyplot.figure(3)
pyplot.imshow(rasterArrays[a])
pyplot.plot(477,177,'mo',markersize=6)
#pyplot.axis([rightSide,leftSide,bottomSide,topSide])
pyplot.xlim(0,1799)
pyplot.ylim(0,1059)
pyplot.gca().invert_yaxis()
#pyplot.gca().invert_xaxis()
pyplot.tick_params(labelbottom='off',labeltop='on')




