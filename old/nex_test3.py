# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:35:25 2017

@author: tanner
"""

import matplotlib.pyplot as pyplot
import matplotlib.image as mpimg
import numpy
import Image

import csv

import calcDist

cFile='/media/tanner/vol2/NCR/colors.csv'

with open(cFile,'rb') as f:
    reader=csv.reader(f)
    cList=list(reader)

cA=numpy.array(cList,dtype=int)
#cCol=numpy.array([])
cCol=[]
rN=[]

for i in range(len(cA)):
    cCol.append(cA[i][1:])
    rN.append(cA[i][0])

#iLoc='/media/tanner/vol2/NCR/MSX_NCR_0.gif'
iLoc='/media/tanner/vol2/NCR/EVX_NCR_0.gif'

img=mpimg.imread(iLoc)
I2=Image.open(iLoc)
col=I2.convert('RGB')

pix=I2.load()

pCol=I2.getcolors()
lCol=col.getcolors()

pCol.sort()
lCol.sort()

#a=numpy.array(lColors[-1][1])
#a=numpy.append(a,0)



#q=img[336][281]

#b=numpy.array(lColors[6][1])
#b=numpy.append(b,0)

pyplot.imshow(img)
#pyplot.plot(336,281,'ro')
#
pyplot.xlim(0,600)
pyplot.ylim(0,550)
#lum_img=img[:,:,0]
#pyplot.imshow(lum_img,cmap='hot')

redX=[]
redY=[]

for i in range(I2.size[0]):
    for j in range(I2.size[1]):
        if pix[i,j]==pCol[0][1]:
            redX.append(i)
            redY.append(j)
            
pyplot.gca().invert_yaxis()

            
pyplot.plot(redX,redY,'ro')
pyplot.hlines(275,0,600)
pyplot.vlines(300,0,600)
#pyplot.plot(-485,184,'ro')
#pyplot.plot(300,(600./2.),'ko')
#pyplot.grid()

"""
Check for Severe Storms With rN,cCol,lCol and pCol
"""
bigVal=[]
threshold=30.0

for i in range(len(lCol)):
    for j in range(len(cCol)):
        if all(cCol[j]==lCol[i][1]):
            if rN[j]>=threshold:                
                print True,j,i,rN[j]
                bigVal.append([rN[j],j,i])






















        