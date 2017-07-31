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

datDir='/home/ubuntu/fwas_data/WWA/'
#datDir='/home/tanner/vol2/WWA/'
fFile=datDir+'current_ww.zip'
zDir=datDir+'current_ww/'

def fetchZip(URL):
    """
    Fetches new WWA Alerts
    """
    print 'Fetching wwa from iastate.edu...'
    response=urllib2.urlopen(URL)
    output=open(fFile,'wb')
    output.write(response.read())
    output.close()
    
def extractZip():
    """
    IA state keeps everything as a shp file in a zip file, here
    is where it is extracted
    """
    print 'extracting WWA...'
    with zipfile.ZipFile(fFile,'r') as z:
        z.extractall(zDir)

def runOGR2OGR():
    """
    Converts SHP to GeoJSON, which is very useful
    """
    print 'Running ogr2ogr: Convert shp to geoJSON...'
    cmd=['/usr/local/bin/ogr2ogr',
    '-f','GeoJSON','-t_srs','crs:84',
    str(zDir+'current.geojson'),
    str(zDir+'current_ww.shp')]
    subprocess.check_call(cmd)
    
def FetchWWA():
    """
    Runs everything above
    """
    fetchZip(URL)
    extractZip()
    runOGR2OGR()
    