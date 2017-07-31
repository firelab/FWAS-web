# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 15:42:38 2017

@author: tanner
"""
import ConfigParser
import WWA_Run
import calcTime
import createAlert
import send

cfgLoc=['']

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
#     FORECASTED MAX wind speed: 15 mph at 02:00 PM, 07-25-2017   sendTo=[str(header['phone']+'@'+gateway),header['email']]
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
        
#/srv/shiny-server/fwas/data/threshold-USERNAME-2017-07-24_15-48-52.cfg
def runInitialWWA(cfg):
    """
    Runs WWA when instantAlert.py is called from the UI (shiny)
    """
    print 'Reading wWA Thresolds for',cfg,'...'
    cfgLoc[0]=cfg
    headerLib,wwaLib=readThresholds()
    if wwaLib['wwa_on']=='1':
        tz=calcTime.convertTimeZone(int(headerLib['time_zone']))
        alert=WWA_Run.runInitialWWA(headerLib,tz,False,True)
        if alert:
#            alert+='\n WWA Alerts are sent every 3 hours '
            contact=configureNotifications(headerLib)
            cMeth=configureSendMethod(contact)
            print 'WWA Found...'
            subj='NWS WWA: '+headerLib['alert_name']
            send.sendEmailAlert(alert,contact,subj,cMeth)
        if not alert:
            print 'No WWA Found...'
    else:
        print 'WWA Turned off for',cfg
#            continue