ffP='/media/tanner/vol2/HRRR/hrrr.t01z.wrfsfcf01.grib2' #Temporary

forecastFile=['']
rasterBands=[]
rasterArrays=[]
cDS=[gdal.Dataset]


#wxInfo=HR.wxStruct
#wxData=[HR.reflectivity,HR.temperature,HR.RH,HR.Empty,HR.Empty,HR.Wind]
def setRadius(wxInfo,radius):
    wxInfo.radius=float(radius)
    
def setLimits(wxData,reflec,temp,rh,Wind):
    wxData[0].limit=reflec
    wxData[1].limit=temp
    wxData[2].limit=rh
    wxData[5].limit=Wind
    
def setLatLon(wxInfo,lat,lon):
    wxInfo.lat=lat
    wxInfo.lon=lon

def setForecastFile(filePath):
    forecastFile[0]=filePath

def getDiskFiles():
    dZ=glob.glob('/media/tanner/vol2/HRRR/grib/*.grib2')
    dZ.sort()
    return dZ

def assignForecast(futureTime):
    cZ=getDiskFiles()
    cZ.sort()
    fFile=cZ[futureTime]
    setForecastFile(fFile)

def readForecastFile():
    ds=gdal.Open(forecastFile[0])
    cDS[0]=ds    
    
def getRasterBands(dataset):
#    numBands=5 #May Change?!
    for i in range(1,7):
        band=dataset.GetRasterBand(i)
        bandArray=band.ReadAsArray()
        rasterBands.append(band)
        rasterArrays.append(bandArray)

def convertLatLonToProj(wxInfo):
    z=0
    raster_wkt= cDS[0].GetProjection()
    spatial_ref=osr.SpatialReference()
    spatial_ref.ImportFromWkt(raster_wkt)
    
    oldCS=osr.SpatialReference()    
    newCS=osr.SpatialReference()
    
    oldCS.ImportFromEPSG(4326)
    newCS.ImportFromWkt(spatial_ref.ExportToWkt())
    
    transform=osr.CoordinateTransformation(oldCS,newCS)
    
#    x,y,z=transform.TransformPoint(coords[1],coords[0])
    x,y,z=transform.TransformPoint(wxInfo.lon,wxInfo.lat)
    gt=cDS[0].GetGeoTransform()
    px=int((x-gt[0])/gt[1])
    py=int((y-gt[3])/gt[5])
    wxInfo.covfefe[0]=px
    wxInfo.covfefe[1]=py
#    covfefe[0]=px
#    covfefe[1]=py

def plotRaster(bandArray):
    pyplot.imshow(bandArray)

def calcAverage(data):
    avg=numpy.average(data)
    return avg

def calcStDev(data):
    stDev=numpy.std(data)
    return stDev

def getBoxValues(wxInfo,boxRad,rasterBand):
#    boxRad=20
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
    LL=[leftSide,bottomSide]
    UL=[leftSide,topSide]
    LR=[rightSide,bottomSide]
    UR=[rightSide,topSide]
    boxSet=rasterBand.ReadAsArray(UL[0],UL[1],boxRad*2,boxRad*2)
    return boxSet

def plotRasterBox(wxInfo,boxRad,rasterBand):
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
#    LL=[leftSide,bottomSide]
    UL=[leftSide,topSide]
#    LR=[rightSide,bottomSide]
#    UR=[rightSide,topSide]
    pyplot.imshow(rasterBand.ReadAsArray(UL[0],UL[1],boxRad*2,boxRad*2))
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()

def calcQuadrant(wxInfo,wxData,n):
    X=wxData[n].exceedX
    Y=wxData[n].exceedY
    oX=wxInfo.radius
    oY=wxInfo.radius
    radBuff=float(wxInfo.radius)/(4.0)
    UD=''
    LR=''
    if X>(oX+radBuff):
        LR='E'
    if X<(oX-radBuff):
        LR='W'
    if Y>(oY+radBuff):
        UD='S'
    if Y<(oY-radBuff):
        UD='N'
    quad=UD+LR
    return quad
    

def calcPercentCovered(wxInfo,data):
    tVal=getBoxValues(wxInfo,int(wxInfo.radius),rasterBands[0])
    totalArea=tVal.size
    affectedArea=len(data)
    pctAffected=float(affectedArea)/float(totalArea)
    return pctAffected

def thresholdsII(wxInfo,wxData,variable,genInt,genVar):        
    datList=[]
    datVal=getBoxValues(wxInfo,int(wxInfo.radius),rasterBands[genInt])
    exceed=numpy.where(datVal>wxData[genInt].limit)
    if exceed[0].size==0:
        wxData[genInt].check=True
        datList.append(False)
        return datList
    else:
        for i in range(len(exceed[0])):
            datList.append(datVal[exceed[0][i]][exceed[1][i]])
        wxData[genInt].raw=datList
        wxData[genInt].exceedX=numpy.average(exceed[0])
        wxData[genInt].exceedY=numpy.average(exceed[1])
        wxData[genInt].limBool=True
        wxData[genInt].check=True
        wxData[genInt].average=calcAverage(datList)
        wxData[genInt].stDev=calcStDev(datList)
        wxData[genInt].exceedQuad=calcQuadrant(genInt)
        wxData[genInt].pctCovered=calcPercentCovered(datList)
            
