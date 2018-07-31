# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:54:29 2018

@author: tanner

Create backup of thresholds for later data analysis
"""
import glob
import os
import shutil

import PATHFILE
fp = PATHFILE.FWAS_PATHS()

adp = fp.get_alertDataPath()
backup_directory = fp.get_thresholdArchivePath()

cZ = glob.glob(adp+"*.cfg")
#cZ=glob.glob('/srv/shiny-server/fwas/data/*.cfg')
#backup_directory='/home/ubuntu/fwas_data/threshold_archive/'

def backup_cfg():
    fName=[]
    fDir=[]
    for i in range(len(cZ)):
        sT=cZ[i].split("/")
        for part in sT:
            if part.find("threshold")>-1:
                fName.append(part)
                fDir.append(cZ[i])
        
        
    for i in range(len(fName)):
        checkName=backup_directory+fName[i]
        if not os.path.isfile(checkName):
            shutil.copyfile(fDir[i],checkName)
            print 'Backing Up', checkName
        else:
            print "File %s Already Exists" % checkName
            
            
