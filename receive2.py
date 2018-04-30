# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 10:43:49 2017

@author: tanner
"""

import sys
import imaplib
import email
import datetime
import glob
import ConfigParser

cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')

M = imaplib.IMAP4_SSL('imap.gmail.com')

M.login('fireweatheralert@gmail.com', 'dahomeybenin')

#rv, mailboxes = M.list()
#if rv == 'OK':
#    print "Mailboxes:"
#    print mailboxes

rv,data=M.select("INBOX")
rv,lData=M.search(None,"ALL")

datList=lData[0].split()
datList=[int(x) for x in datList]


mStr=M.fetch(75,'(RFC822)')

msg=email.message_from_string(mStr[1][0][1])
sendFrom=msg['From']
#sendBody=msg.get_payload(decode=True)
#print sendFrom

val='stop'

a=sendFrom.find(':')
b=sendFrom.find('@')
c=len(sendFrom)
d=sendFrom.find('<')
e=sendFrom.find('>')

if d==-1 and e==-1:
    print 'Text Message'
    #Text Message
#    print sendFrom
    print sendFrom[:b]
    msg_body=msg.get_payload(i=0) #We Can't Decode Text messages without summoning demons... So instead we manually parse it!
    msg_body=str(msg_body)
    valLoc=msg_body.find(val)
    if valLoc==-1:
        print 'Trying capitalization...'
        valLoc=msg_body.find(val.capitalize())
    print valLoc
    print msg_body[valLoc:valLoc+len(val)]
        
else:
    print 'Email'
    #email
    print sendFrom[d+1:e]
    msg_body=msg.get_payload(decode=True)
#    print msg_body
    valLoc=msg_body.find(val)
    if valLoc==-1:
        print 'Trying capitalization...'
        valLoc=msg_body.find(val.capitalize())
    print valLoc
    print msg_body[valLoc:valLoc+len(val)]


#cZ=glob.glob('/home/tanner/src/breezy/fwas/data/*.cfg')

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


headLib=readHeaderFiles(cZ)
























