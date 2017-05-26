################################################################################
#               ___________________________________________________            #
#                                                                              #
#                               WEB - LiDAR :                                  #
#               Web Application to processing and visualization                #
#                             LiDAR data                                       #
#                            Server.r tree metrics                                       #
#               ___________________________________________________            #
#                                                                              #
#                            Carlos Alberto Silva                              #
#                              Forest Engineer                                 #
#                            MSc Forest Resource                               #
#                         Carlos_engflorestal@outlook.com                      #
#                              US Forest Service                               #
#                     Rocky Mountain Reserach Station                          #
################################################################################

################################################################################
# Function to open LiDAR data in R
# readLAS
# from:https://gist.github.com/themel/3911799
publicHeaderDescription <- function() {
  hd <- structure(list(Item = c("File Signature (\"LASF\")",
                                "(1.1) File Source ID", "(1.1) Global Encoding",
                                "(1.1) Project ID - GUID data 1", "(1.1) Project ID - GUID data 2",
                                "(1.1) Project ID - GUID data 3", "(1.1) Project ID - GUID data 4",
                                "Version Major", "Version Minor", "(1.1) System Identifier",
                                "Generating Software", "(1.1) File Creation Day of Year",
                                "(1.1) File Creation Year", "Header Size", "Offset to point data",
                                "Number of variable length records",
                                "Point Data Format ID (0-99 for spec)", "Point Data Record Length",
                                "Number of point records", "Number of points by return",
                                "X scale factor", "Y scale factor", "Z scale factor", "X offset",
                                "Y offset", "Z offset", "Max X", "Min X", "Max Y", "Min Y", "Max Z",
                                "Min Z"), Format = c("char[4]", "unsigned short", "unsigned short",
                                                     "unsigned long", "unsigned short", "unsigned short",
                                                     "unsigned char[8]", "unsigned char", "unsigned char", "char[32]",
                                                     "char[32]", "unsigned short", "unsigned short", "unsigned short",
                                                     "unsigned long", "unsigned long", "unsigned char", "unsigned short",
                                                     "unsigned long", "unsigned long[5]", "double", "double", "double",
                                                     "double", "double", "double", "double", "double", "double", "double",
                                                     "double", "double"), Size = c("4 bytes", "2 bytes", "2 bytes",
                                                                                   "4 bytes", "2 byte", "2 byte", "8 bytes", "1 byte", "1 byte",
                                                                                   "32 bytes", "32 bytes", "2 bytes", "2 bytes", "2 bytes", "4 bytes",
                                                                                   "4 bytes", "1 byte", "2 bytes", "4 bytes", "20 bytes", "8 bytes",
                                                                                   "8 bytes", "8 bytes", "8 bytes", "8 bytes", "8 bytes", "8 bytes",
                                                                                   "8 bytes", "8 bytes", "8 bytes", "8 bytes", "8 bytes"), Required =
                         c("*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*",
                           "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*", "*",
                           "*", "*", "*", "*", "*")), .Names = c("Item", "Format", "Size",
                                                                 "Required"), row.names = 2:33, class = "data.frame")
  hd$what <- ""
  hd$what[grep("unsigned", hd$Format)] <- "integer"
  hd$what[grep("char", hd$Format)] <- "raw"
  hd$what[grep("short", hd$Format)] <- "integer"
  hd$what[grep("long", hd$Format)] <- "integer"
  hd$what[grep("double", hd$Format)] <- "numeric"
  hd$signed <- TRUE
  hd$signed[grep("unsigned", hd$Format)] <- FALSE
  ## number of values in record
  hd$n <- as.numeric(gsub("[[:alpha:][:punct:]]", "", hd$Format))
  hd$n[hd$what == "character"] <- 1
  hd$n[is.na(hd$n)] <- 1
  ## size of record
  hd$Hsize <- as.numeric(gsub("[[:alpha:]]", "", hd$Size))
  ## size of each value in record
  hd$Rsize <- hd$Hsize / hd$n
  hd$Rsize[hd$what == "raw"] <- 1
  hd$n[hd$what == "raw"] <- hd$Hsize[hd$what == "raw"]
  hd
}

