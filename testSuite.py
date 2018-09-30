#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 08:35:41 2018

@author: tanner
"""
import getpass
import time

import nightlyTestOne as nto
import PATHFILE
from HRRR_Parse import getDataset,getDiskFiles

fp = PATHFILE.FWAS_PATHS()


if(getpass.getuser()=="tanner"):
    cfg_file = "/home/tanner/src/gitFWAS/FWAS/test_fwas/threshold-TEST.cfg"
    log_file = "/home/tanner/src/gitFWAS/FWAS/test_fwas/test_log.log"
else:
    cfg_file = "/home/ubuntu/src/FWAS/test_fwas/threshold-TEST.cfg"
    log_file = "/home/ubuntu/src/FWAS/test_fwas/test_log.log"

start=time.time()
dF=getDiskFiles()
dsList=[]
for i in range(len(dF)):
    ds=getDataset(i)
    dsList.append(ds)
dsList.sort()

test_result = False

try:
    nto.ascertainCfg(cfg_file)
    a = nto.runFWAS(dsList)
    print(a)
    if(len(a)>0):
        test_result=True
except:
    test_result=False
    pass

with open(log_file,"a") as f:
    fStr = str(int(time.time()))+" FWAS Nightly Test Result: "+str(test_result)+"\n"
    f.write(fStr)
    f.close()
