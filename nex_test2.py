# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:35:58 2017

@author: tanner
"""
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
import numpy.ma as ma
import pyart.graph #NOTE: HAD TO BUILD FROM SOURCE DUE TO DOGSHIT
import pyart.io
import numpy

import glob

import calcDist

cZ=glob.glob('/media/tanner/vol2/NEXRAD/*')

radar = pyart.io.read_nexrad_archive(cZ[0])

#display = pyart.graph.RadarDisplay(radar)
#fig = plt.figure(figsize=(9, 12))
#
#
plots = [
    # variable-name in pyart, display-name that we want, sweep-number of radar (0=lowest ref, 1=lowest velocity)
    ['reflectivity', 'Reflectivity (dBZ)', 0],
    ['differential_reflectivity', 'Zdr (dB)', 0],
    ['differential_phase', 'Phi_DP (deg)', 0],
    ['cross_correlation_ratio', 'Rho_HV', 0],
    ['velocity', 'Velocity (m/s)', 1],
    ['spectrum_width', 'Spectrum Width', 1]
]

#def plot_radar_images(plots):
#    ncols = 2
#    nrows = len(plots)/2
#    for plotno, plot in enumerate(plots, start=1):
#        ax = fig.add_subplot(nrows, ncols, plotno)
#        display.plot(plot[0], plot[2], ax=ax, title=plot[1],
#             colorbar_label='',
#             axislabels=('East-West distance from radar (km)' if plotno == 6 else '', 
#                         'North-South distance from radar (km)' if plotno == 1 else ''))
#        display.set_limits((-300, 300), (-300, 300), ax=ax)
#        display.set_aspect_ratio('equal', ax=ax)
#        display.plot_range_rings(range(100, 350, 100), lw=0.5, col='black', ax=ax)
#    plt.show()
    
    
refl_grid = radar.get_field(0, 'reflectivity')
##print refl_grid[0]
#rhohv_grid = radar.get_field(0, 'cross_correlation_ratio')
#zdr_grid = radar.get_field(0, 'differential_reflectivity')
#
## apply rudimentary quality control
#reflow = np.less(refl_grid, 20)
#zdrhigh = np.greater(np.abs(zdr_grid), 2.3)
#rhohvlow = np.less(rhohv_grid, 0.95)
#notweather = np.logical_or(reflow, np.logical_or(zdrhigh, rhohvlow))
##print notweather[0]
#
#qcrefl_grid = ma.masked_where(notweather, refl_grid)
#
qced = radar.extract_sweeps([0])
#qced.add_field_like('reflectivity', 'reflectivityqc', qcrefl_grid)

###############
#Modifcations #
###############

#maxInRadar=refl_grid.max()
#locMax=numpy.unravel_index(refl_grid.argmax(),refl_grid.shape)
#locMax=(0,166)
hField=numpy.zeros(refl_grid.shape)
###hField[:]=0
#hField[locMax[0]-5:locMax[0]+5,locMax[1]-5:locMax[1]+5]=75
###hField[locMax[1]-10:locMax[1]+10]=75
#qced.add_field_like('reflectivity','h',hField)
#
rLat=radar.latitude['data'][0]
rLon=radar.longitude['data'][0]

#mLat=radar.gate_latitude['data'][locMax[0]][locMax[1]]
#mLon=radar.gate_longitude['data'][locMax[0]][locMax[1]]


thresh=30.0

exceed=numpy.where(refl_grid>thresh)
p=numpy.array([exceed[0],exceed[1]])
#i=1
a=[]
d=[]
for i in range(len(p[0])):
    mLat=radar.gate_latitude['data'][p[0][i]][p[1][i]]
    mLon=radar.gate_longitude['data'][p[0][i]][p[1][i]]
    nA=calcDist.getSpatial([rLat,rLon],[mLat,mLon])
    a.append(nA[0])
##    b.append(nA[1])
##    c.append(nA[2])
    d.append(calcDist.getSpatial([rLat,rLon],[mLat,mLon]))
a=numpy.array(a)
#print a.min()
#print a.argmin()
ska=a.argmin()
skaV=[d[ska],refl_grid[p[0][ska]][p[1][ska]]]
pix=[p[0][ska],p[1][ska]]
LL=[radar.gate_latitude['data'][p[0][ska]][p[1][ska]],radar.gate_longitude['data'][p[0][ska]][p[1][ska]]]
print skaV
print LL
print pix
del a,d,p,exceed

hField[pix[0]-15:pix[0]+15,pix[1]-15:pix[1]+15]=skaV[1]
qced.add_field_like('reflectivity','h',hField)

#####################
# End Modifications #
#####################

display = pyart.graph.RadarDisplay(qced)

plt.figure(1)
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


plt.figure(2)
display.plot('reflectivity')
display.plot_cross_hair(500)
display.plot_range_rings(range(100, 350, 100), lw=0.5, col='black')
display.plot_range_rings(range(10,50,10),lw=1)
#display.plot_label('A',)
#display.set_limits((-300, 300), (-300, 300))
#display.set_limits((-150, 150), (-150, 150))
display.set_limits((-50,50),(-50,50))
display.set_aspect_ratio('equal')

#plt.figure(3)
##pyplot.imshow(refl_grid,cmap='pyart_NWSRef')
#display.plot('reflectivityqc',cmap='pyart_NWSRef')
#display.plot_cross_hair(500)
#display.plot_range_rings(range(100, 350, 100), lw=0.5, col='black')
#display.plot_range_rings(range(10,50,10),lw=1)
###display.plot_label('A',)
##display.set_limits((-300, 300), (-300, 300))
#display.set_limits((-50,50),(-50,50))
#display.set_aspect_ratio('equal')

























