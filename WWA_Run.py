# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:41:14 2017

@author: tanner

Simplifies code by unifying everything, also good for debugging.
"""

import WWA_Fetch
import WWA_Intersector
import WWA_Parse
import WWA_Alert

#WWA_Fetch.FetchWWA()
#tz='America/Denver'
#headerLib={'alert_name': 'standard_alert',
# 'alert_time': '2017-07-17 16:29:58',
# 'carrier': 'mms.att.net',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '46.92',
# 'limit': '0',
# 'longitude': '-114.1',
# 'phone': '4062742109',
# 'radius': '50',
# 'time_zone': '2'}
#headerLib={'alert_name': 'standard_alert',
# 'alert_time': '2017-07-17 16:29:58',
# 'carrier': 'mms.att.net',
# 'email': 'fsweather1@usa.com',
# 'expires_after': '24',
# 'latitude': '29.9511',
# 'limit': '0',
# 'longitude': '-90.0715',
# 'phone': '4062742109',
# 'radius': '60',
# 'time_zone': '2'}

#dat=WWA_Intersector.findIntersections(headerLib,tz,False,True)
#alert=WWA_Alert.createAlert(dat,headerLib,tz)
#print alert

def runWWA(headerLib,tz,plot,optPrint):
    """
    Runs regular WWA called from WWA_One.py
    """
#    WWA_Fetch.FetchWWA()
    dat=WWA_Intersector.findIntersections(headerLib,tz,plot,optPrint)
    alert=WWA_Alert.createAlert(dat,headerLib,tz)
    return alert

def runInitialWWA(headerLib,tz,plot,optPrint):
    """
    Initial Run, called by instantAlert.py
    """
#    WWA_Fetch.FetchWWA()
    dat=WWA_Intersector.findIntersections(headerLib,tz,plot,optPrint)
    alert=WWA_Alert.createAlert(dat,headerLib,tz)
    return alert
    
    
    
    
    
    
    
    
    
    