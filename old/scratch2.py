# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 08:49:53 2017

@author: tanner
"""
import glob
import gdal
from osgeo import osr
import calcDist


cZ=glob.glob('/home/tanner/src/breezy/HRRR/grib/*.grib2')
dataset=gdal.Open(cZ[0])

lat=40.92
lon=-87.66

covfefe=[0,0]
reverse=[0,0]

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
x,y,z=transform.TransformPoint(lon,lat)
gt=dataset.GetGeoTransform()
px=int((x-gt[0])/gt[1])
py=int((y-gt[3])/gt[5])
covfefe[0]=px
covfefe[1]=py

back=osr.CoordinateTransformation(newCS,oldCS)

xN=1450*gt[1]+gt[0]
yN=465*gt[5]+gt[3]

#print "oProj: ",x,y
#print "nProj: ",xN,yN
#print "diff: ",abs(x-xN),abs(yN-y)

lo,la,z=back.TransformPoint(xN,yN)
print la,lo
print lat,lon

spa=calcDist.getSpatial([lat,lon],[la,lon])




























