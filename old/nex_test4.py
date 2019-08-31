# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:17:10 2017

@author: tanner
"""


import gdal
from osgeo import osr
import osgeo

import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import numpy
import Image


#iLoc='/media/tanner/vol2/NCR/MSX_NCR_0.gif'
iLoc='/media/tanner/vol2/NCR/EVX_NCR_0.gif'
jLoc='/media/tanner/vol2/NCR/EVX_NCR_0.gfw'


tLoc='/media/tanner/vol2/HRRR/hrrr.t19z.wrfsfcf04.grib2'

ds=gdal.Open(iLoc)
#qq=gdal.Open(jLoc)

band=ds.GetRasterBand(1)
bandArray=band.ReadAsArray()

#pyplot.imshow(bandArray,cmap='inferno')

#ds.SetProjection('NAD-83')

#raster_wkt= ds.GetProjection()
spatial_ref=osr.SpatialReference()
#spatial_ref.ImportFromWkt(raster_wkt)
#
oldCS=osr.SpatialReference()    
newCS=osr.SpatialReference()
#
oldCS.ImportFromEPSG(4326)
newCS.ImportFromEPSG(4152)
#
transform=osr.CoordinateTransformation(oldCS,newCS)

#coords=[30.398421,-86.466861]
coords=[31.320206,-92.482054]
location=[30.394226,-86.487741]

gt=ds.GetGeoTransform()

x,y,z=transform.TransformPoint(location[1],location[0])

px=int((x-gt[0])/gt[1])
py=int((y-gt[3])/gt[5])

print px
print py




