readLAS <-
  function(lasfile, skip = 0, nrows = NULL, returnSP = FALSE, returnHeaderOnly = FALSE) {
    
    hd <- publicHeaderDescription()
    pheader <- vector("list", nrow(hd))
    names(pheader) <- hd$Item
    con <- file(lasfile, open = "rb")
    isLASFbytes <- readBin(con, "raw", size = 1, n = 4, endian = "little")
    pheader[[hd$Item[1]]] <- readBin(isLASFbytes, "character", size = 4, endian = "little")
    if (! pheader[[hd$Item[1]]] == "LASF") {
      stop("Not a valid LAS file")
    }
    for (i in 2:nrow(hd)) {
      pheader[[hd$Item[i]]] <- readBin(con, what = hd$what[i], signed = hd$signed[i], size = hd$Rsize[i], endian = "little", n = hd$n[i])
      #print(names(pheader)[i])
      #print(pheader[[hd$Item[i]]])
    }
    close(con)
    ## read the data
    numberPointRecords <- pheader[["Number of point records"]]
    offsetToPointData <- pheader[["Offset to point data"]]
    pointDataRecordLength <-pheader[["Point Data Record Length"]]
    xyzScaleOffset <- cbind(unlist(pheader[c("X scale factor", "Y scale factor", "Z scale factor")]),
                            unlist(pheader[c("X offset", "Y offset", "Z offset")]))
    
    
    if (returnHeaderOnly) return(pheader)
    
    con <- file(lasfile, open = "rb")
    junk <- readBin(con, "raw", size = 1, n = offsetToPointData)
    
    ## deal with rows to skip and max rows to be read
    if (skip > 0) {
      ## seek is unreliable on windows, or I'm using it incorrectly
      ## so we junk the bytes to skip
      junk <- readBin(con, "raw", size = 1, n = pointDataRecordLength * skip)
      numberPointRecords <- numberPointRecords - skip
      #pos <- seek(con, where = pointDataRecordLength * skip)
      # print(c(pos = seek(con), skip = skip, where = pointDataRecordLength * skip))
    }
    if (!is.null(nrows)) {
      if (numberPointRecords > nrows) numberPointRecords <- nrows
    }
    
    if (numberPointRecords < 1) stop("no records left to read")
    
    
    # include a loop to read just points inside the x and y coordinates
    
    allbytes <- matrix(readBin(con, "raw", n = pointDataRecordLength * numberPointRecords, size = 1, endian = "little"),
                       ncol= pointDataRecordLength, nrow = numberPointRecords, byrow = TRUE)
    
    
    close(con)
    mm <- matrix(readBin(t(allbytes[,1:(3*4)]), "integer", size = 4, n = 3 * numberPointRecords, endian = "little"), ncol = 3, byrow = TRUE)
    gpstime <- NULL
    if (ncol(allbytes) == 28) gpstime <- readBin(t(allbytes[ , 21:28]), "numeric", size = 8, n = numberPointRecords, endian = "little")
    
    intensity <- readBin(t(allbytes[, 13:14]), "integer", size = 2, n = numberPointRecords, signed = FALSE, endian = "little")
    mm[,1] <- mm[ ,1] * xyzScaleOffset[1,1] + xyzScaleOffset[1, 2]
    mm[,2] <- mm[ ,2] * xyzScaleOffset[2,1] + xyzScaleOffset[2, 2]
    mm[,3] <- mm[ ,3] * xyzScaleOffset[3,1] + xyzScaleOffset[3, 2]
    colnames(mm) <- c("x", "y", "z")
    
    bytes <- readBin(t(allbytes[,15]), "integer", size = 1, n = numberPointRecords, signed = FALSE, endian = "little")
    require(bitops)
    
    # bits 0..2: byte & 00000111
    returnNumber <- bitAnd(7, bytes)
    # bits 3..5: byte & 00111000 >> 3
    numberOfReturns <- bitShiftR(bitAnd(56, bytes), 3)
    # bit 6: & 0100000 >> 6
    scanDirectionFlag <- bitShiftR(bitAnd(bytes, 64), 6)
    # bit 7: & 1000000 >> 7 
    edgeOfFlightFlag <- bitShiftR(bitAnd(bytes, 128), 7)
    
    
    if (returnSP) {
      require(sp)
      SpatialPoints(cbind(mm, gpstime, intensity, returnNumber))
    } else {
      cbind(mm, gpstime, intensity, returnNumber)
    }
  }

