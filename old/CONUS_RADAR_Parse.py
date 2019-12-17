# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 14:25:44 2017

@author: tanner
"""

import gdal

import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import numpy
import Image
import csv
import calcDist
import geopy

#location=[30.394226,-86.487741] #Destin FL
#location=[34.813119,-87.659985] #Florence AL
#location=[35.017959,-85.321779] #Chattanooga TN
#location=[34.710064,-86.601078] #Huntsville AL
#location=[33.203321,-87.566494] #Tuscaloosa AL
#location=[46.918049,-114.091620] #Missoula MT
#location=[38.886183,-94.365780] #Kansas City/Pleasant Hill
#location=[30.6945,-880.399] #Mobile AL
#radius=12

#hDir='/media/tanner/vol2/CONUS_RADAR/'
hDir='/home/ubuntu/fwas_data/CONUS_RADAR/'

gifName=hDir+'conus_radar.gif'
rTime=hDir+'rTimes.txt'

def openDataset(dsPath):
    """
    Opens a a gif with its gfw which makes it something GDAL can read and parse!
    """
    ds=gdal.Open(dsPath)
    return ds

def projToPix(ds,coords):
    """
    Takes coordinate system NAD83/WGS84 (very similar) and turns it into pixels
    needs GDAL
    
    Note that these are floating point numbers, not integers. Some Image parsers
    will get pissed...
    """
    x=coords[1]
    y=coords[0]
    gt=ds.GetGeoTransform()
    px=float((x-gt[0])/gt[1])
    py=float((y-gt[3])/gt[5])
    return[px,py]

def pixToProj(ds,pLoc):
    """
    Turns a Pixel into its nearest Lat/Lon coordinate. This works pretty well
    if they are floats and not ints
    """
    gt=ds.GetGeoTransform()
    lon=pLoc[0]*gt[1]+gt[0]
    lat=pLoc[1]*gt[5]+gt[3]
    return [lat,lon]

def getRadarCodes():
    """
    Radar Codes are essentially just RGB colors that indicate weather severity
    This fetches and parses them
    """
    cCol=[]
    rN=[]
#    cFile='/media/tanner/vol2/NCR/colors.csv'
    cFile='/home/ubuntu/src/FWAS/data/colors.csv'
    with open(cFile,'rb') as f:
        reader=csv.reader(f)
        cList=list(reader)
    cA=numpy.array(cList,dtype=int)
    for i in range(len(cA)):
        cCol.append(cA[i][1:])
        rN.append(cA[i][0])
    return [cCol,rN]

def openImage(iLoc):
    """
    opens the gif with the python image library
    """
    img=Image.open(iLoc)
    return img
    
def checkColors(img,cCol,rN,threshold):
    """
    Checks all available colors in the image to see if any exceed the threshold
    """
    bigVal=[]
#    threshold=30.0 #This is where we set the threshold! (not anymore)
    pix=img.load()
    col=img.convert('RGB')    
    
    pCol=img.getcolors()
    lCol=col.getcolors()
    lCol.sort()

#    checkRadar
    for i in range(len(lCol)):
        for j in range(len(cCol)):
            if all(cCol[j]==lCol[i][1]):
                if rN[j]>=threshold:                
                    print True,j,i,rN[j]
                    bigVal.append([rN[j],j,i])
    return bigVal   
    
def plotRadar(iLoc,img,plotColor,colorData,yLoc,zoom,buff):
    """
    This plots the radar, it isn't used except for debugging
    """
    pyplot.figure(0)
    pyplot.title('CONUS Base RADAR')
    pCol=img.getcolors()
    im2=mpimg.imread(iLoc)
    pix=img.load()
    pyplot.imshow(im2)
    pyplot.xlim(0,len(im2[0]))
    pyplot.ylim(0,len(im2))
    
    X=[]
    Y=[]
    if plotColor==True:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pix[i,j]==pCol[colorData][1]:
                    X.append(i)
                    Y.append(j)
    pyplot.gca().invert_yaxis()
    pyplot.plot(yLoc[0],yLoc[1],'mo')
    pyplot.plot(X,Y,'ro')
    pyplot.hlines(yLoc[1],0,len(im2[0]))
    pyplot.vlines(yLoc[0],0,len(im2))

#    buff=100    
    
#    print yLoc[1]-buff
#    print yLoc[0]-buff
#
#    print yLoc[1]+buff
#    print yLoc[0]+buff     
    
    if zoom==True:
        pyplot.title('CONUS Base RADAR w/Zoom on Buffer')
        pyplot.ylim((yLoc[1]-buff),(yLoc[1]+buff))
        pyplot.xlim((yLoc[0]-buff),(yLoc[0]+buff))
        pyplot.gca().invert_yaxis()
    
def calcBuffer(origin,boundary):
    """
    Creates a Buffer around the specified location
    """
    origin=numpy.array(origin)
    boundary=numpy.array(boundary)
    ob=origin-boundary
    bDist=numpy.linalg.norm(ob)
    return bDist
    


def getPointBuffer(loc,radius):
    """
    Creates the Radius
    """
    origin=geopy.Point(loc[0],loc[1])
    newPt=geopy.distance.VincentyDistance(miles=int(radius)).destination(origin,180)
    return newPt

def getBufferRegion(pLoc,buff):
    """
    Math for buffer
    """
#    buff=100 # For no good reason
    
    bA=pLoc[0]-buff
    bB=pLoc[1]-buff
    bC=pLoc[0]+buff
    bD=pLoc[1]+buff
    return [int(bA),int(bB),int(bC),int(bD)]

def createRadiusBuffer(dataset,pLoc,location,radius):
    """
    Pulls all of the above functions together to create a buffer
    """
    print 'Creating',radius,'mile buffer...'
    point=getPointBuffer(location,radius)
    pPoint=projToPix(dataset,[point[0],point[1]])
    bRad=calcBuffer(pLoc,pPoint)
    print radius,'miles equals',round(bRad,1),'in Proj...'
    aOF=getBufferRegion(pLoc,bRad)
    return [bRad,aOF]


def plotAreaOfInterest(region,img,buff):
    """
    Localized Plotter to make sure that we are in the right area
    """
    pyplot.figure(1)
    pyplot.title('RADAR AREA OF INTEREST')
    ix2=img.crop((region[0],region[1],region[2],region[3]))
    pyplot.imshow(ix2)
    pyplot.hlines(buff,0,buff)
    pyplot.vlines(buff,0,buff)
    
    pyplot.ylim(0,buff*2)
    pyplot.xlim(0,buff*2)
    pyplot.gca().invert_yaxis()

#    pyplot.plot(buff,buff,'mo')

def getRadarSubset(img,region):
    """
    Crops big image for additional checks and makes it less resource intensive
    """
    ix2=img.crop((region[0],region[1],region[2],region[3]))
    return ix2

def getClosestPixel(img,colorData,dataset,location,aOF):
    """
    Based on colors, finds the closest pixel that exceeds the threshold
    """
    pCol=img.getcolors()
    pCol.sort()
    pix=img.load()
    gDist=[]
    gSpatial=[]
    
    XY=[]
    UV=[]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j]==pCol[colorData][1]:
                ei=i+aOF[0]
                ej=j+aOF[1]
                ll=pixToProj(dataset,[ei,ej])
                dist=calcDist.getSpatial(location,ll)
                gDist.append(dist[0])
                gSpatial.append(dist)
                XY.append([i,j])
                UV.append([ei,ej])
    gDist=numpy.array(gDist)
#    print gSpatial[gDist.argmin()]
    return [gSpatial[gDist.argmin()],XY[gDist.argmin()],UV[gDist.argmin()]]

def checkRadarLevels(img,colors,dataset,location,radius,aOF):
    """
    Checks various radar levels starting at highest and working its way down
    """
    for i in range(len(colors)):
        print 'checking radar Level: ', colors[i][0]
        cVal=getClosestPixel(img,colors[i][2],dataset,location,aOF)
        if cVal[0][0]<float(radius):
            print 'storm within range! <3...(',str(cVal[0][0]),')'
            return  [cVal,colors[i][0]]
#            print 'nearest point: ',cVal
        else:    
            print 'storm too far away O_o...('+str(cVal[0][0])+')'
            print 'checking next level...'
            continue

def runRadarCheck(location,radius,plot_on,threshold):
    """
    Master Run Function, does checks to make sure data is good and sorted
    Also will double radius, if the radius is smaller than 45 miles to make
    sure no storms are lurking just outside of the users area
    """

#    threshold=30.0
    
    dsLoc=gifName
    dataset=openDataset(dsLoc)
    pLoc=projToPix(dataset,location)
    cCol,rN=getRadarCodes()
    img=openImage(dsLoc)
    """
    First Try
    """
    print 'Checking Within Radius',radius,'miles...'
    buff,aOF=createRadiusBuffer(dataset,pLoc,location,radius)
    img2=getRadarSubset(img,aOF)
    cVars=checkColors(img2,cCol,rN,threshold)
    cVars.sort(reverse=True)
    A=checkRadarLevels(img2,cVars,dataset,location,radius,aOF)
    
    if A==None and radius<45: #Double the radius just to be sure...
        print 'Nothing in Initial Radius Worth Reporting...'
        print 'Checking Double Initial Radius',radius*2,'miles...'
        buff,aOF=createRadiusBuffer(dataset,pLoc,location,radius*2)
        img2=getRadarSubset(img,aOF)
        cVars=checkColors(img2,cCol,rN,threshold)
        cVars.sort(reverse=True)
        A=checkRadarLevels(img2,cVars,dataset,location,radius*2,aOF)
    if plot_on==True and A!=None:
#        if A!=None:
            print 'plotting...'
#            pyplot.figure(0)
            plotRadar(dsLoc,img,False,0,pLoc,True,buff)
            pyplot.plot(A[0][2][0],A[0][2][1],'ro')
#            pyplot.figure(1)
            plotAreaOfInterest(aOF,img,buff)
            pyplot.plot(A[0][1][0],A[0][1][1],'ro')
    if A==None:
        print 'Nothing Found on Base Reflectivity...'
        A=[]
        return A
    else:
        return [A[0][0],A[1]]
#        return A

#A=runRadarCheck(location,radius,True)

"""
Keep This stuff in case of bugs
"""

#dataset=openDataset(gifName)
##
#pLoc=projToPix(dataset,location)
#cCol,rN=getRadarCodes()
#img=openImage(gifName)
#threshold=30
##
###a=getPointBuffer(location,100)
###oLoc=projToPix(dataset,[a[0],a[1]])
###buff=calcBuffer(pLoc,oLoc)
##
#buff,aOF=createRadiusBuffer(dataset,pLoc,location,radius)
##
###buff=100
##
##
#png=getRadarSubset(img,aOF)
#
#cVars=checkColors(png,cCol,rN,threshold)
#cVars.sort(reverse=True)
#
#cVal=getClosestPixel(png,cVars[0][2],dataset,location)

#colorData=cVars[0][2]

#pCol=png.getcolors()
#pCol.sort()
#pix=png.load()
#gDist=[]
#gSpatial=[]
#XY=[]
#UV=[]
#for i in range(png.size[0]):
#    for j in range(png.size[1]):
#        if pix[i,j]==pCol[colorData][1]:
##        if pix[i,j]==pCol[1][1]:
#            ei=i+aOF[0]
#            ej=j+aOF[1]
#            ll=pixToProj(dataset,[ei,ej])
#            dist=calcDist.getSpatial(location,ll)
#            gDist.append(dist[0])
#            gSpatial.append(dist)
#            XY.append([i,j])
#            UV.append([ei,ej])
#gDist=numpy.array(gDist)

            
#XY=numpy.array(XY)
#XY=XY+[aOF[0],aOF[1]]
#pyplot.plot(XY[:,0:1],XY[:,1:],'ro')
#gDist=numpy.array(gDist)

#plotRadar(gifName,img,False,0,pLoc,True,buff)
#UV=numpy.array(UV)
#pyplot.plot(UV[:,0:1],UV[:,1:],'ro')
#plotAreaOfInterest(aOF,img,buff)
#XY=numpy.array(XY)
#pyplot.plot(XY[:,0:1],XY[:,1:],'ro')




#pyplot.figure(3)
#ix2=img.crop((aOF[0],aOF[1],aOF[2],aOF[3]))
#pyplot.imshow(ix2)

#lCol=png.convert('RGB').getcolors()
    
    
    
    
    