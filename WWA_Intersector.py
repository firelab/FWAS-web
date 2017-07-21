# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 13:33:41 2017

@author: tanner
"""

import json
from shapely.wkt import loads
from shapely.geometry import Polygon, mapping
import matplotlib.pyplot as pyplot
import random
import geopy
from geopy.distance import great_circle
import WWA_Parse


fLoc='/media/tanner/vol2/WWA/current_ww/current.geojson'
#fLoc='/home/ubuntu/fwas_data/WWA/current_ww/current.geojson'

def getLoc(headerLib):
    loc=[]
    loc.append(float(headerLib['latitude']))
    loc.append(float(headerLib['longitude']))
    rad=float(headerLib['radius'])
    return loc,rad
    
def getPointBuffer(loc,radius,direction):
    origin=geopy.Point(loc[0],loc[1])
    newPt=geopy.distance.VincentyDistance(miles=int(radius)).destination(origin,int(direction))
    return newPt    
    
    
def findIntersections(headerLib,tz,plot_on,print_wwa):
    loc,rad=getLoc(headerLib)
    print 'Radius set to:',rad,'mi'
    print 'Location set:',loc
    #Build Polygon Based on Loc
    ptA=getPointBuffer(loc,rad,180)
    ptB=getPointBuffer(loc,rad,90)
    ptC=getPointBuffer(loc,rad,0)
    ptD=getPointBuffer(loc,rad,270)
    
    yA=[ptD[1],ptD[1],ptB[1],ptB[1],ptD[1]]
    yB=[ptA[0],ptC[0],ptC[0],ptA[0],ptA[0]]
    
    rCoords=zip(yA,yB)
    p1=Polygon(rCoords)

    fIn=open(fLoc)
    jLoad=json.load(fIn)
    
    prox_wwa=[]    
    
    print 'Checking:',len(jLoad['features']),'Watches,Warnings and Advisories...'
    for i in range(len(jLoad['features'])):
    #print jLoad['features'][i]['properties']
        jCoords=jLoad['features'][i]['geometry']['coordinates'][0]
        x=[row[0] for row in jCoords]
        y=[row[1] for row in jCoords]
           
        wCoords=zip(x,y)
        
        if len(wCoords)<=2:
            continue
        try:    
            p2=Polygon(wCoords)
        except:
            print 'Something Wrong with',i,'Ignoring...'
            continue
        a=p1.intersection(p2)
        
        if a:
            if a.wkt.find('MULTIPOLYGON')>-1:
                inter=a[0].exterior.coords.xy        
            else:
                inter=a.exterior.coords.xy
                
#            prox_wwa.append(jLoad['features'][i]['properties'])
            print 'Intersection @',i
            prox_prop=jLoad['features'][i]['properties']
            print 'Parsing Data for',i,'...'
            wwp=WWA_Parse.parseWWA(prox_prop,tz,print_wwa)
            if wwp!=None:
                prox_wwa.append(wwp)
            
            if plot_on==True:
                print 'Plotting',i,'...'
                pyplot.figure(i)
                title='i: '+str(i)+' TYPE: '+jLoad['features'][i]['properties']['TYPE']+' SIG: '+jLoad['features'][i]['properties']['SIG']
                pyplot.title(str(title))
                pyplot.plot(yA,yB,'g-')
                pyplot.plot(x,y,'r-')
                
                pyplot.fill(inter[0],inter[1],alpha=.5)
#                pyplot.plot(-114.1,46.92,'m*',markersize=10)
    
        if not a:
            continue
    print len(prox_wwa),'Intersections Found!'
    return prox_wwa
    
    
#locData=findIntersections(headerLib,tz,True,False)
    
#for i in range(len(locData)):
#    WWA_Parse.printWWA(locData[i])
    
    
    
    
    
    
    
    
    
    
    
    