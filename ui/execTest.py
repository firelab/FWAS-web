#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:22:25 2017

@author: tanner
"""

import time
import datetime
import sys
import dateutil
import dateutil.tz

print "This is script is executable!"

fout=open("/home/tanner/src/FWAS/ui/test.txt","w")
fout.write("this script is executable!\n")
fout.write(str(time.time()))
fout.write("\n")
fout.write(str(datetime.datetime.now()))
fout.close()
#
argFile=str(sys.argv[1])
print argFile

from_zone=dateutil.tz.gettz('UTC')
print from_zone
