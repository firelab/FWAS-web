# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:47:28 2017

@author: tanner
"""

import gdal
from osgeo import osr
import osgeo
import matplotlib.pyplot as pyplot
import glob

cZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
#a=0

fFile=cZ[1]

ds=gdal.Open(fFile)
dataset=ds


rasterSKA=[]
rasterSHIT=[]

for i in range(1,8):  
    band=ds.GetRasterBand(i)
    bandArray=band.ReadAsArray()
    rasterSKA.append(band)
    rasterSHIT.append(bandArray)

#band=ds.GetRasterBand(1)
#bandArray=band.ReadAsArray()
#rasterSKA.append(band)
#rasterSHIT.append(bandArray)
    
#0 is reflectivity
#1 is lightning
#2 is Temperature BAD
#3 is Temperature GOOD
#4 is RH
#5 is WIND
#6 is PRECIP RATE

rasterBands=[]
rasterArrays=[]

#rasterBands.append(band)
#rasterArrays.append(bandArray)

# I would prefer
#0 is reflectivity
#1 is Temp
#2 is RH
#3 is Lightning
#4 is precip rate
#5 is Wind


rasterBands.append(rasterSKA[0])
rasterBands.append(rasterSKA[3])
rasterBands.append(rasterSKA[4])
rasterBands.append(rasterSKA[1])
rasterBands.append(rasterSKA[6])
rasterBands.append(rasterSKA[5])
#
rasterArrays.append(rasterSHIT[0])
rasterArrays.append(rasterSHIT[3])
rasterArrays.append(rasterSHIT[4])
rasterArrays.append(rasterSHIT[1])
rasterArrays.append(rasterSHIT[6])
rasterArrays.append(rasterSHIT[5])

#del rasterSKA,rasterSHIT



a=4

#centerX=1155
#centerY=440
centerX=477
centerY=200
boxRad=20

leftSide=centerX-boxRad
rightSide=centerX+boxRad
topSide=centerY-boxRad
bottomSide=centerY+boxRad
#"""
#FLASHES/(km^2*5_min)
#"""
#
pyplot.figure(2)
pyplot.imshow(rasterArrays[a])
pyplot.plot(centerX,centerY,'mo',markersize=6)
pyplot.axis([rightSide,leftSide,bottomSide,topSide])
#pyplot.xlim(0,1799)
#pyplot.ylim(0,1059)
#pyplot.gca().invert_yaxis()
pyplot.gca().invert_xaxis()
pyplot.tick_params(labelbottom='off',labeltop='on')
pyplot.colorbar()
pyplot.show()       
#a=5

pyplot.figure(3)
pyplot.imshow(rasterArrays[a])
pyplot.plot(centerX,centerY,'mo',markersize=6)
#pyplot.axis([rightSide,leftSide,bottomSide,topSide])
pyplot.xlim(0,1799)
pyplot.ylim(0,1059)
pyplot.gca().invert_yaxis()
#pyplot.gca().invert_xaxis()
pyplot.tick_params(labelbottom='off',labeltop='on')
pyplot.colorbar()
pyplot.show()   
      
#pyplot.figure(4)
#pyplot.imshow(rasterSHIT[2])
#pyplot.plot(centerX,centerY,'mo',markersize=6)
##pyplot.axis([rightSide,leftSide,bottomSide,topSide])
#pyplot.xlim(0,1799)
#pyplot.ylim(0,1059)
#pyplot.gca().invert_yaxis()
##pyplot.gca().invert_xaxis()
#pyplot.tick_params(labelbottom='off',labeltop='on')
#pyplot.colorbar()
#pyplot.show()   