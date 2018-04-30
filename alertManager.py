#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:03:23 2017

@author: tanner

FWAS Alert Manager: run this As Primary CRONJOB for HRRR & RAWS 

"""

import glob
import ConfigParser
import calcTime
import datetime
import one
import os
import HRRR_Fetch
from HRRR_Parse import getDataset,getDiskFiles
from multiprocessing import Pool
import time
import threshold_archiver

checkTime=datetime.datetime.now()
cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#cZ=glob.glob('/home/tanner/src/breezy/fwas/data/*.cfg')
threshold_archiver.backup_cfg()

def readExpirationDate(cfgLoc):
    """
    reads first part of config file to see if alert is expired
    """
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    headerDict={}
#    thresholdDict={}
#    unitDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        headerDict[options[i]]=cfg.get(section,options[i])
#    options=cfg.options(cfg.sections()[1])
#    section=cfg.sections()[1]
#    for i in range(len(options)):
#        thresholdDict[options[i]]=cfg.get(section,options[i])
#    options=cfg.options(cfg.sections()[2])
#    section=cfg.sections()[2]
#    for i in range(len(options)):
#        unitDict[options[i]]=cfg.get(section,options[i])
    return headerDict

def getNewForecasts():
    """
    Download new HRRR Data. Runs every Hour
    """
    HRRR_Fetch.cleanHRRRDir()
    HRRR_Fetch.fetchHRRR()     
        
#This is where HRRR Grib files get read 
#into the program now to speed things up!
xStart=time.time()
getNewForecasts()
xEnd=time.time()

start=time.time()
dF=getDiskFiles()
dsList=[]
for i in range(len(dF)):
    ds=getDataset(i)
    dsList.append(ds)
dsList.sort()

"""
#################################
#
# Multiprocessing Function
#
#################################
"""
def runCore(cfg):
    try:
        one.ascertainCfg(cfg)
        one.runFWAS(dsList)
        print True
        return True
    except:
        print 'Could not Generate Alert for:',cZ[i],'Something is Wrong...'
        print False
        return False
        pass


#    return hDict

"""
Single Core Stuff: use if something bad happened with multiproc
""" 
#getNewForecasts()
#for i in range(len(cZ)):
#    tExpire=readExpirationDate(cZ[i])
#    tTime=calcTime.calcExpirationDate(tExpire['alert_time'],tExpire['expires_after'])
#    if tTime>checkTime: #This means the alert has not yet expired and can be used!
#        print "Alert is Valid... Checking Weather..."
#        one.ascertainCfg(cZ[i])
#        try:
#            one.runFWAS(dsList)
#            print True
#        except:
#            print 'Could not Generate Alert for',cZ[i],'Something is wrong...'
#            print False
#            pass
#    if tTime<checkTime: #This means the Alert Has expired and should be removed!
#        print "Alert has expired... Deleting alert..."
#        print cZ[i]
#        os.remove(cZ[i])
#        print False

"""
MultiProc Stuff (Way Faster!)
"""
casiopea=[] #List of good forecasts
for i in range(len(cZ)):
    tExpire=readExpirationDate(cZ[i])
    tTime=calcTime.calcExpirationDate(tExpire['alert_time'],tExpire['expires_after'])
    if tTime>checkTime: #This means the alert has not yet expired and can be used!
        print "Alert is Valid... Proceeding..."
        casiopea.append(cZ[i])
    if tTime<checkTime: #This means the Alert Has expired and should be removed!
        print "Alert has expired... Deleting alert..."
        print cZ[i]
        os.remove(cZ[i])
        print False
  
pool=Pool()
results=pool.map(runCore,casiopea)
pool.close()
pool.join()
end=time.time()
print '------------------------------------------'
print 'FWAS Duration:',end-start
print 'FWAS+HRRR:',end-xStart
print '------------------------------------------'











