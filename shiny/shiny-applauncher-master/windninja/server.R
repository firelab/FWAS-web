#================================= 
#            WindNinja
#=================================

library(shiny)
library(leaflet)
library(maps)
library(raster)
library(plotGoogleMaps)
library(stringr)

#default max upload size is 5MB, increase to 30.
options(shiny.maxRequestSize=50*1024^2)

demFile <- NULL
forecastDir <- ""
gSpdFiles <- NULL

# From a future version of Shiny
bindEvent <- function(eventExpr, callback, env=parent.frame(), quoted=FALSE) {
  eventFunc <- exprToFunction(eventExpr, env, quoted)
  
  initialized <- FALSE
  invisible(observe({
    eventVal <- eventFunc()
    if (!initialized)
      initialized <<- TRUE
    else
      isolate(callback())
  }))
}

# Make smaller, side-by-side text boxes
textInputRow<-function (inputId, label, value = "") 
{
    div(
        tags$label(label, `for` = inputId), 
        tags$input(id = inputId, type = "text", value = value, class="input-small"))
}


#==================================================================
#     server logic
#==================================================================

shinyServer(function(input, output, session) {
 
#-----------------------------------------------------
#    Add run button 
#----------------------------------------------------- 

  addRunButton <- reactive({
      if(input$elevation == "boundingBox" || input$elevation == "centerLatLon" || length(input$demFile) > 0){
          if(length(input$run_wn) > 0){
              if(input$run_wn == 1){
                  paste("")
              }
              else{
                  actionButton('run_wn', img(src = "wn-icon.png", height = 40, width = 40))
              }
          }
          else{
              actionButton('run_wn', img(src = "wn-icon.png", height = 40, width = 40))
          }
      }
      else{
          paste("")
      }
  })

  output$runButton <- renderUI({
      addRunButton()
  })
  
  addRunButtonText <- reactive({
      if(input$elevation == "boundingBox" || input$elevation == "centerLatLon" || length(input$demFile) > 0){
          if(length(input$run_wn) > 0){
              if(input$run_wn == 1){
                  h4("Run finished!")
              }
              else{
                  h4("Start run!")
              }
          }
      }
      else{
          paste("Specify the elevation input to get started.")
      }
  })
  
  output$runButtonText <- renderUI({
      addRunButtonText()
  })

#-----------------------------------------------------
#    write the cfg
#-----------------------------------------------------   

  writeCfg <- reactive({
  isolate({
      cfg<-"windninja.cfg"
      cat("num_threads = 2\n",file=cfg)
      cat(paste("vegetation = ", input$vegetation, "\n", collapse=""), file=cfg, append=TRUE)

      if(input$elevation == "centerLatLon"){
          cat(paste("fetch_elevation = dem.tif\n"), file=cfg, append=TRUE)
          cat(paste("elevation_source = us_srtm\n"), file=cfg, append=TRUE)
          cat(paste("x_center = ", input$centerLon, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("y_center = ", input$centerLat, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("x_buffer = ", input$xBuffer, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("y_buffer = ", input$yBuffer, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("buffer_units = ", input$unitsBuffer, "\n", collapse=""),file=cfg, append=TRUE)
          demFile <<- "dem.tif"
      }
 
      else if(input$elevation == "boundingBox"){
          cat(paste("fetch_elevation = dem.tif\n"), file=cfg, append=TRUE)
          cat(paste("elevation_source = us_srtm\n"), file=cfg, append=TRUE)
          cat(paste("north = ", input$northExtent, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("south = ", input$southExtent, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("east = ", input$eastExtent, "\n", collapse=""),file=cfg, append=TRUE)
          cat(paste("west = ", input$westExtent, "\n", collapse=""),file=cfg, append=TRUE)
          demFile <<- "dem.tif"
      }

      else if(input$elevation == "uploadDem"){
          #move the file to working dir and rename
          if(length(input$demFile$datapath) == 2){
              system(paste("mv ",  input$demFile$datapath[1], "dem.asc"))
              system(paste("mv ",  input$demFile$datapath[2], "dem.prj"))
          }
          else{
              system(paste("mv ",  input$demFile$datapath, "dem.asc"))
          }
          demFile <<- "dem.asc"
          cat(paste("elevation_file = ", demFile, "\n"), file=cfg, append=TRUE)
      }
      cat(paste("time_zone = auto-detect\n", collapse=""), file=cfg, append=TRUE)
      cat(paste("initialization_method = ", input$initializationMethod, "\n", collapse=""), file=cfg, append=TRUE)

      if(input$initializationMethod == "domainAverageInitialization"){
          cat(paste("input_wind_height = ", input$inputWindHeight, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("units_input_wind_height = ", input$unitsInputWindHeight, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("input_speed = ", input$inputSpeed, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("input_speed_units = ", input$unitsInputSpeed, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("input_direction = ", input$inputDirection, "\n", collapse=""), file=cfg, append=TRUE)
      }
      else if(input$initializationMethod == "wxModelInitialization"){
          cat(paste("wx_model_type = ", input$wxModelType, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("forecast_duration = ", input$forecastDuration, "\n", collapse=""), file=cfg, append=TRUE)
          forecastDir <<- paste0(input$wxModelType,"-", demFile)
      }
      if(input$diurnalInput == TRUE){
          cat("diurnal_winds = true\n", file=cfg, append=TRUE)
          if(input$initializationMethod != "wxModelInitialization"){
              cat(paste("uni_air_temp = ", input$inputAirTemp, "\n", collapse=""), file=cfg, append=TRUE)
              cat(paste("air_temp_units = ", input$unitsInputAirTemp, "\n", collapse=""), file=cfg, append=TRUE)
          }
      }
      if(input$stabilityInput == TRUE){
          cat("non_neutral_stability = true\n", file=cfg, append=TRUE)
          
      }
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) & input$initializationMethod != "wxModelInitialization"){
          cat(paste("uni_cloud_cover = ", input$inputCloudCover, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("cloud_cover_units = ", input$unitsInputCloudCover, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("year = ", input$year, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("month = ", input$month, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("day = ", input$day, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("hour = ", input$hour, "\n", collapse=""), file=cfg, append=TRUE)
          cat(paste("minute = ", input$minute, "\n", collapse=""), file=cfg, append=TRUE)
      }
      cat(paste("output_wind_height = ", input$outputWindHeight, "\n", collapse=""), file=cfg, append=TRUE)
      cat(paste("units_output_wind_height = ", input$unitsOutputWindHeight, "\n", collapse=""), file=cfg, append=TRUE)
      cat(paste("mesh_choice = ", input$meshChoice, "\n", collapse=""), file=cfg, append=TRUE)
      if(input$outFire == 1 || input$outGoogleMaps == 1){
          cat("write_ascii_output = true\n", file=cfg, append=TRUE)
      }
      if(input$outGoogleEarth == 1){
          cat("write_goog_output = true\n", file=cfg, append=TRUE)
      }
      if(input$outShape == 1){
          cat("write_shapefile_output = true\n", file=cfg, append=TRUE)
      }
      if(input$outVtk == 1){
          cat("write_vtk_output = true\n", file=cfg, append=TRUE)
      }
      })
  })
     
#-----------------------------------------------------
#   Start a WindNinja run
#-----------------------------------------------------

    createRunMessage <- reactive({
        if(length(input$run_wn) > 0){ 
            if(input$run_wn == 1){
                paste("Click the refresh button in your browser to do another run.\n")
            }
            else{
                #paste("Specifiy input parameters above. Click the run button when you're ready to do a run.\n",
                #      collapse="")
            }
        }
        else{
            paste("")
        }
    })
    
    output$runMessage <- renderText({
      createRunMessage()
  })
    

    runWN <- reactive({
        if(length(input$run_wn) > 0 && input$run_wn == 1){
        
        withProgress(session, min=1, max=15, {
        i = 1
        writeCfg()
        unlink ("wnpipe")
        system("mkfifo wnpipe")
    
         system(paste("NINJA_FILL_DEM_NO_DATA=YES", "/home/natalie/src/windninja/build/src/cli/WindNinja_cli", 
                "windninja.cfg", ">> wnpipe"
                ), intern=FALSE, wait=FALSE)
         fileName="wnpipe"
         con=fifo(fileName,open="rt",blocking=TRUE)
         linn = " "
         while ( length(linn) > 0) {
           i = i + 1
           linn=scan(con,nlines=1,what="character", sep=" ", quiet=TRUE)
           setProgress(message = 'WindNinja is running.',
                       detail = paste(linn, collapse=" "), value = i)
         }
         close(con)
         unlink ("wnpipe")
       })
       }
    })

    output$wnText <- renderPrint({
         runWN()   
    })
    
#-----------------------------------------------------
#   Download outputs
#-----------------------------------------------------

  createDownloadButton <- reactive({
      if(length(input$run_wn) > 0 && 
          input$run_wn == 1){ 

          downloadButton('downloadData', 'Download Output Files')
      }
      if("windninja.cfg" %in% dir()){
          downloadButton('downloadData', 'Download Output Files')
      }
  })
  
  output$downloadButton <- renderUI({
      createDownloadButton()
  }) 
  
  output$downloadData <- downloadHandler(
         filename = function() { paste("windninja_output", '.tar.gz', sep='') },
         content = function(file) {
           tar(file,".", compression="gzip") 
         }
  )

#-----------------------------------------------------
#  Clean up for another run 
#-----------------------------------------------------
createCleanupButton<-reactive({
    if(length(input$run_wn) > 0 || length(input$run_wn) == 0){
        if("windninja.cfg" %in% dir()){
            actionButton('clean_up', 'Clean Up')
        }
        else{
            h4("")
        }
    }
})
output$cleanupButton<-renderUI({
    createCleanupButton()
})
cleanup<-reactive({
    #isolate({
        if(length(input$clean_up) > 0 && input$clean_up > 0){
            unlink("windninja.cfg")
            unlink("*.asc")
            unlink("*.prj")
            unlink("www/L*")
            unlink("www/*.htm")
            unlink("NCEP*", recursive=TRUE)
            unlink("dem*")
            unlink("*.kmz")
            h4("Project space cleaned up. Click the refresh button in your browser to do another run.")
        }
    #})
})

output$cleanupText<-renderUI({
    cleanup()
})

#---------------------------------------------------------
# convert ascii grids to Google Maps format and display
#---------------------------------------------------------
  convertToGoogleMaps <- reactive({  
      if(length(input$run_wn) > 0){ 
          if(input$run_wn==1 && input$outGoogleMaps == 1){
              i = 1
              withProgress(session, min=1, max=10, {
              
              setProgress(message = 'Writing Google Maps output.',
                       detail = "This may take a few minutes...", value = 2)
                       
              if(input$initializationMethod == "wxModelInitialization"){
                  
                  dir<-system(paste("ls -t", forecastDir), intern = TRUE)
                  dir<-paste0(forecastDir, "/", dir[1])
                  
                  spdFiles<-system(paste("ls -t", dir, " | grep vel.asc"), intern = TRUE)
                  angFiles<-system(paste("ls -t", dir, " | grep ang.asc"), intern = TRUE)

                  gSpdFiles<<-spdFiles

                  spdFiles<-paste0(dir, "/", spdFiles)
                  angFiles<-paste0(dir, "/", angFiles)
              }
              else{
                  spdFiles<-system("ls -t | grep vel.asc", intern = TRUE)
                  angFiles<-system("ls -t | grep ang.asc", intern = TRUE)

                  spdFiles<-(spdFiles[1]) # get the most recent one
                  angFiles<-(angFiles[1]) # get the most recent one

              }
              
              for(i in 1:length(spdFiles)){
                  spd<-raster(spdFiles[i])
                  ang<-raster(angFiles[i])
              
                  setProgress(value = 3 + i)

                  vectors<-brick(spd, ang)
                  names(vectors)<-c("speed", "angle")

                  vectors_sp<-rasterToPoints(vectors, spatial=TRUE)
              
                  #setProgress(value = 6)
          
                  vectors_sp$angle<-vectors_sp$angle - 180
                  vectors_sp$angle[vectors_sp$angle < 0] <- vectors_sp$angle[vectors_sp$angle < 0] + 360
              
                  #setProgress(value = 8)
              
                  t<-str_extract(spdFiles[1], "_[0-9]?[0-9][0-9]m_")
                  maxlength <- as.numeric(substr(t, 2,(nchar(t)-2)))

                  wind_vect=vectorsSP(vectors_sp, maxlength=maxlength, zcol=c('speed','angle'))
              
                  #setProgress(value = 10)
                   
                  if(input$initializationMethod == "wxModelInitialization"){
                      if(!is.na(str_extract(spdFiles[1], "NAM"))){
                          model<-"NAM"
                      }
                      else if(!is.na(str_extract(spdFiles[1], "NDFD"))){
                          model<-"NDFD"
                      }
                      else if(!is.na(str_extract(spdFiles[1], "RAP"))){
                          model<-"RAP"
                      }
                      else if(!is.na(str_extract(spdFiles[1], "GFS"))){
                          model<-"GFS"
                      }
                      else{
                          model<-""
                      }

                      begin<-str_locate(spdFiles[i], dir)[2] + 6
                      end<-nchar(spdFiles[i])-8
                      fname<-paste0(model, "_", substr(spdFiles[i], begin, end), ".htm")
                      #fname<-paste0("wind_vect_", i, ".htm")
                  }
                  else{
                      fname<-paste0("domainAverage", substr(spdFiles[i], 4, nchar(spdFiles[i])-8), ".htm")
                  }

                  pal<-colorRampPalette(c("blue","green","yellow", "orange", "red"))
                  m=plotGoogleMaps(wind_vect, filename=fname, zcol='speed', colPalette=pal(5),
                           mapTypeId='TERRAIN',strokeWeight=2,
                           clickable=FALSE,openMap=FALSE)
                           
                  #setProgress(value = 13)
                           
                  system(paste("mv", fname, "Legend* www/"))
              
                  #setProgress(value = 14)
              }
              
              paste("")
              
              setProgress(value = 15)
              })   
          }
      }
      else{
          paste("")
      }
  })
  
  output$convertToGoogleMapsText <- renderUI({
      convertToGoogleMaps() #writes the Google Maps File 
    })

  displayMap <- reactive({
      if(length(input$run_wn) > 0 ){   
          if(input$run_wn==1 && 
             input$outGoogleMaps == 1 && 
             length(list.files(path="www/", pattern=".htm") != 0)){
              tags$iframe(
                  srcdoc = paste(readLines(paste0('www/',input$windVectFile)), collapse = '\n'),
                  width = "100%",
                  height = "900px"
              )
          }
      }
      if(length(list.files(path="www/", pattern=".htm") != 0)){
         #f<-list.files(path="www/", pattern=".htm")[1]
         tags$iframe(
             srcdoc = paste(readLines(paste0('www/',input$windVectFile)), collapse = '\n'),
             width = "100%",
             height = "600px"
        )   
      }
  })

  output$mymap <- renderUI({
      displayMap()
  })

#-------------------------------------------------------------
#   create map viewing options for wx model runs
#-------------------------------------------------------------
createMapSelection <- reactive({
   if((length(input$run_wn) == 0 ||
       length(input$run_wn) > 0 ) && 
       length(list.files(path="www/", pattern=".htm") != 0)){ 
          selectInput("windVectFile", "Select a forecast to view:",
                      selected=(list.files(path="www/", pattern=".htm")[1]),
                      c=list.files(path="www/", pattern=".htm"))                
    }
})
output$mapSelection <- renderUI({
      createMapSelection()
  })

#-------------------------------------------------------------
#   create elevation input options (bb or dem upload)
#-------------------------------------------------------------
  createSpace <- reactive({
      if(input$elevation == "boundingBox"){
          tags$br()
      }
  })
  createNbox <- reactive({
      if(input$elevation == "boundingBox"){
          textInputRow("northExtent", "North:", "46.8468")
      }
  })
  createSbox <- reactive({
      if(input$elevation == "boundingBox"){
          textInputRow("southExtent", "South:", "46.7856")
      }
  })
  createEbox <- reactive({
      if(input$elevation == "boundingBox"){
          textInputRow("eastExtent", "East:", "-116.7914")
      }
  })
  createWbox <- reactive({
      if(input$elevation == "boundingBox"){
          textInputRow("westExtent", "West:", "-116.9517")
      }
  })
  createLatbox <- reactive({
      if(input$elevation == "centerLatLon"){
          textInputRow("centerLat", "Lat:", "46.7856")
      }
  })
  createLonbox <- reactive({
      if(input$elevation == "centerLatLon"){
          textInputRow("centerLon", "Lon:", "-116.9517")
      }
  })
  createXbuffer <- reactive({
      if(input$elevation == "centerLatLon"){
          textInputRow("xBuffer", "x Buffer:", "10")
      }
  })
  createYbuffer <- reactive({
      if(input$elevation == "centerLatLon"){
          textInputRow("yBuffer", "y Buffer:", "10")
      }
  })
  createUnitsBuffer <- reactive({
      if(input$elevation == "centerLatLon"){
          selectInput("unitsBuffer", "Buffer units:",
                list("mi" = "miles", 
                     "km" = "kilometers"))
      }
  })
  createDemUpload <- reactive({
      if(input$elevation == "uploadDem"){
          fileInput("demFile", "Upload DEM:", multiple=TRUE, accept=NULL)
      }
  })

  output$addExtraSpace <- renderUI({
      createSpace()
  })
  output$addExtraSpace2 <- renderUI({
      createSpace()
  })
  output$nField <- renderUI({
      createNbox()
  })
  output$sField <- renderUI({
      createSbox()
  })
  output$eField <- renderUI({
      createEbox()
  })
  output$wField <- renderUI({
      createWbox()
  })
  output$latField <- renderUI({
      createLatbox()
  })
  output$lonField <- renderUI({
      createLonbox()
  })
  output$xBufferField <- renderUI({
      createXbuffer()
  })
  output$yBufferField <- renderUI({
      createYbuffer()
  })
  output$bufferUnits <- renderUI({
      createUnitsBuffer()
  })
  output$demUploader <- renderUI({
      createDemUpload()
  })


#-------------------------------------------------------------
#   create input wind fields for domain average runs
#-------------------------------------------------------------
  createHeightBox <- reactive({
      if(input$initializationMethod == "domainAverageInitialization"){
          textInputRow("inputWindHeight", "Input height:", "20.0")
      }
  })
  createUnitsHeightButtons <- reactive({
      if(input$initializationMethod == "domainAverageInitialization"){
          #radioButtons("unitsInputWindHeight", "Units", c("ft" = "ft", "m" = "m"))
          selectInput("unitsInputWindHeight", "Units:",
                list("ft" = "ft", 
                     "m" = "m"))
      }
  })
  createInputSpeedBox <- reactive({
      if(input$initializationMethod == "domainAverageInitialization"){
          textInputRow("inputSpeed", "Wind speed:", "0.0")
      }
  })
  createUnitsSpeedButtons <- reactive({
      if(input$initializationMethod == "domainAverageInitialization"){
          #radioButtons("unitsInputSpeed", "Units", c("mph" = "mph", "m/s" = "mps"))
          selectInput("unitsInputSpeed", "Units:",
                list("mph" = "mph", 
                     "m/s" = "mps"))
      }
  })
  createDirectionBox <- reactive({
      if(input$initializationMethod == "domainAverageInitialization"){
          textInputRow("inputDirection", "Wind direction:", "0")
      }
  })
  createOutputHeightBox <- reactive({
      textInputRow("outputWindHeight", "Output height:", "20.0")
  })
  createUnitsOutputHeightButtons <- reactive({
      #radioButtons("unitsOutputWindHeight", "Units", c("ft" = "ft", "m" = "m"))
      selectInput("unitsOutputWindHeight", "Units:",
                list("ft" = "ft", 
                     "m" = "m"))
  })
  
  output$inputHeightField <- renderUI({
      createHeightBox()
  })
  output$unitsInputHeightField <- renderUI({
      createUnitsHeightButtons()
  })
  output$inputSpeedField <- renderUI({
      createInputSpeedBox()
  })
  output$unitsInputSpeedField <- renderUI({
      createUnitsSpeedButtons()
  })
  output$inputDirectionField <- renderUI({
      createDirectionBox()
  })
  output$outputHeightField <- renderUI({
      createOutputHeightBox()
  })
  output$unitsOutputHeightField <- renderUI({
      createUnitsOutputHeightButtons()
  })

#-------------------------------------------------------------
#   create input wind fields for weather model runs
#-------------------------------------------------------------
  createModelTypeInput <- reactive({
      if(input$initializationMethod == "wxModelInitialization"){
          selectInput("wxModelType", "Weather Model:",
                list("NAM" = "NCEP-NAM-12km-SURFACE",
                     "NAM-Alaska" = "NCEP-NAM-Alaska-11km-SURFACE", 
                     "GFS" = "NCEP-GFS-GLOBAL-0_5deg-SURFACE",
                     "RAP" = "NCEP-RAP-13km-SURFACE",
                     "NDFD" = "NCEP-NDFD-5km"))
      }
  })
  createDuration <- reactive({
      if(input$initializationMethod == "wxModelInitialization"){
          textInputRow("forecastDuration", "Forecast duration (hrs):", "6")
      }
  })
  output$forecastDuration <- renderUI({
      createDuration()
  })
  output$inputWxModelType <- renderUI({
      createModelTypeInput()
  })
#-------------------------------------------------------------
#   create input option boxes for diurnal and stability
#-------------------------------------------------------------
  createSpace <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          tags$br()
      }
  })
  createYearbox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          year <- as.POSIXlt(Sys.time())$year + 1900
          textInputRow("year", "Year:", year)
      }
  })
  createMonthbox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          month <- as.POSIXlt(Sys.time())$mon + 1
          textInputRow("month", "Month:", month)
      }
  })
  createDaybox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          day <- as.POSIXlt(Sys.time())$mday
          textInputRow("day", "Day:", day)
      }
  })
  createHourbox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          hour <- as.POSIXlt(Sys.time())$hour
          textInputRow("hour", "Hour:", hour)
      }
  })
  createMinutebox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          min <- as.POSIXlt(Sys.time())$min
          textInputRow("minute", "Minute:", min)
      }
  })

  output$addExtraSpace <- renderUI({
      createSpace()
  })
  output$yearField <- renderUI({
      createYearbox()
  })
  output$monthField <- renderUI({
      createMonthbox()
  })
  output$dayField <- renderUI({
      createDaybox()
  })
  output$hourField <- renderUI({
      createHourbox()
  })
  output$minuteField <- renderUI({
      createMinutebox()
  })
  
  createInputAirTempBox <- reactive({
      if(input$diurnalInput == TRUE & input$initializationMethod != "wxModelInitialization"){
          textInputRow("inputAirTemp", "Air temperature:", "72.0")
      }
  })
  createUnitsAirTempButtons <- reactive({
      if(input$diurnalInput == TRUE & input$initializationMethod != "wxModelInitialization"){
          #radioButtons("unitsInputAirTemp", "Units", c("F" = "F", "C" = "C"))
          selectInput("unitsInputAirTemp", "Units:",
                list("F" = "F", 
                     "C" = "C"))
      }
  })
  createInputCloudCoverBox <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          textInputRow("inputCloudCover", "Cloud cover:", "50")
      }
  })
  createUnitsCloudCoverButtons <- reactive({
      if((input$diurnalInput == TRUE || input$stabilityInput == TRUE) &
          input$initializationMethod != "wxModelInitialization"){
          selectInput("unitsInputCloudCover", "Units:",
                list("percent" = "percent", 
                     "fraction" = "fraction"))
      }
  })

  output$inputAirTempField <- renderUI({
      createInputAirTempBox()
  })
  output$unitsInputAirTempField <- renderUI({
      createUnitsAirTempButtons()
  })
  output$inputCloudCoverField <- renderUI({
      createInputCloudCoverBox()
  })
  output$unitsInputCloudCoverField <- renderUI({
      createUnitsCloudCoverButtons()
  })

#----------------------------------------------------------------------
#  Use map to choose DEM
#----------------------------------------------------------------------

  # Create reactive values object to store our markers, so we can show 
  # their values in a table.
  values <- reactiveValues(markers = NULL)
  
  # Create the map; this is not the "real" map, but rather a proxy
  # object that lets us control the leaflet map on the page.
  map <- createLeafletMap(session, 'map')
  
  bindEvent(input$map_click, function() {
    values$selectedCity <- NULL
    if (!input$addMarkerOnClick)
      return()
    map$addMarker(input$map_click$lat, input$map_click$lng, NULL)
    values$markers <- rbind(data.frame(lat=input$map_click$lat,
                                       long=input$map_click$lng),
                            values$markers)
  })
  
  bindEvent(input$clearMarkers, function() {
    map$clearMarkers()
    values$markers <- NULL
  })

#==============================================================================
#         TESTING
#============================================================================== 
  
    createTestMessage <- reactive({
      if(length(input$run_wn) > 0 ){
      paste("forecastDir = ", forecastDir, collapse = "")
      }
  })
  output$testMessage <- renderUI({
      createTestMessage()
  })
  
  
  
})  

