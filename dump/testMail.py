#!/usr/bin/env python

import smtplib

fromaddr = "wind.ninja.support@gmail.com"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "WindWizardSucks")

# Send text message through SMS gateway of destination number
server.sendmail( fromaddr, '4062412530@vtext.com', 'This is just a WindNinja messaging test.' )

server.quit()

