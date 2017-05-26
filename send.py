# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:25:32 2017

@author: tanner
"""

import smtplib
import yaml


def sendEmailAlert(AlertB,To,subject):
    """
    Sends email/Text message to whoever requested it, Password is currently exposed O_o
    """
    # fi=open('/home/ubuntu/src/FWAS/dump/app.yml')
    # conf=yaml.load(fi)
    email="fireweatheralert@gmail.com"
    pWord=""

    print "sending Alert..."
    fromaddr = str(email)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, str(pWord))

    # Send text message through SMS gateway of destination number

    messageA = "From: FWAS <barrifle@gmail.com>\nTo: FWAS Client <"+str(To)+">\nSubject: FWAS: "+str(subject)+"\n\n"

    message=messageA+AlertB
#    print message
#    print type(message)

    server.sendmail( fromaddr, str(To), message )

    server.quit()
