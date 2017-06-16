# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:05:55 2017

@author: tanner
"""

import mwlatest
import ConfigParser
import station
from geopy.distance import great_circle
import math
import datetime
import dateutil
#import send
#import raws
import pint

#timeInt=2

def convertTimeZone(timeInt):
    """
    converts Number from Shiny App to Time Zone STring
    """
    validTimes=[1,2,3,4,5]
    validStringTimes=['America/Los_Angeles','America/Denver','US/Arizona','America/Chicago','America/New_York']
    timeString=''  
    for i in range(len(validTimes)):
        if timeInt==validTimes[i]:
            timeString=validStringTimes[i]
    return timeString

#A=convertTimeZone(timeInt)
#print A

def calcExpirationDate(start,dur):
    """
    uses datetime library to add alert duration to when the alert started
    """
    startObj=datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
    dObj=datetime.timedelta(hours=int(dur))
    expObj=startObj+dObj
    return expObj
