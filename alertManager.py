#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:03:23 2017

@author: tanner
"""

import glob
import ConfigParser
import calcTime
import datetime
import one
import os

checkTime=datetime.datetime.now()
cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')

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

for i in range(len(cZ)):
    tExpire=readExpirationDate(cZ[i])
    tTime=calcTime.calcExpirationDate(tExpire['alert_time'],tExpire['expires_after'])
    if tTime>checkTime: #This means the alert has not yet expired and can be used!
        print "Alert is Valid... Checking Weather..."
        one.ascertainCfg(cZ[i])
        one.runFWAS()
        print True
    if tTime<checkTime: #This means the Alert Has expired and should be removed!
        print "Alert has expired... Deleting alert..."
        os.remove(cZ[i])
        print False