################################################################################
################################################################################
# Libraries
#install.packages("sp")
#install.packages("rgl")
#install.packages("RColorBrewer")
#require(sp)
#require(rgl)

################################################################################
################################################################################
# Libraries
#library(shiny)
#library(shinyRGL)
#library(shinyGridster)
#library(ShinyDash)
#library(shinyIncubator)

################################################################################
InTREE<-function(Input, fr=FALSE, Deciduous=FALSE,Pinus=FALSE,Combined=TRUE,myequation=FALSE,Ang,ht1,ht2,ht3,radius=NULL) {

  #rgl.open()
  #bg3d("white")
  
  #Input<-subset(Input, Input[,3]>= hthreshold) # subset by height treshold
  Input2<-Input
  
  while (nrow(Input2)>2){  # loop
    
    if (!exists ("ClipTree0")) {
      
      Input<-cbind(Input[,1:3],0) } else { Input<-ClipTree0} 
    
    MaxZ<-max(Input[,3])  # fild the max point
    XY<-as.data.frame(subset(Input[,1:2],Input[,3]==MaxZ)) # get the x and y from the max point
    maxPoint<-cbind(XY[1,],MaxZ)   
    
    if(exists("XYsave")==TRUE){
      XYsave<-rbind(XYsave,maxPoint)} else {XYsave<-maxPoint}
    
    # radius: Fr= fixes radius, 
    if (fr==TRUE){r<-radius} 
    if (Deciduous==TRUE) {r<- (3.09632 + 0.00895*(MaxZ*MaxZ))/2} 
    if (Pinus==TRUE) {r<- (3.75105 + 0.17919*MaxZ + 0.01241*(MaxZ*MaxZ))/2} 
    if (Combined==TRUE) {r<-(2.51503+0.00901*(MaxZ*MaxZ))/2}
    if (myequation==TRUE) {r<-Ang+ht1*MaxZ+ht2*(MaxZ*MaxZ) + ht3*(MaxZ*MaxZ*MaxZ)}
    
    # create the polygon to clip the tree
    angs <- rep(seq(0,2*pi, length=50),5)
    distfun <- sqrt(1)
    x <- XY[1,1] + r*distfun*cos(angs)
    y <- XY[1,2] + r*distfun*sin(angs)
    Poly <- Polygon(rbind(cbind(x,y),cbind(x[1],y[1])))
    Poly2 <- Polygons(list(Poly), "s1")
    PolyTree <- SpatialPolygons(list(Poly2))
    #plot(x,y)
    # clip tree
    points<-SpatialPoints(Input[,1:3])
    
    TreeVec<-over(as(points, "SpatialPoints"), PolyTree)
    
    # classification of the points , tree= number and not tree = NA = 0 
    TreeVec[is.na(TreeVec)]<-0
    
    if (exists("TreeID")==TRUE) {
      TreeID<-as.numeric(TreeID) + 1 } else { TreeID<-as.numeric(1)}
    
    TreeVec[TreeVec!=0]<-TreeID
    
    ClipTree<-cbind(Input[,1:3],TreeVec)
    Input2<-ClipTree
    ClipTree0<-subset(ClipTree, ClipTree[,4]==0) # mylas with treeID = 0. This data will return to process
    
    TreeK<-subset(ClipTree,ClipTree[,4]!=0) # Tree selected
    
    # merge data with trees ID
    if (exists("MylasTree")==TRUE) {
      MylasTree<-rbind(MylasTree,TreeK)
    } else {MylasTree<-TreeK}
    
    # plot 3d trees
    #plot3d(MylasTree[,1:3], col=c(MylasTree[,4]), add=T)
    #axes3d()  
    #vec<-rbind(c( XY[1,1], XY[1,2], 0 ), c( XY[1,1], XY[1,2], MaxZ))
    #segments3d(vec, col="brown", lwd=2)
    
    if ((!nrow(ClipTree0)>2)==TRUE) {
      print("LiDAR data processed")
      break}
  }
  list(MylasTree,XYsave)
} 


