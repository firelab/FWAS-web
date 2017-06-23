#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 09:40:07 2017

@author: tanner

Instant Party!

This file runs when a run is created to establish communication with user
and give alert, SHOULD DO EVERY ALERT, RAWS HRRR ETC
"""

import one
import sys

print "Running FWAS instant!"

argFile=str(sys.argv[1])

one.ascertainCfg(argFile)
one.runInitialFWAS()
