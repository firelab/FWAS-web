# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:20:43 2017

@author: tanner
"""
from mpl_toolkits.basemap import Basemap
import osr, gdal
import matplotlib.pyplot as plt
import numpy as np
import gdal
#gdata=gdal.Open('/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2')
#geo=dataset.GetGeoTransform()
#d=gdata.GetRasterBand(1)
#data=d.ReadAsArray()

def convertXY(xy_source, inproj, outproj):
    # function to convert coordinates

    shape = xy_source[0,:,:].shape
    size = xy_source[0,:,:].size

    # the ct object takes and returns pairs of x,y, not 2d grids
    # so the the grid needs to be reshaped (flattened) and back.
    ct = osr.CoordinateTransformation(inproj, outproj)
    xy_target = np.array(ct.TransformPoints(xy_source.reshape(2, size).T))

    xx = xy_target[:,0].reshape(shape)
    yy = xy_target[:,1].reshape(shape)

    return xx, yy
    
# Read the data and metadata
ds = gdal.Open('/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2')

data = ds.GetRasterBand(1).ReadAsArray()
gt = ds.GetGeoTransform()
proj = ds.GetProjection()

xres = gt[1]
yres = gt[5]

# get the edge coordinates and add half the resolution 
# to go to center coordinates
xmin = gt[0] + xres * 0.5
xmax = gt[0] + (xres * ds.RasterXSize) - xres * 0.5
ymin = gt[3] + (yres * ds.RasterYSize) + yres * 0.5
ymax = gt[3] - yres * 0.5

ds = None

# create a grid of xy coordinates in the original projection
xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]

# Create the figure and basemap object
fig = plt.figure(figsize=(12, 6))
m = Basemap(projection='robin', lon_0=0, resolution='c')

# Create the projection objects for the convertion
# original (Albers)
inproj = osr.SpatialReference()
inproj.ImportFromWkt(proj)

# Get the target projection from the basemap object
outproj = osr.SpatialReference()
outproj.ImportFromProj4(m.proj4string)

# Convert from source projection to basemap projection
xx, yy = convertXY(xy_source, inproj, outproj)

# plot the data (first layer)
im1 = m.pcolormesh(xx, yy, data[0,:,:].T, cmap=plt.cm.jet)

# annotate
m.drawcountries()
m.drawcoastlines(linewidth=.5)

#plt.savefig('world.png',dpi=75)