#******************************************************************************
#
#  Project:  wrfCoordTransform.py
#  Purpose:  Transform a point from lat/long to WRF space
#  Author:   Natalie Wagenbrenner <nwagenbrenner@gmail.com>
#
#******************************************************************************
#  No Copyright, Public Domain
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#******************************************************************************

import gdal
from gdalconst import *
#import struct
import osr

##
# open the dataset
#
ds = gdal.Open('/home/natalie/DN/FESD/geo_em.d01.nc', \
     GA_ReadOnly )
if ds is None:
    print 'Cannot open WRF file.'

print 'Driver:', ds.GetDriver().ShortName,'/', \
    ds.GetDriver().LongName

##
# define and set projection string
#
projString = "PROJCS[\"WGC 84 / WRF Lambert\",GEOGCS[\"WGS 84\",\
              DATUM[\"World Geodetic System 1984\",\
              SPHEROID[\"WGS 84\",6378137.0,298.257223563,\
              AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],\
              PRIMEM[\"Greenwich\",0.0,AUTHORITY[\"EPSG\",\"8901\"]],\
              UNIT[\"degree\",0.017453292519943295],\
              AXIS[\"Geodetic longitude\",EAST],AXIS[\"Geodetic latitude\",NORTH],\
              AUTHORITY[\"EPSG\",\"4326\"]],\
              PROJECTION[\"Lambert_Conformal_Conic_2SP\"],\
              PARAMETER[\"central_meridian\",-97],\
              PARAMETER[\"latitude_of_origin\",43.19017],\
              PARAMETER[\"standard_parallel_1\",33],\
              PARAMETER[\"false_easting\",0.0],PARAMETER[\"false_northing\",0.0],\
              PARAMETER[\"standard_parallel_2\",45],\
              UNIT[\"m\",1.0],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH]]";


newCS = osr.SpatialReference()
newCS.ImportFromWkt(projString)
newCS.ExportToWkt()

oldCS = osr.SpatialReference()
oldCS.ImportFromEPSG(4326)  #WGS84 code

##
# create transformation object
#
transform = osr.CoordinateTransformation(oldCS, newCS)


##
# perform the transformation
#
xCenter = -116.5251  
yCenter = 43.19017
z = 0

xCenterWRF, yCenterWRF, z = transform.TransformPoint(xCenter,yCenter)

#now calculate distance in WRF space from center to llcorner
#nXSize = ds.RasterXSize  #for some reason gdal is reading this as 512, not 214...weird.
#nYSize = ds.RasterYSize  #for some reason gdal is reading this as 512, not 286...weird.
#dx = nXSize/2  
#dy = nXSize/2
dx = 214/2
dy = 286/2
cellSize = 12000
xllCorner = xCenterWRF-(dx*cellSize)
yllCorner = yCenterWRF-(dy*cellSize)

#check the transform
transformRev = osr.CoordinateTransformation(newCS, oldCS)
transformRev.TransformPoint(xllCorner,yllCorner)
transformRev.TransformPoint(xCenterWRF, yCenterWRF)




