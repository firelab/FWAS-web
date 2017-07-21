# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:45:18 2017

@author: tanner
"""

baseDir='/media/tanner/vol2/WWA/'
stateDir='states.csv'
zoneDir='alert_zones/'
countyDir='alert_counties/'

#import datetime
#import WWA_Intersector
#import WWA_Parse
import csv

#tz='America/New York'
#headerLib={'alert_name': 'standard_alert',
# 'alert_time': '2017-07-17 16:29:58',
# 'carrier': 'mms.att.net',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '37.7703',
# 'limit': '0',
# 'longitude': '-111.6021',
# 'phone': '4062742109',
# 'radius': '50',
# 'time_zone': '2'}
#headerLib={'alert_name': 'standard_alert',
# 'alert_time': '2017-07-17 16:29:58',
# 'carrier': 'mms.att.net',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '30.7490',
# 'limit': '0',
# 'longitude': '-84.3880',
# 'phone': '4062742109',
# 'radius': '10',
# 'time_zone': '2'}
##dat=WWA_Intersector.findIntersections(headerLib,tz,False,True)

#print '-------------'

def createHead(headerLib,tz):
    head="THE FOLLOWING WATCHES WARNINGS AND ADVISORIES ARE IN EFFECT FOR YOUR AREA\n"+\
    "All observations were taken within a "+headerLib['radius']+\
    " mile radius of your location. All times are: "+tz+".\n\n"
    return head


#def getLocation(dat):

def createLine(dat,region):
    line='A '+dat.hType+' '+dat.hSig+' issued by: '+dat.wfo+' is in effect'+\
    ' from '+dat.start_time.strftime('%I:%M %p %m-%d-%Y')+\
    ' until '+dat.end_time.strftime('%I:%M %p %m-%d-%Y')+\
    ' for the '+region+' area.\n'
    return line

#for i in range(len(dat)):
#    WWA_Parse.printWWA(dat[i])

def createBody(dat):
    print 'Creating Body of Alerts...'
    sData=[]
    for i in range(len(dat)):
        if dat[i]==None:
            continue
        if dat[i].ugc==None:
            continue
            
        zLoc=dat[i].ugc[2]
        #zLoc='C'
        sLoc=dat[i].ugc[:2]
        
#        state=['']
        path=['']
        if zLoc=='Z':
            path[0]=baseDir+zoneDir+sLoc+'.tsv'
        if zLoc=='C':
            path[0]=baseDir+countyDir+sLoc+'.tsv'
        
        
        with open(path[0],'rb') as f:
            reader=csv.reader(f,delimiter='\t') #Its a TSV not CSV!
            zList=list(reader)
            
        zone=[]
        
        for j in range(len(zList)):
            zList[j][1]=zList[j][1].translate(None,' ')
            if zList[j][1]==dat[i].ugc:
                zone.append(zList[j])
        #        print zList[i]
            
        sLine=createLine(dat[i],zone[0][2])
        sData.append(sLine)
    #    print createLine(dat[0],zone[0][2])
    return sData
        
    
def createAlert(dat,headerLib,tz):
    print 'Creating WWA Alert...'
#    dat=WWA_Intersector.findIntersections(headerLib,tz,False,True)
    sBody=createBody(dat)
    if len(sBody)==0:
        print 'No Alerts in Area...'
        return ''
    head=createHead(headerLib,tz)
    sBody=''.join(sBody)
    return head+sBody
#    print sBody

#createAlert(headerLib,tz)













    