def checkThresholds(wxInfo,wxData,variable):
    datList=[]
    if variable=='reflectivity':
        genVar=variable
        genInt=0
        thresholdsII(wxInfo,wxData,variable,genInt,genVar)
    if variable=='temperature':
        genVar=variable
        genInt=1
        thresholdsII(wxInfo,wxData,variable,genInt,genVar)
    if variable=='Wind':
        genVar=variable
        genInt=5
        thresholdsII(wxInfo,wxData,variable,genInt,genVar)
    if variable=='RH':
        datVal=getBoxValues(wxInfo,int(wxInfo.radius),rasterBands[2])
        exceed=numpy.where(datVal<wxData[2].limit)
        if exceed[0].size==0:
            datList.append(False)
            return datList
        else:
            for i in range(len(exceed[0])):
                datList.append(datVal[exceed[0][i]][exceed[1][i]])
            wxData[2].raw=datList
            wxData[2].exceedX=numpy.average(exceed[0])
            wxData[2].exceedY=numpy.average(exceed[1])
            wxData[2].limBool=True
            wxData[2].average=calcAverage(datList)
            wxData[2].stDev=calcStDev(datList)
            wxData[2].exceedQuad=calcQuadrant(2)
            wxData[2].pctCovered=calcPercentCovered(datList)
            wxData[2].check=True
#    if variable=='reflectivity' or 'temperature' or 'Wind' or 'RH':

#        
        
    
def locationSanityCheck(wxInfo,wxData,varNum,boxRad):
    """
    Good To Run if you get lost
    """

    a=varNum

    print wxData[varNum]
    print wxData[varNum].exceedX,wxData[varNum].exceedY
    print wxData[varNum].exceedQuad
    print wxData[varNum].pctCovered
    
    centerX=wxInfo.covfefe[0]
    centerY=wxInfo.covfefe[1]    
    
    leftSide=centerX-boxRad
    rightSide=centerX+boxRad
    topSide=centerY-boxRad
    bottomSide=centerY+boxRad
    
    UL=[leftSide,topSide]
    
    pyplot.figure(1)
    bA=osgeo.gdal_array.BandReadAsArray(rasterBands[a],UL[0],UL[1],boxRad*2,boxRad*2)
    pyplot.imshow(bA)
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()
    
    pyplot.figure(2)
    pyplot.imshow(rasterArrays[a])
    pyplot.plot(477,177,'mo',markersize=6)
    pyplot.axis([rightSide,leftSide,bottomSide,topSide])
    #pyplot.xlim(0,1799)
    #pyplot.ylim(0,1059)
    #pyplot.gca().invert_yaxis()
    pyplot.gca().invert_xaxis()
    pyplot.tick_params(labelbottom='off',labeltop='on')
    pyplot.colorbar()
    
    pyplot.figure(3)
    pyplot.imshow(rasterArrays[a])
    pyplot.plot(wxInfo.covfefe[0],wxInfo.covfefe[1],'mo',markersize=6)
    #pyplot.axis([rightSide,leftSide,bottomSide,topSide])
    pyplot.xlim(0,1799)
    pyplot.ylim(0,1059)
    pyplot.gca().invert_yaxis()
    #pyplot.gca().invert_xaxis()
    pyplot.tick_params(labelbottom='off',labeltop='on')
    

def setControls(fCastNum,radius,Lat,Lon,limReflec,limTemp,limRH,limWind,runSanityCheck,checkWhat):
    wxInfo=HR.wxStruct
    wxData=[HR.reflectivity,HR.temperature,HR.RH,HR.Empty,HR.Empty,HR.Wind]
    
    assignForecast(fCastNum)
    readForecastFile()
    getRasterBands(cDS[0])

    setRadius(wxInfo,radius)
    setLatLon(wxInfo,Lat,Lon)
    convertLatLonToProj(wxInfo)
    setLimits(wxData,limReflec,limTemp,limRH,limWind)
    
    for i in range(len(wxData)):
        checkThresholds(wxInfo,wxData,wxInfo.dataForms[i])
        
    if runSanityCheck==True:
        locationSanityCheck(wxInfo,wxData,checkWhat,int(wxInfo.radius))
    
    return wxData
    

lat=46.926183
lon=-114.092779

#assignForecast(18)


#lD=getDiskFiles()
#
#setForecastFile(lD[0])
#readForecastFile()
#getRasterBands(cDS[0])
##
#setRadius(int(20))
#setLatLon(lat,lon)
#convertLatLonToProj()
#setLimits(20,20,57,5)    
##
#for i in range(len(wxData)):
#    checkThresholds(wxInfo.dataForms[i])
#
#locationSanityCheck(5,int(wxInfo.radius))
#