################################################################################
# TM
output$sctPlotAlpha <- renderWebGL({

output$pageviews <-	renderText({
  if (!file.exists("pageviews.Rdata")) pageviews <- 0 else load(file="pageviews.Rdata")
  pageviews <- pageviews + 1
  save(pageviews,file="pageviews.Rdata")
  paste("Number of Visits:",pageviews)
})
 
 if ((input$Mydata)=="ED") {

LiDAR<- readLAS("Eglin.plots_1.las")
} else { 
    
  inFileLAS <- input$las
    if (is.null(inFileLAS)) {
      plot3d(1,1,1, axes=FALSE, col="white", pch=".") 
      return(NULL)} 

  LiDAR<- readLAS(inFileLAS$datapath) } 

  plot3d(1,1,1, axes=FALSE, col="white") 
         
  output$HtreshoudAlpha <- renderUI({
    min<-min(LiDAR[,3])
    max<-max(LiDAR[,3])
    value<-min+1.37
    sliderInput("HtreshoudAlpha","Tree Height Threshold (m)",min,max,value,step=0.01,format="#.##")})
      
  if (input$action_button == 0) 
    return()
  isolate({ 
    
    withProgress(session, min=1, max=5, {
      setProgress(message = 'LiDAR data processing',
                  detail = 'This may take a while...')
      for (i in 1:5) {
        setProgress(value = i)
        Sys.sleep(0.5)
      }  
  
      htreshApha<-input$HtreshoudAlpha
  
  LiDARsub <- subset(LiDAR, LiDAR[,3] >= htreshApha) 
  
  Ang<-as.numeric(input$Ang)
  ht1<-as.numeric(input$ht1)
  ht2<-as.numeric(input$ht2)
  ht3<-as.numeric(input$ht3)
  radius<-as.numeric(input$frv)
  
  if ((input$radiustype)=="FR") {LAsClip<-InTREE(LiDARsub,fr=TRUE, Deciduous=FALSE,Pinus=FALSE,Combined=FALSE,myequation=FALSE,Ang,ht1,ht2,ht3,radius=radius)} 
  
  if ((input$radiustype)=="VR") {
  if ((input$equation)=="DC") {LAsClip<-InTREE(LiDARsub,fr=F,Deciduous=TRUE,Pinus=FALSE,Combined=FALSE,myequation=FALSE,Ang=NULL,ht1=NULL,ht2=NULL,ht3=NULL,radius=NULL)}
  if ((input$equation)=="PI") {LAsClip<-InTREE(LiDARsub,fr=F,Deciduous=FALSE,Pinus=TRUE,Combined=FALSE,myequation=FALSE,Ang=NULL,ht1=NULL,ht2=NULL,ht3=NULL,radius=NULL)}
  if ((input$equation)=="CB") {LAsClip<-InTREE(LiDARsub,fr=F,Deciduous=FALSE,Pinus=FALSE,Combined=TRUE,myequation=FALSE,Ang=NULL,ht1=NULL,ht2=NULL,ht3=NULL,radius=NULL)}
  if ((input$equation)=="YR") {LAsClip<-InTREE(LiDARsub,fr=F,Deciduous=FALSE,Pinus=FALSE,Combined=FALSE,myequation=TRUE,Ang,ht1,ht2,ht3,radius=NULL)}}
    
  MylasTree<-data.frame(LAsClip[1])
  
  XYsave<-data.frame(LAsClip[2])
  
  output$summaryTrees <- renderTable({
    summary<-matrix(,ncol=2,nrow=6)
    colnames(summary)<-c("Metrics", "Value")
    summary[1,]<-c("Number of trees",nlevels(factor(MylasTree[,4])))
    summary[2,]<-c("Hmax",max(LiDARsub[,3]))
    summary[3,]<-c("Hmean",round(mean(LiDARsub[,3]),digits=2))
    summary[4,]<-c("Hmin",min(LiDARsub[,3],na.rm=TRUE))
    summary[5,]<-c("Median",round(median(LiDARsub[,3]),digits=2))
    summary[6,]<-c("Hsd",round(sd(LiDARsub[,3]),digits=2))
    summary
  })
  

    bg3d(input$backApha)

      
    plot3d(MylasTree[,1:3],  axes=FALSE, xlab="UTM.Easting", ylab="UTM.Northing", zlab="Height(m)", col=MylasTree[,4], xlim=c(range(LiDAR[,1])),ylim=c(range(LiDAR[,2])),zlim=c(range(LiDAR[,3])))
      
      if ((input$PlotAxes)==TRUE) {
        axes3d(,col=input$Axescolor)
      } else {axes3d(c("x-", "y-"))}
      
    if (input$Trunkcbox2==TRUE){
      for ( i in 1:nrow(XYsave)) {
        vec<-rbind(c(XYsave[i,1], XYsave[i,2], 0 ), c(XYsave[i,1], XYsave[i,2], XYsave[i,3]))
      segments3d(vec, col=input$trunkcolor, lwd=2)}}
  
  
    title3d(xlab = "UTM.Easting", ylab = "UTM.Northing",zlab = "Height(m)", col=input$legendcolor)
    planes3d(a=0,b=0,c=-1,d=0.0001,color="gray",alpha=0.4)
    aspect3d(1,1,0.5)
  
  output$downloadTree2 <- downloadHandler(
    filename = function() {
      paste("Trees",input$las, Sys.Date(), '.csv', sep='')
    },
    content = function(file) {
      newLAS<-merge(LiDARsub,MylasTree,by=c("x","y","z"))
     write.csv(newLAS, file, row.names=FALSE)
    })
  output$plotUTMx <- renderPlot({
    par(mfrow=c(1,1), mar=c(4,4,0,0))
    plot(cbind(LiDAR[,1],LiDAR[,3]), col="forestgreen", xlab="UTM Easting", ylab="Height (m)")
    abline(h=htreshApha, v=0, col = "red",lwd=3,lty = 3)},height = 320, width = 400)
  
  output$plotUTMy <- renderPlot({
    par(mfrow=c(1,1), mar=c(4,4,0,0))
    plot(LiDAR[,2:3], col="forestgreen",xlab="UTM Northing", ylab="Height (m)")
    abline(h=htreshApha, v=0, col = "red", lwd=3,lty = 3)},height = 320, width = 400)
  
  output$histTree <- renderPlot({
    par(mfrow=c(2,1), mar=c(4.5,4,2,5))
    dens<-density(LiDARsub[,3],adjust = 1.3, kernel = "gaussian")
    plot(dens$y,dens$x, col="black",xlab="Density",ylab="Height (m)",type="line",lwd="1",ylim=c(0,max(LiDAR[,3]))) 
    polygon(dens$y,dens$x, col="forestgreen", border="black")
    boxplot(LiDARsub[,3],ylim=c(0,max(LiDARsub[,3])),horizontal=F, col="forestgreen",ylab="Height (m)")
  },height = 580,width=300) 

  }) 
  })
  
},width=545, height=540)
################################################################################
