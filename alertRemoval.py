#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:51:01 2017

@author: tanner
"""

import platform
import imaplib
import email
import datetime
import glob
import ConfigParser
import os

print '==========================='
print 'Alert Removal System     '
print datetime.datetime.now()
print platform.system(),platform.release()
print '===========================\n'

cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#cZ=glob.glob('/home/tanner/src/breezy/cfgLoc/*.cfg')

def readHeaderFiles(cfgLoc):
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


M = imaplib.IMAP4_SSL('imap.gmail.com')
M.login('', '')

#rv, mailboxes = M.list()

rv,data=M.select("INBOX")
rv,lData=M.search(None,"ALL")

datList=lData[0].split()
datList=[int(x) for x in datList]
rm_cZ=[]
rm_em=[] 

#j=1
for j in datList:
#    i=0
    for i in range(len(cZ)):
        problems=[]
        mStr=M.fetch(j,'(RFC822)')
        
        msg=email.message_from_string(mStr[1][0][1])
        sendFrom=msg['From']
        #sendBody=msg.get_payload(decode=True)
        #print sendFrom
        
        hList=readHeaderFiles(cZ[i])
        
        hName=hList['alert_name']
        
        val='stop'
        
        tVal=val+' '+hName
        
        sendType=[0]    
        
        a=sendFrom.find(':') #????
        b=sendFrom.find('@') #Finds where the email is
        c=len(sendFrom)
        d=sendFrom.find('<') #These show up in Emails
        e=sendFrom.find('>') #But not text messages
        
        
#        print '--------------------------'
#        print 'Reading Message No: ',j
        if d==-1 and e==-1:
            send_id=sendFrom[:b]
            msg_body=msg.get_payload(i=0) #We Can't Decode Text messages without summoning demons... So instead we manually parse it!
            msg_body=str(msg_body)
            valLoc=msg_body.find((val+' '+hName))
            if valLoc==-1:
                valLoc=msg_body.find((val.capitalize()+' '+hName))
            sendType[0]=1
                
        else:
            send_id=sendFrom[d+1:e]
            msg_body=msg.get_payload(decode=True)
            valLoc=msg_body.find((val+' '+hName))
            if valLoc==-1:
                valLoc=msg_body.find((val.capitalize()+' '+hName))
            sendType[0]=0
        
        localContact=''
        
        if sendType[0]==0:
            if send_id==hList['email']:
                localContact=hList['email']
#                rm_cZ.append(cZ[i])
#                rm_em.append(j)
        if sendType[0]==1:
            if send_id==hList['phone']:
                localContact=hList['phone']
#                rm_cZ.append(cZ[i])
#                rm_em.append(j)
                
        if localContact!=send_id:
            problems.append('localContact!=send_id') #This prevents one users from deleting another users Alert         
       
        if valLoc!=-1 and not any(problems):
            print '---------------------------'
            print 'Reading Message No.',j
            print 'cfg File No.',i
            print sendType
            print 'sender:',send_id
            print 'cfg_contact:',localContact
            print 'stop loc:',valLoc
            print 'message:',msg_body[valLoc:valLoc+len(tVal)]
            print 'alert_name:',hList['alert_name']
            print cZ[i]
            
            rm_cZ.append(cZ[i])
            rm_em.append(j)
        localContact=''


#print '--------------------------'
print '==========================='

print '-=-=-=-=-=-=-=-=-=-=-=-=-=-'
print 'Emails & Alerts Slated for Removal'
print '-=-=-=-=-=-=-=-=-=-=-=-=-=-'
print rm_cZ
print rm_em
print '-=-=-=-=-=-=-=-=-=--=-=-=-=-'

check=len(rm_cZ)==len(rm_em)

if check==True:
    print 'Removal Lengths are equal'
    print check
    print 'rm_cZ,rm_em'
    print len(rm_cZ),len(rm_em)
if check==False:
    print 'Error, something has gone wrong with the removal system...'
    exit
    
if not any(rm_cZ) and not any(rm_em):
    print 'No Alerts Slated For Removal...'
    print 'Exiting'
    exit


for i in range(len(rm_cZ)):
    print 'Removing Alert:',rm_cZ[i]
    os.remove(rm_cZ[i])
    M.store(rm_em[i],'+X-GM-LABELS','\\Trash')



#set_em=list(set(rm_em))
