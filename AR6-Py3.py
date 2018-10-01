#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 17:18:08 2018

@author: tanner

Alert Removal System Version 6

This File Comports FWAS with Zawinski's Law:
Every program attempts to expand until it can read mail. 
Those programs which cannot so expand are replaced by ones which can.

Tested Platforms:
EMAIL
ATT

Untested Platforms:
Verizon
T-Mobile
Everything Else
"""

import platform
import datetime
import glob
import configparser as ConfigParser
import os
import base64
import sys
from bs4 import BeautifulSoup
import unicodedata

from email.message import EmailMessage
import smtplib

from imap_tools import MailBox
#
sys.path.insert(0,base64.b64decode('L2hvbWUvdWJ1bnR1L3NyYy90ZXN0Qm9uZFN0cmVldC8='))
import sys_codec

#alertPath = "/home/tanner/src/gitFWAS/alertRemoval2/cfg/*.cfg"
#cZ = glob.glob(alertPath)

import PATHFILE
fp = PATHFILE.FWAS_PATHS()
alertPath = fp.get_alertDataPath()+"*.cfg"
cZ = glob.glob(alertPath)

DELETE_ALERTS = True

def readHeaderFiles(cfgLoc):
    """
    reads first part of config file
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
    return headerDict

def determineSenderMethod(localContact,remoteContact):
    for i in range(len(localContact)):
        if(remoteContact==localContact[i]):
            return True,localContact[i]
        else:
            return False,'NONE'

def listSMSGateways():
    """
    provides a list of all SMS Gateways (Acutally we are using MMS due to message sizes)
    """    #MMS Gateways
    gate={'att':'mms.att.net',
    'verizon':'vzwpix.com',
    'tmobile':'tmomail.net',
    'virgin':'vmpix.com',
    'sprint':'pm.sprint.com',
    'boost':'myboostmobile.com',
    'uscellular':'mms.uscc.net',
    'metro':'mymetropcs.com',
    'cricket':'mms.cricketwireless.net',
    'projectfi':'msg.fi.google.com',
    'cellcom':'cellcom.quiktxt.com'}
    return gate

def getSMSGateway(carrier,gateways):
    """
    converts input from shiny to SMS Gateway
    """
    gateway=gateways[str(carrier)]
    return gateway

def configureNotifications(header):
    """
    Figures out email or text message
    """
    sendTo=''
    valid=listSMSGateways()
    if header['email']=='NaN' and header['carrier']!='NaN':
        gateway=getSMSGateway(header['carrier'],valid)
        sendTo=[header['phone']+'@'+gateway]
        sendMethod = ['phone']
    if header['phone']=='NaN' and header['email']!='NaN':
        sendTo=[header['email'].lower()]
        sendMethod = ['email']
    if header['phone']!='NaN' and header['email']!='NaN':
        gateway=getSMSGateway(header['carrier'],valid)
        sendTo=[str(header['phone']+'@'+gateway),header['email']]
        sendMethod = ['phone','email']
    if header['phone']=='NaN' and header['email']=='NaN':
        sendTo=['NONE']
        sendMethod = ['NONE']
    return sendTo,sendMethod

def sendEmail(sender,alertName):
    message = "Alert: "+str(alertName)+" successfully stopped!"
    
    msg = EmailMessage()
    msg['Subject'] = 'FWAS ALERT NOTIFICATION'
    msg['From'] = "FWAS <fireweatheralert@gmail.com>"
    msg['To'] = "<"+str(sender)+">"
    msg.preamble = "FWAS ALERT NOTIFICATION"
    msg.set_content(message)
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sys_codec.openAndDecode()[0], sys_codec.openAndDecode()[1]) 
    server.send_message(msg)
    return "CONFIRMATION SENT!"
    

def runAlertRemoval():
    LOGMSG = ''
    LOGMSG += 'FWAS Email Processor Version 6\n'
    LOGMSG += str(datetime.datetime.now())
    LOGMSG += str(platform.system())+"\n"
    LOGMSG += str(platform.release())+"\n"

    mailbox = MailBox('imap.gmail.com')
    mailbox.login(sys_codec.openAndDecode()[0], sys_codec.openAndDecode()[1]) 
    
    #Get All the messages in the mailbox
    messages = []
    for message in mailbox.fetch():
        messages.append(message)
    
    #Quick Cheks on The system
    if len(messages)==0:
        LOGMSG+= '\nNO EMAILS IN INBOX...\nExiting...'
