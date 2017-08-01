# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:25:32 2017

@author: tanner

SENDS ALL ALERTS
"""

import smtplib
import sys
import base64
sys.path.insert(0,base64.b64decode('L2hvbWUvdWJ1bnR1L3NyYy90ZXN0Qm9uZFN0cmVldC8='))
import sys_codec

def sendEmailAlert(AlertB,To,subject,method):
    """
    Sends email/Text message to whoever requested it, Password is currently exposed O_o
    """
    if method!='BOTH' and method!='NONE': #send to EITHER email OR text
        # fi=open('/home/ubuntu/src/FWAS/dump/app.yml')
        # conf=yaml.load(fi)

        print "sending Alert",To,"..."
        fromaddr = str(sys_codec.openAndDecode()[0])
    
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, str(sys_codec.openAndDecode()[1]))
    
        # Send text message through SMS gateway of destination number
    
        messageA = "From: FWAS <fireweatheralert@gmail.com>\nTo: FWAS Client <"+str(To)+">\nSubject: FWAS: "+str(subject)+"\n\n"
    
        message=messageA+AlertB
    #    print message
    #    print type(message)
        try:
            server.sendmail( fromaddr, str(To), message )
        except:
            print 'SEND RECIPIENT IS NOT VALID!!!!!!!!!!!!'
            pass
    
        server.quit()
    if method=='BOTH': #send to text AND email
        for i in range(len(To)):
            # fi=open('/home/ubuntu/src/FWAS/dump/app.yml')
            # conf=yaml.load(fi)
        
            print "sending Alert To",To[i],'...'
            fromaddr = str(email)
        
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, str(pWord))
        
            # Send text message through SMS gateway of destination number
        
            messageA = "From: FWAS <fireweatheralert@gmail.com>\nTo: FWAS Client <"+str(To)+">\nSubject: FWAS: "+str(subject)+"\n\n"
        
            message=messageA+AlertB
        #    print message
        #    print type(message)
            try:
                server.sendmail( fromaddr, str(To[i]), message )
            except: 
                print 'Send Recipient is Not Valid!!!!'
                print 'O_o'
                pass
        
            server.quit()
    if method=='NONE':
        print 'No Valid Contact information provided...O_o'
        print 'Quitting...'
        return False

