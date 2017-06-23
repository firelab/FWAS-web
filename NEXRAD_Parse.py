# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:04:44 2017

@author: tanner
"""

import matplotlib.pyplot as pyplot
import numpy.ma as ma
import pyart.graph #NOTE: HAD TO BUILD FROM SOURCE DUE TO DOGSHIT
import pyart.io
import numpy
import glob

import calcDist
import NEXRAD_radarStation

def getDiskFile():
    dZ=glob.glob('/media/tanner/vol2/NEXRAD/*')
    return dZ

def readRadar(diskFile):
    radar=pyart.io.read_nexrad_archive(diskFile)
    return radar

def getReflectivityPlot(radar):
    plots = [
    # variable-name in pyart, display-name that we want, sweep-number of radar (0=lowest ref, 1=lowest velocity)
    ['reflectivity', 'Reflectivity (dBZ)', 0],
    ['differential_reflectivity', 'Zdr (dB)', 0],
    ['differential_phase', 'Phi_DP (deg)', 0],
    ['cross_correlation_ratio', 'Rho_HV', 0],
    ['velocity', 'Velocity (m/s)', 1],
    ['spectrum_width', 'Spectrum Width', 1]
    ]
    
    refl_grid = radar.get_field(0, 'reflectivity')
    return refl_grid

def ParseNEXRADTime(time):
    date=time[14:24]
    utcTime=time[25:33]

    return [date,utcTime]

def organizeData(radarInfo,radar,threshold):
    s1=NEXRAD_radarStation.radarStation()
    s1.radar_lat=radar.latitude['data'][0]
    s1.radar_lon=radar.longitude['data'][0]
    
    s1.gate_lat=radar.gate_latitude['data'][radarInfo[2][0]][radarInfo[2][1]]
    s1.gate_lon=radar.gate_longitude['data'][radarInfo[2][0]][radarInfo[2][1]]
    s1.gate_dist=radarInfo[0][0]
    s1.gate_bearing=radarInfo[0][1]
    s1.gate_cardinal=radarInfo[0][2]
    s1.gate_val=radarInfo[1]
    s1.gate_thresh=threshold
    s1.date,s1.time=ParseNEXRADTime(radar.time['units'])
    s1.is_empty=False
    s1.check=True
    return s1

def calcNearestPixel(refl_grid,radar,your_location):
    threshold=30.0 #HARD SET HERE
#    rLat=radar.latitude['data'][0]
#    rLon=radar.longitude['data'][0]
    
    yLat=float(your_location[0])
    yLon=float(your_location[1])
    
    exceed=numpy.where(refl_grid>threshold)
    pEx=numpy.array([exceed[0],exceed[1]])
    
    if exceed[0].size==0:
        rStation=NEXRAD_radarStation.radarStation()
        return rStation
        
    else:
        dists=[]
        dInfo=[]
    
        for i in range(len(pEx[0])):
            mLat=radar.gate_latitude['data'][pEx[0][i]][pEx[1][i]]
            mLon=radar.gate_longitude['data'][pEx[0][i]][pEx[1][i]]
            nA=calcDist.getSpatial([yLat,yLon],[mLat,mLon])
            dists.append(nA[0])
            dInfo.append(calcDist.getSpatial([yLat,yLon],[mLat,mLon]))
        dists=numpy.array(dists)
        
        localMin=dists.argmin()
        pix=[pEx[0][localMin],pEx[1][localMin]]
        nInfo=[dInfo[localMin],refl_grid[pEx[0][localMin]][pEx[1][localMin]],pix]
        
        rStation=organizeData(nInfo,radar,threshold)
        del dists,dInfo,pEx,exceed,nInfo
        return rStation
    
    
    
#    del dists,dInfo,pEx,exceed
#    return nInfo

def plotRadar(radar,refl_grid,pix,exceed,general,qualityControl):
    qced = radar.extract_sweeps([0])

    hField=numpy.zeros(refl_grid.shape)
    hField[pix[0]-15:pix[0]+15,pix[1]-15:pix[1]+15]=60  
    qced.add_field_like('reflectivity','h',hField)

    
    display = pyart.graph.RadarDisplay(qced)
    
    pyplot.figure(1)
    if exceed==True:
        display.plot('h',cmap='pyart_NWSRef')
        display.plot_cross_hair(500)
        display.plot_range_rings(range(100, 350, 100), lw=0.5, col='black')
        #display.plot_range_ring(10,lw=1)
        display.plot_range_rings(range(10,50,10),lw=1)
        #display.set_limits((-300, 300), (-300, 300))
        display.set_limits((-50,50),(-50,50))
        display.set_aspect_ratio('equal')
        #display.plot_label('Base',(rLat,rLon))
        #display.plot_label('MaxLoc',(mLat,mLon))
        pyplot.xticks(numpy.arange(-40,50,10))
        pyplot.yticks(numpy.arange(-40,50,10))
        pyplot.grid()
    
    pyplot.figure(2)
    if general==True:         
        display.plot('reflectivity')
        display.plot_cross_hair(500)
        display.plot_range_rings(range(100, 350, 100), lw=0.5, col='black')
        display.plot_range_rings(range(10,50,10),lw=1)
        #display.plot_label('A',)
        #display.set_limits((-300, 300), (-300, 300))
        #display.set_limits((-150, 150), (-150, 150))
        display.set_limits((-50,50),(-50,50))
        display.set_aspect_ratio('equal')
    if qualityControl==True:
        print 'Quality Control is currently disabled pending testing...'



#test_loc=[42.25446,-75.977281]

#dF=getDiskFile()

def checkRadar(diskFile,viewStation,location):
    radar=readRadar(diskFile)
    grid=getReflectivityPlot(radar)
    rStation=calcNearestPixel(grid,radar,location)
    if viewStation==True:
        NEXRAD_radarStation.viewStation(rStation)
    return rStation




























