#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:49:54 2017

@author: tanner
"""

import pykml.parser
import urllib2
import os
import zipfile
import glob

#path='/media/tanner/vol2/NIFC/'
#kPath='/media/tanner/vol2/NIFC/conus_lg_incidents.kmz'
#cPath='/media/tanner/vol2/NIFC/incidents.csv'
#nDir='/media/tanner/vol2/OSM/conuskml/'
#path='/home/ubuntu/fwas_data/NIFC/'
#kPath='/home/ubuntu/fwas_data/NIFC/conus_lg_incidents.kmz'
#cPath='/home/ubuntu/fwas_data/NIFC/incidents.csv'
#npath='/home/ubuntu/fwas_data/NIFC/'

import PATHFILE
fp = PATHFILE.FWAS_PATHS()
path = fp.get_nifcDataPath()
kPath = path+"conus_lg_incidents.kmz"
cPath = path+"incidents.csv"
#npath = 

def fetchKMZ():
    url='https://fsapps.nwcg.gov/afm/data/kml/conus_lg_incidents.kmz'
    response=urllib2.urlopen(url)
    kmz=open(kPath,'wb')
    kmz.write(response.read())
    kmz.close()

def createZip():
    os.rename(kPath,kPath[:-3]+'zip')

def extractZip():
    with zipfile.ZipFile(kPath[:-3]+'zip',"r") as z:
        z.extractall(path)

def writeCSV():
    kmlPath=glob.glob(path+'*.kml')
    root=pykml.parser.fromstring(open(kmlPath[0],'r').read())
    num_incidents=len(root.Document.Folder[1].Placemark)
    f=open(cPath,'w')
    f.write('Fire Name,Longitude,Latitude,0\n')
    incList=[]
    for j in range(num_incidents):
        incident=root.Document.Folder[1].Placemark[j]
        print incident.name,incident.Point.coordinates
        incList.append([str(incident.name),str(incident.Point.coordinates)])
    
    incList.sort()
    for i in range(len(incList)):
        f.write(str(incList[i][0]))
        f.write(',')
        f.write(str(incList[i][1]))
        f.write('\n')
    f.close()



fetchKMZ()
createZip()
extractZip()
writeCSV()
    
    





    
