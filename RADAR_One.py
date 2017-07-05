#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:38:41 2017

@author: tanner
"""

import glob
import ConfigParser
import datetime

import send
import createAlert

import CONUS_RADAR_Run
import NCR_Run
import NEXRAD_Run
#from one import configureNotifications

radarType='CONUS'
#radarType='NCR'
#radarType='NEXRAD'

Threshold=40.0

cfgLoc=['']

checkTime=datetime.datetime.now()
#cZ=glob.glob('/home/tanner/src/breezy/fwas/data/*.cfg')
cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#cZ=['/srv/shiny-server/fwas/data/threshold-USERNAME-2017-06-29_17-45-43.cfg']
#cfgLoc[0]=cZ[0]

def readThresholds():
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    headerDict={}
    radarDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        headerDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[5])
    section=cfg.sections()[5]
    for i in range(len(options)):
        radarDict[options[i]]=cfg.get(section,options[i])
    
    return [headerDict,radarDict]

def configureNotifications(header):
    """
    Figures out email or text message
    """
    sendTo=''
    valid=createAlert.listSMSGateways()
    if header['email']=='NaN':
        gateway=createAlert.getSMSGateway(header['carrier'],valid)
        sendTo=header['phone']+'@'+gateway
    if header['phone']=='NaN':
        sendTo=header['email']
    if header['phone']!='NaN' and header['email']!='NaN':
        gateway=createAlert.getSMSGateway(header['carrier'],valid)
        sendTo=[str(header['phone']+'@'+gateway),header['email']]
    if header['phone']=='NaN' and header['email']=='NaN':
        sendTo='NONE'
    return sendTo

def configureSendMethod(To):
    if type(To) is list:
        return 'BOTH'
    if type(To) is str:
        return 'REGULAR'
    
for i in range(len(cZ)):
    print 'Reading Radar Thresholds for',cZ[i],'...'
    cfgLoc[0]=cZ[i]
    headerLib,radarLib=readThresholds()
    alert=''
    if radarType=='CONUS':
        print 'Using Default...'
        print 'Checking CONUS Base Reflectivity...'
        alert=CONUS_RADAR_Run.getRadarAlerts(headerLib,radarLib,False,Threshold)
    if radarType=='NCR':
        print 'Using Composite Reflectivity...'
        print 'Checking...'
        alert=NCR_Run.getRadarAlerts(headerLib,radarLib,False,Threshold)
    if radarType=='NEXRAD':
        print 'Using Level II Product...'
        print 'WARNING: may be very slow...'
        print 'checking...'
        alert=NEXRAD_Run.runNEXRAD(headerLib,radarLib,'America/Denver',False)  
        
    if alert:
        contact=configureNotifications(headerLib)
        cMeth=configureSendMethod(contact)
        print "Radar Threshold Met!"
        subj='Radar Alert: '+headerLib['alert_name']
        send.sendEmailAlert(alert,contact,subj,cMeth)
    if not alert:
        print "No RADAR Found, Checking again in 15..."
    
    
    
    
    
    
    
    
