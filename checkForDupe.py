#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:58:01 2017

@author: tanner

Checks for Duplicates, integrated into the GUI and not called as part of the FWAS
Backend
"""

import glob
import ConfigParser
import sys

#arg1='cell_Alert'
#arg2='fsweather1@usa.com'
#arg3='NaN'

arg1=str(sys.argv[1])
arg2=str(sys.argv[2])
arg3=str(sys.argv[3])

import PATHFILE
fp = PATHFILE.FWAS_PATHS()
adp = fp.get_alertDataPath()+"*.cfg"
cZ = glob.glob(adp)
#cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#cZ=glob.glob('/home/tanner/src/breezy/cfgLoc/*.cfg')

class basicInfo:
    """
    Class That describes the most essential contact info in an Alert
    """
    alert_name=''
    contact=''
    email=''
    phone=''


def readHeaderFiles(cfgLoc):
    """
    reads first part of config 
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

def checkForDuplicates(name_arg,email_arg,cell_arg):
    """
    checks to see if what the user provides in the FWAS UI is identical to a previous
    alert that they already created with their email/phone number.
    
    This is important because If two identical alerts exist, then they both will be deleted 
    if the user wants to delete an annoying alert.
    """
    hList=[]
    for i in range(len(cZ)):
        bI=basicInfo()
    #    hList.append(readHeaderFiles(cZ[i]))
        header=readHeaderFiles(cZ[i])
        bI.alert_name=header['alert_name']
        bI.email=header['email']
        bI.phone=header['phone']
        
        if header['email']=='NaN' and header['phone']!='NaN':
            #Cell Phone Only
            bI.contact=header['phone']
        if header['email']!='NaN' and header['phone']=='NaN':
            #email Only
            bI.contact=header['email']
        if header['email']!='NaN' and header['phone']!='NaN':
            bI.contact='both'
        
    #    print bI.contact
        hList.append(bI)  
    is_duplicate=False
    for i in range(len(hList)):
        if name_arg==hList[i].alert_name:        
            if email_arg==hList[i].email and cell_arg==hList[i].phone:
#                print 'Identical Both Alert'
                is_duplicate='TrueBoth'
            if email_arg==hList[i].email and cell_arg!=hList[i].phone:
#                print 'Identical Email Alert'
                is_duplicate='TrueEmail'
            if email_arg!=hList[i].email and cell_arg==hList[i].phone:
#                print 'Identical Phone Alert'
                is_duplicate='TruePhone'
#    return is_duplicate
    print is_duplicate
                                
#print arg1,arg2,arg3                

checkForDuplicates(arg1,arg2,arg3)
        


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
