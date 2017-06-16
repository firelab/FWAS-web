# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:18:39 2017

@author: tanner
"""

import math
import numpy
import pyproj
import gdal
from gdalconst import *
#import struct
import osr

ds=gdal.Open('/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2')
dataset=ds

#def toLCC(lat,lon,spOne,spTwo,LOA,CM):
#    
##    F=numpy.cos(spOne)*(tan)
#    
#
#    x=rho*numpy.sin(n*(lon-LOA))
#    y=rho0-rho*numpy.cos(n*(lon-LOA))

raster_wkt = ds.GetProjection()
spatial_ref = osr.SpatialReference()
spatial_ref.ImportFromWkt(raster_wkt)
print spatial_ref.ExportToPrettyWkt()


#lat=46.926183
#lon=-114.092779

lat=29.9918
lon=-90.076800
newCS=osr.SpatialReference()
newCS.ImportFromWkt(spatial_ref.ExportToWkt())

oldCS=osr.SpatialReference()
oldCS.ImportFromEPSG(4326)

transform=osr.CoordinateTransformation(oldCS,newCS)

z=0

x,y,z=transform.TransformPoint(lon,lat)
gt=ds.GetGeoTransform()
px=int((x-gt[0])/gt[1])
py=int((y-gt[3])/gt[5])

print px,py