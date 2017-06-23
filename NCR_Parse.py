# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 14:57:21 2017

@author: tanner
"""

import gdal

import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import numpy
import Image
import csv
import calcDist


#location=[30.394226,-86.487741] #Destin FL
#location=[34.813119,-87.659985] #Florence AL
#location=[35.017959,-85.321779] #Chattanooga TN
#location=[34.710064,-86.601078] #Huntsville AL
#location=[33.203321,-87.566494] #Tuscaloosa AL
#radius=12

#dsLoc='/media/tanner/vol2/NCR/HTX_NCR_0.gif'

def openDataset(dsPath):
    ds=gdal.Open(dsPath)
    return ds

def projToPix(ds,coords):
    x=coords[1]
    y=coords[0]
    gt=ds.GetGeoTransform()
    px=float((x-gt[0])/gt[1])
    py=float((y-gt[3])/gt[5])
    return[px,py]

def pixToProj(ds,pLoc):
    gt=ds.GetGeoTransform()
    lon=pLoc[0]*gt[1]+gt[0]
    lat=pLoc[1]*gt[5]+gt[3]
    return [lat,lon]

def getRadarCodes():
    cCol=[]
    rN=[]
    cFile='/media/tanner/vol2/NCR/colors.csv'
    with open(cFile,'rb') as f:
        reader=csv.reader(f)
        cList=list(reader)
    cA=numpy.array(cList,dtype=int)
    for i in range(len(cA)):
        cCol.append(cA[i][1:])
        rN.append(cA[i][0])
    return [cCol,rN]
    
def openImage(iLoc):
    img=Image.open(iLoc)
    return img

def checkColors(img,cCol,rN):
    bigVal=[]
    threshold=30.0 #This is where we set the threshold!
    pix=img.load()
    col=img.convert('RGB')    
    
    pCol=img.getcolors()
    lCol=col.getcolors()
#    checkRadar
    for i in range(len(lCol)):
        for j in range(len(cCol)):
            if all(cCol[j]==lCol[i][1]):
                if rN[j]>=threshold:                
                    print True,j,i,rN[j]
                    bigVal.append([rN[j],j,i])
    return bigVal
    
def plotRadar(iLoc,img,plotColor,colorData):
    pCol=img.getcolors()
    im2=mpimg.imread(iLoc)
    pix=img.load()
    pyplot.imshow(im2)
    pyplot.xlim(0,600)
    pyplot.ylim(0,550)
    
    X=[]
    Y=[]
    if plotColor==True:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pix[i,j]==pCol[colorData][1]:
                    X.append(i)
                    Y.append(j)
    pyplot.gca().invert_yaxis()
    pyplot.plot(X,Y,'ro')
    pyplot.hlines(275,0,600)
    pyplot.vlines(300,0,600)
    
def getClosestPixel(img,colorData,dataset,location):
    pCol=img.getcolors()
    pix=img.load()
    gDist=[]
    gSpatial=[]

    XY=[]   
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pix[i,j]==pCol[colorData][1]:
                ll=pixToProj(dataset,[i,j])
                dist=calcDist.getSpatial(location,ll)
#                print dist                
                gDist.append(dist[0])
                gSpatial.append(dist)
                XY.append([i,j])
    gDist=numpy.array(gDist)
#    print gSpatial[gDist.argmin()]
    return [gSpatial[gDist.argmin()],XY[gDist.argmin()]]
#                X.append(i)
#                Y.append(j)

def checkRadarLevels(img,colors,dataset,location,radius):
    for i in range(len(colors)):
        print 'checking storm Level: ', colors[i][0]
        cVal=getClosestPixel(img,colors[i][2],dataset,location)
        if cVal[0][0]<float(radius):
            print 'storm within range! <3...(',str(cVal[0][0]),')'
            return  [cVal,colors[i][0]]
#            print 'nearest point: ',cVal
        else:    
            print 'storm too far away O_o...('+str(cVal[0][0])+')'
            print 'checking next level...'
            continue
#            print 'too far away: ',cVal
    
def runRadarCheck(dsLoc,location,radius,plot_on):           
    dataset=openDataset(dsLoc)
    pLoc=projToPix(dataset,location)
    cCol,rN=getRadarCodes()
    img=openImage(dsLoc)
#    pCol=img.getcolors()
    cVars=checkColors(img,cCol,rN)
    cVars.sort(reverse=True)    
    

    A=checkRadarLevels(img,cVars,dataset,location,radius)
    if A==None and radius<45: 
    #double radius if nothing is found Just to be Sure....
        A=checkRadarLevels(img,cVars,dataset,location,radius*2)
        
    if plot_on==True:
        plotRadar(dsLoc,img,False,0)
        pyplot.plot(pLoc[0],pLoc[1],'ro')
        if A!=None:
            pyplot.plot(A[0][1][0],A[0][1][1],'ko')
    if A==None:
        A=[]
        return A
    else:
        return [A[0][0],A[1]]


#A=runRadarCheck(dsLoc,location,radius,False)





































