#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 21:33:11 2017

@author: tanner

This is the Master Run Script for NWS WWA Alerts. Aside from Instant Alerts, 
this is the file executed or run via cron.
"""

import send
import glob
import ConfigParser
import calcTime
import createAlert
import time

import WWA_Run

nowTime=time.time()
hourLen=10800.0 #3 Hours in seconds!

cfgLoc=['']

cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
def readThresholds():
    """
    This is a simpler version of the one found in one.py as it only handles one var
    rather than 3 (For WWA)
    """
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    headerDict={}
    radarDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        headerDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[6])
    section=cfg.sections()[6]
    for i in range(len(options)):
        radarDict[options[i]]=cfg.get(section,options[i])
    
    return [headerDict,radarDict]

def configureNotifications(header):
    """
    Figures out email or text message
    """
    sendTo=''
    valid=createAlert.listSMSGateways()
#    if header['email']=='NaN':
#        gateway=createAlert.getSMSGateway(header['carrier'],valid)
#        sendTo=header['phone']+'@'+gateway
#    if header['phone']=='NaN':
#        sendTo=header['email']
#    if header['phone']!='NaN' and header['email']!='NaN':
#        gateway=createAlert.getSMSGateway(header['carrier'],valid)
#        sendTo=[str(header['phone']+'@'+gateway),header['email']]
#    if header['phone']=='NaN' and header['email']=='NaN':
#        sendTo='NONE'
    if header['email']=='NaN' and header['carrier']!='NaN':
        gateway=createAlert.getSMSGateway(header['carrier'],valid)
        sendTo=header['phone']+'@'+gateway
    if header['phone']=='NaN' and header['email']!='NaN':
        sendTo=header['email']
    if header['phone']!='NaN' and header['email']!='NaN':
        gateway=createAlert.getSMSGateway(header['carrier'],valid)
        sendTo=[str(header['phone']+'@'+gateway),header['email']]
    if header['phone']=='NaN' and header['email']=='NaN':
        sendTo='NONE'
    return sendTo
  
def configureSendMethod(To):
    """
    If they user wants both text and email alerts
    """
    if To=='NONE':
        return 'NONE'
    if type(To) is list:
        return 'BOTH'
    if type(To) is str:
        return 'REGULAR'

def writeWWATime(cfgLoc,uTime):
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    options=cfg.options(cfg.sections()[6])
    section=cfg.sections()[6]
    cfg.set(section,options[1],str(uTime))
    with open(cfgLoc,'w') as nCfg:
        cfg.write(nCfg)

x=0
y=0
for i in range(len(cZ)):
    print 'Reading wWA Thresolds for',cZ[i],'...'
    cfgLoc[0]=cZ[i]
    headerLib,wwaLib=readThresholds()
    print 'Alert Name:',headerLib['alert_name']
    time_diff=nowTime-float(wwaLib['wwa_time'])
    if time_diff>=hourLen:   
        print 'More Than 3 Hours have Passed Since Last WWA Check...'
        print 'Time Since Last Alert:',time_diff,'Seconds'
        if wwaLib['wwa_on']=='1':
            x+=1
            tz=calcTime.convertTimeZone(int(headerLib['time_zone']))
            alert=WWA_Run.runWWA(headerLib,tz,False,True)
            if alert:
                contact=configureNotifications(headerLib)
                cMeth=configureSendMethod(contact)
                print 'WWA Found...'
                subj=headerLib['alert_name']
                send.sendEmailAlert(alert,contact,subj,cMeth)
                writeWWATime(cZ[i],time.time())
            if not alert:
                print 'No WWA Found...'
        else:
            print 'WWA Turned off for',cZ[i]
            y+=1   
    #        continue
    if time_diff<hourLen:
        print 'Less than Three Hours have passed since last WWA Alert...'
        print 'Waiting',hourLen-time_diff,'seconds...'
        continue

    
#def runInitialWWA(cfg):
#    print 'Reading wWA Thresolds for',cfg,'...'
#    cfgLoc[0]=cfg
#    headerLib,wwaLib=readThresholds()
#    if wwaLib['wwa_on']=='1':
#        x+=1
#        tz=calcTime.convertTimeZone(int(headerLib['time_zone']))
#        alert=WWA_Run.runWWA(headerLib,tz,False,True)
#        if alert:
#            contact=configureNotifications(headerLib)
#            cMeth=configureSendMethod(contact)
#            print 'WWA Found...'
#            subj='NWS WWA: '+headerLib['alert_name']
#            send.sendEmailAlert(alert,contact,subj,cMeth)
#        if not alert:
#            print 'No WWA Found...'
#    else:
#        print 'WWA Turned off for',cZ[i]
#        y+=1   
    #        continue

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    