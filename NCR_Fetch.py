# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 11:06:14 2017

@author: tanner
"""

import glob
import urllib2

#stid='KLVX'
#ncrDir='/media/tanner/vol2/NCR/'
ncrDir='/home/ubuntu/fwas_data/NCR/'

def checkforGFW(sid,gfwStr):
    """
    Checks to see if we have a gfw for the station provided
    """
    val=False
    cZ=glob.glob(str(ncrDir+'*.gfw'))
#    print cZ
#    print ncrDir+gfwStr
    for i in range(len(cZ)):
        if cZ[i]==str(ncrDir+gfwStr):
            val=True
    return val

def fetchRadar(stid):
    """
    fetches the gif and possibly gfw from radar.weather.gov
    """
    #Need to Fetch both gif and gfw!
    baseurl='https://radar.weather.gov/ridge/RadarImg/NCR/'
    sid=stid[1:]
    endGif='_NCR_0.gif'
    endGfw='_NCR_0.gfw'
    gifName=ncrDir+sid+endGif
    gfwName=ncrDir+sid+endGfw
    URL=baseurl+str(sid)+endGif
    urlG=baseurl+str(sid)+endGfw
    
    print URL,urlG
#    print gifName,gfwName
    
    if checkforGFW(sid,sid+endGfw)==True:
        print 'gfw file for:',sid,'exists, downloading gif...'
        gifResponse=urllib2.urlopen(URL)
        output=open(gifName,'wb')
        output.write(gifResponse.read())
        output.close()
        return gifName
    
    if checkforGFW(sid,sid+endGfw)==False:
        print 'gfw file for:',sid,'does not exist, downloading gif,gfw...'
        gifResponse=urllib2.urlopen(URL)
        gfwResponse=urllib2.urlopen(urlG)
        output=open(gifName,'wb')
        gfwOut=open(gfwName,'wb')
        output.write(gifResponse.read())
        gfwOut.write(gfwResponse.read())
        output.close()
        gfwOut.close()
        return gifName
        

    
    

