# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:11:55 2017

@author: tanner
"""

import matplotlib.pyplot as pyplot

import gdal
import ogr
ds=gdal.Open('/media/tanner/vol2/HRRR/hrrr.t04z.wrfsfcf10.grib2')
dataset=ds

dArray=ds.GetRasterBand(4).ReadAsArray()
pyplot.imshow(dArray)