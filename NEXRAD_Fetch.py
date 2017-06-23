# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:05:01 2017

@author: tanner
"""

import datetime
from siphon.radarserver import RadarServer
import urllib2
import glob
import os

'https://noaa-nexrad-level2.s3.amazonaws.com/2017/06/20/KMSX/KMSX20170620_165708_V06'

def buildURL(stid):
    now=datetime.datetime.utcnow()
    base=' https://unidata-nexrad-level2-chunks.s3.amazonaws.com/'
    base2='https://noaa-nexrad-level2.s3.amazonaws.com/'
    date1=str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'
    date2=str(now.year)+str(now.month)+str(now.day)+'_'+str(now.hour)    
    return [base,base2,date1,date2]
#buildURL('KMSX')

def fetchStation(stid):
    rs=RadarServer('http://thredds-aws.unidata.ucar.edu/thredds/radarServer/nexrad/level2/S3/')
    query=rs.query()
    query.stations(str(stid).upper()).time(datetime.datetime.utcnow())
    catalog=rs.get_catalog(query)
    
    ds=list(catalog.datasets.values())[0]
    
    url=ds.access_urls['HTTPServer']
    
    dataDir='/media/tanner/vol2/NEXRAD/'
#    dataDir='/home/ubuntu/fwas_data/NEXRAD/'
    fName=dataDir+url[88:]
    response=urllib2.urlopen(url)
    output=open(fName,'wb')
    output.write(response.read())
    output.close()
    return fName

def cleanDir():
    cZ=glob.glob('/media/tanner/vol2/NEXRAD/*')
#    cZ=glob.glob('/home/ubuntu/fwas_data/NEXRAD/*')
    for i in range(len(cZ)):
        os.remove(cZ[i])
    