# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:06:59 2017

@author: tanner

SOURCE:
https://mesonet.agron.iastate.edu/data/gis/shape/4326/us/current_ww.zip
"""

import urllib2
import zipfile
import subprocess

URL='https://mesonet.agron.iastate.edu/data/gis/shape/4326/us/current_ww.zip'

#datDir='/home/ubuntu/fwas_data/WWA/'
datDir='/home/tanner/vol2/WWA/'
fFile=datDir+'current_ww.zip'
zDir=datDir+'current_ww/'

def fetchZip(URL):
    print 'Fetching wwa from iastate.edu...'
    response=urllib2.urlopen(URL)
    output=open(fFile,'wb')
    output.write(response.read())
    output.close()
    
def extractZip():
    print 'extracting WWA...'
    with zipfile.ZipFile(fFile,'r') as z:
        z.extractall(zDir)

def runOGR2OGR():
    print 'Running ogr2ogr: Convert shp to geoJSON...'
    cmd=['/usr/local/bin/ogr2ogr',
    '-f','GeoJSON','-t_srs','crs:84',
    str(zDir+'current.geojson'),
    str(zDir+'current_ww.shp')]
    subprocess.check_call(cmd)
    
def FetchWWA():
    fetchZip(URL)
    extractZip()
    runOGR2OGR()
    