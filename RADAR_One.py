#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:38:41 2017

@author: tanner

This is the alert Manager for Radar Alerts
It won't delete alerts and relies on the primary alert manager for that
(alertmanager.py)
RADAR_One.py is run every 15-20 minutes rather than hourly.
Alerts are independent of the other ones and send as a separate message
"""

import glob
import ConfigParser
import datetime
import time

import send
import createAlert

import CONUS_RADAR_Run
import NCR_Run
import NEXRAD_Run
import CONUS_RADAR_Fetch
#from one import configureNotifications

###############################################################################
# If we ever decide to use Composite Radar or Level II Products, they exist   #
# but are disabled                                                            #
# Eventually they could be reenabled here. With Some Work...                  #
###############################################################################
radarType='CONUS'
#radarType='NCR'
#radarType='NEXRAD'

Threshold=40.0
nowTime=time.time()
hourLen=3600.0 #Seconds
cfgLoc=[''] #The Config File we are reading
#cfgLoc[0]='/home/tanner/src/breezy/cfgLoc/threshold-USERNAME-2017-07-24_15-48-52.cfg'

checkTime=datetime.datetime.now()
import PATHFILE
fp = PATHFILE.FWAS_PATHS()
cZ = glob.glob(fp.get_alertDataPath()+"*.cfg")

#cZ=glob.glob('/home/tanner/src/breezy/fwas/data/*.cfg')
#cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#cZ=[cfgLoc[0]]
#cZ=['/srv/`shiny-server/fwas/data/threshold-USERNAME-2017-07-06_18-15-22.cfg']
#cZ=['/srv/shiny-server/fwas/data/threshold-USERNAME-2017-06-29_17-45-43.cfg']
#cfgLoc[0]=cZ[0]

def readThresholds():
    """
    This is a simpler version of the one found in one.py as it only handles one var
    rather than 3
    """
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    headerDict={}
    precipDict={}
    radarDict={}
    tStormDict={}
    options=cfg.options(cfg.sections()[0])
    section=cfg.sections()[0]
    for i in range(len(options)):
        headerDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[4])
    section=cfg.sections()[4]
    for i in range(len(options)):
        precipDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[5])
    section=cfg.sections()[5]
    for i in range(len(options)):
        radarDict[options[i]]=cfg.get(section,options[i])
    options=cfg.options(cfg.sections()[7])
    section=cfg.sections()[7]
    for i in range(len(options)):
        tStormDict[options[i]]=cfg.get(section,options[i])
    return [headerDict,precipDict,radarDict,tStormDict]

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

def setVars(tStormLib,precipLib):
    """
    Does simple conversion from Str to Bool if user wants Thunderstorms, precip or both from Radar
    """
    stormBool=False #stool
    precipBool=False #pool
    if tStormLib['thunderstorm_on']=='1':
        stormBool=True
    if precipLib['precip_on']=='1':
        precipBool=True
    
    return [stormBool,precipBool]
    
def writeRadarTime(cfgLoc,utime):
    """
    Writes a time to their config file, so that alerts only go out once
    every hour after the first alert was sent. This is cool because
    it checks for the first storm, finds it, sends it and then essentially
    sleeps for 1 hour.
    """
    cfg=ConfigParser.ConfigParser()
    cfg.read(cfgLoc)
    options=cfg.options(cfg.sections()[5])
    section=cfg.sections()[5]
    cfg.set(section,options[2],str(utime))
    with open(cfgLoc,'w') as nCfg:
        cfg.write(nCfg)

#Below is what runs
#Because all that is implemented right now is CONUS_RADAR
#We just pull that first to save time and cpu usage...
CONUS_RADAR_Fetch.fetchRadar(False)
for i in range(len(cZ)):
    print 'Reading Radar Thresholds for',cZ[i],'...'
    cfgLoc[0]=cZ[i]
    headerLib,precipLib,radarLib,tStormLib=readThresholds()
    if radarLib['radar_on']=='0':
        continue
    print 'Alert Name:',headerLib['alert_name']
    time_diff=nowTime-float(radarLib['radar_time'])
        
    aVars=setVars(tStormLib,precipLib)
    if aVars[0]==False and aVars[1]==False:
        print 'User',headerLib['email'],headerLib['phone'],'does not want radar data... o_O'        
        continue
    alert=''
    if time_diff>=hourLen:
        print 'More Than One Hour Has Passed since last radar check, checking Radar...'
        print 'Time Since last Alert: ',time_diff,'seconds'        
        if radarType=='CONUS':
            print 'Using Default...'
            print 'Checking CONUS Base Reflectivity...'
            alert=CONUS_RADAR_Run.getRadarAlerts(aVars[0],headerLib,radarLib,False,Threshold,aVars[1],40)
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
            subj=headerLib['alert_name']
            endAlert="\nThis alert can be stopped by replying: stop "+headerLib['alert_name']+"\n"
            alert=alert+endAlert
    #        print alert
            send.sendEmailAlert(alert,contact,subj,cMeth)
            writeRadarTime(cZ[i],time.time())
        if not alert:
            print "No RADAR Found, Checking again in 15..."
        
    if time_diff<hourLen:
        print 'Less than one Hour has passed since last radar alert...'
        print 'Waiting',hourLen-time_diff,'seconds...'
        continue
    
    
    
    
    
    
    
    
