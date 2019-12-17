# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:33:56 2017

@author: tanner

WATCH WARNING ADVISORY Parser
"""

import csv
import datetime
import dateutil
import dateutil.tz

vtec_Path='/home/ubuntu/fwas_data/WWA/vtec/'
#vtec_Path='/home/tanner/vol2/WWA/vtec/'
aaa='vtec_aaa.csv'
k='vtec_k.csv'
pp='vtec_pp.csv'
s='vtec_s.csv'

#u_tz='America/Denver' #This will need to be specified by a CFG File later

class WWA:
    """
    struct that holds good stuff  about a WWA
    """
    start_time=''
    end_time=''
    cType=''
    cSig=''
    cStatus=''
    wfo=''
    gtype=''
    hType=''
    hSig=''
    hStatus=''
    ugc=''
    
 
def printWWA(wwa):
    """
    Prints info in a WWA class, good for debugging
    """
    print '----------------------------'
    print 'WATCH WARNING ADVISORY PRINTER'
    print '----------------------------'
    print 'start_time:',wwa.start_time
    print 'end_time:',wwa.end_time
    print 'coded_type:',wwa.cType
    print 'coded_sig:',wwa.cSig
    print 'coded_status:',wwa.cStatus
    print 'human_type:',wwa.hType
    print 'human_sig:',wwa.hSig
    print 'human_status:',wwa.hStatus
    print 'Weather Forecasting Office:',wwa.wfo
    print 'GTYPE:',wwa.gtype
    print 'NWS_UGC:',wwa.ugc
    print '----------------------------'

 
def getWarnTimes(properties,tz,wwa):
    """
    For a Given Warning/Watch/Advisory,
    gets the stop and start time as useful objects in local time. 
    """
    start_d=datetime.datetime.strptime(properties['INIT_ISS'],'%Y%m%d%H%M')
    end_d=datetime.datetime.strptime(properties['EXPIRED'],'%Y%m%d%H%M')
    from_zone=dateutil.tz.gettz('UTC')
    to_zone=dateutil.tz.gettz(tz)
    utcStart=start_d.replace(tzinfo=from_zone)
    utcEnd=end_d.replace(tzinfo=from_zone)
    localStart=utcStart.astimezone(to_zone)
    localEnd=utcEnd.astimezone(to_zone)
    wwa.start_time=localStart
    wwa.end_time=localEnd
#    return [localStart,localEnd]
#
def decodeType(ppList,properties,wwa):
    """
    Decode the type of WWA (Red Flag or Flood etc)
    """
    for i in range(len(ppList)):
        if ppList[i][0]==properties['TYPE']:
            wwa.cType=ppList[i][0]
            wwa.hType=ppList[i][1]

def decodeSig(sList,properties,wwa):
    """
    Decodes the Significance of the Alert (Warning Watch or Advisory)
    """
    for i in range(len(sList)):
        if sList[i][0]==properties['SIG']:
            wwa.cSig=sList[i][0]
            wwa.hSig=sList[i][1]

def decodeStatus(aaaList,properties,wwa):
    """
    Decodes the Status, new or old or cancelled or expired
    """
    for i in range(len(aaaList)):
        if aaaList[i][0]==properties['STATUS']:
            wwa.cStatus=aaaList[i][0]
            wwa.hStatus=aaaList[i][1]

def decodeRemainder(properties,wwa):
    """
    Decodes the WFO and GType which are mostly worthless but cool
    """
    wwa.wfo=properties['WFO']
    wwa.gtype=properties['GTYPE']
    wwa.ugc=properties['NWS_UGC']

def correctFW(wwa):
    """
    Fire Weather Warning is not what people call it! Red Flag Warning!
    """
    if wwa.hSig=='Warning' and wwa.hType=='Fire Weather':
        wwa.hType='Red Flag'
 
def parseWWA(properties,tz,print_opt):
    """
    Run Function for WWA
    """
    wwa=WWA()    
    
    with open(vtec_Path+pp,'rb') as f:
        reader=csv.reader(f)
        ppList=list(reader)

    with open(vtec_Path+s) as f:
        reader=csv.reader(f)
        sList=list(reader)
    
    with open(vtec_Path+aaa) as f:
        reader=csv.reader(f)
        aaaList=list(reader)

    try:
        getWarnTimes(properties,tz,wwa)
    except:
        print 'Problem With DATASET!'
        return
    decodeType(ppList,properties,wwa)
    decodeSig(sList,properties,wwa)
    decodeStatus(aaaList,properties,wwa)
    decodeRemainder(properties,wwa)
    correctFW(wwa)
    
    if print_opt==True:
        printWWA(wwa)
        
    return wwa