#        print(LOGMSG)
        return LOGMSG
    if len(cZ)==0:
        LOGMSG+='\nNO ALERTS ON DISK...\nExiting...'
#        print(LOGMSG)
        return LOGMSG
    
    for i in range(len(messages)):
        for j in range(len(cZ)):
            try:
                mID = messages[i].id #Some sort of ID, not really important
                mUID = messages[i].uid # Important to delete
                mFrom_ = messages[i].from_.lower()# Sender of email/Alert Recipient
                mSubj = messages[i].subject # The Email Subject, may be blank
                mTo = messages[i].to #who it is to, usually fireweatheralert@gmail.com       
                
                LOGMSG+="\n---------------------------------\n"            
                LOGMSG+="READING MESSAGE: "+str(i)+"\n"     
                LOGMSG+="ID: "+mID+"\nUID: "+mUID+"\nFROM: "+mFrom_+"\nSUBJECT: "+mSubj+"\nTO: "+mTo[0]+"\n"
                LOGMSG+="---------------------------------\n"
    
                messageHTML = messages[i].html # Get the HTML version of the message
                messageSoup = BeautifulSoup(messageHTML,"lxml") #Convert to a bs4 obj
                messageText = messageSoup.text # Get as a string
                clean_messageText = unicodedata.normalize("NFKD",messageText)
    
                #Remove double spaces
                cmt = clean_messageText.strip()
                while '  ' in cmt:
                    cmt = cmt.replace('  ', ' ') 
                    
                cmt = cmt.lower() # Make everything lowercase
                
                localInfo = readHeaderFiles(cZ[j])
                localInfo['phone'] = localInfo['phone'].translate('()[] -.{}/') #Strip any crap out of the number          
                
                LOGMSG+="---------------------------------\n"
                LOGMSG+="LOOKING AT ALERT: "+str(j)+"\n"
                LOGMSG+="FILENAME: "+cZ[j]+"\n"
                LOGMSG+="NAME: "+localInfo['alert_name']+"\nPHONE: "+localInfo['phone']+"\nCARRIER: "
                LOGMSG+=localInfo['carrier']+"\nEMAIL: "+localInfo['email']+"\n"
                LOGMSG+="---------------------------------\n"
    
                #For Each Alert Get a Contact method, and the address 
                localContact,contactMethod = configureNotifications(localInfo)
                match,contactAddr = determineSenderMethod(localContact,mFrom_)
                
    
                if(contactAddr=='None' or match==False):
    #                print('Alert and Email Do Not Match\n')
                    LOGMSG+="\nLocal Information and Email Info Do Not Match for: "+str(i)+" and "+str(j)
                    LOGMSG+=" ENDING SEARCH FOR THIS MESSAGE AND ALERT COMBINATION...."
                    LOGMSG+="\n======================================================\n"
                    continue            
                            
                #Create a message to look for
                stopKeyword = 'stop'
                fullStopKwd = stopKeyword +' '+localInfo['alert_name']
                fullStopKwd = fullStopKwd.lower()
                stopLoc = cmt.find(fullStopKwd)
                if(stopLoc>-1):
                    LOGMSG+="\nFOUND STOP COMMAND AT: "+str(stopLoc)+ "\n"
                else:
                    LOGMSG+="\nNO STOP COMMAND FOUND!\n"
    
                if(DELETE_ALERTS==True):
                    if(stopLoc > -1):
                        LOGMSG+="DELETE_ALERTS = TRUE\n"
                        LOGMSG+="DELETING: "+cZ[i]+"\n"+"NAME: "+localInfo['alert_name']
                        LOGMSG+="\nFROM: "+contactAddr+"\n"
                        os.remove(cZ[i])
                        mailbox.move([mUID],"backup")
                        LOGMSG+=sendEmail(contactAddr,localInfo['alert_name'])
                        LOGMSG+="\n======================================================\n"
    
                else:
                    if(stopLoc > -1):
                        LOGMSG+="\nDelete Alerts is OFF, would delete if on\n"
                        LOGMSG+="\n======================================================\n" 
            except:
                LOGMSG+="ERROR AT "+str(i)+" "+str(j)+"\n"
                pass
            
    LOGMSG+="Processed Completed Sucessfully."
    return LOGMSG



alertLog = runAlertRemoval()
print(alertLog)











