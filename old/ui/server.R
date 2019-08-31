#================================= 
#            FWAS
#=================================
##########################################################################
##
## Fire Weather Alert System
##
##########################################################################

library(shiny)
library(shinyjs)

#radarData<-read.csv(file="/media/tanner/vol2/NEXRAD_INFO/nexradID.csv",header=FALSE,sep=",")
radarData<-read.csv(file="/home/ubuntu/src/FWAS/data/nexradID.csv",header=FALSE,sep=",")
# dupePath<-"/home/tanner/src/breezy/checkForDupe.py"
dupePath<-"/home/ubuntu/src/FWAS/checkForDupe.py"
# fireData<-read.csv(file="/media/tanner/vol2/NIFC/incidents.csv")
fireData<-read.csv(file="/home/ubuntu/fwas_data/NIFC/incidents.csv")

##########################################################################
##
## Initial Stuff
##
##########################################################################



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

##########################################################################
##
## Start Server Code
##
##########################################################################

shinyServer(function(input, output, session) {
  
  stid<-""
  # addRunButton <- reactive({
  #   actionButton('run_wn', label ="Go!")
  # })

  output$runButton <- renderUI({
    addRunButton()
  })
  
  # addRunButtonText <- reactive({
  #   if(input$elevation == "boundingBox" || input$elevation == "centerLatLon" || length(input$demFile) > 0){
  #     if(length(input$run_wn) > 0){
  #       if(input$run_wn == 1){
  #         h4("Run finished!")
  #       }
  #       else{
  #         h4("Start run!")
  #       }
  #     }
  #   }
  #   else{
  #     paste("Specify the elevation input to get started.")
  #   }
  # })
  # 
  # output$runButtonText <- renderUI({
  #   addRunButtonText()
  # })
  
#######################################################
##                                                    #
## Location Finder Code and Fire Perimeter Code       #
##                                                    #
#######################################################

  onclick("locate",{js$func()})
  output$location<-renderUI({
    if (is.null(input$locationType))
      return()
    
    switch(input$locationType,
           "1" = tagList(
             numericInput("Lat", label = ("Enter Latitude (Decimal Degrees)"), value = 46.92,step=0.1),
             verbatimTextOutput("latVal"),
             numericInput("Lon", label = ("Enter Longitude (Decimal Degrees)"), value = -114.1,step=0.1),
             verbatimTextOutput("lonVal")),
           "2" = tagList(actionButton("locate","Allow Location Access"),br(),br(),verbatimTextOutput("glat"),verbatimTextOutput("glon")),
           "3" = tagList(
            div('NOTE: Selecting a Fire Location REPLACES the location set by a preset. Use \'Enter Lat/Lon\' if you want to use the preset location. ',style="color:blue"),
            hr(),selectInput('fire_name','Select Fire Location',
            c(Choose='',fireData[1]),selectize=TRUE),br(),
            verbatimTextOutput("fLat"),br(),
            verbatimTextOutput("fLon"))

           )
  })
  observeEvent(input$fire_name,{
      nLoc<-match(input$fire_name,fireData[[1]])
      output$fLat<-renderPrint(paste('Lat:',fireData[[3]][nLoc],sep=""))
      output$fLon<-renderPrint(paste('Lon:',fireData[[2]][nLoc],sep=""))
#       fireLat<-renderPrint(fireData[[3]][nLoc])
#       fireLon<-renderPrint(fireData[[2]][nLoc])
  })

  output$glat<-renderPrint(paste('Lat:',input$geoLat,sep=" "))
  output$glon<-renderPrint(paste('Lon:',input$geoLon,sep=" "))
  aCheck<-reactive({
    validate(
      need(input$locationType==1,paste("Using Geolocation:",input$geoLat,input$geoLon,sep=" ")),
      need(input$locationType==2,paste("Using Specified Lat/Lon:",input$Lat,input$Lon,sep=" "))
      # need(input$geolocation==TRUE,paste("Geolocation services are disalbed/unavailable/denied, Please Try again or manually enter Lat/Lon"))
    )
    # validate(
    #  need(input$geolocation==TRUE,paste("Geolocation services are disalbed/unavailable/denied, Please Try again or manually enter Lat/Lon"))
    #   
    # )
    # if (input$geolocation==TRUE && input$locationType=="2")
    # {
    #   b_arg<-renderPrint("GEOLOC TO BE USED!")
    # }
    
  })
  output$bCheck<-renderPrint({aCheck()})
  # gWarn<-reactive({
  #   validate(
  #     need(!is.null(input$geolocation),paste("")),
  #     need((is.null(input$geolocation) & input$geolocation==FALSE),paste("DENIED"))
  #     # need((input$geolocation!=FALSE),paste("Geolocation services are disalbed/unavailable/denied, Please Try again or manually enter Lat/Lon")),
  #     # need(input$geolocation=="TRUE",paste(""))
  #     )
  # })
  # output$gCheck<-renderPrint({gWarn()})

  
##########################################################################
##
## Vary The UI based on User Requests
##
##########################################################################
#  output$address <- renderUI({
#    if (is.null(input$not_type))
#      return()
#    
#    # Depending on input$input_type, we'll generate a different
#    # UI component and send it to the client.
#    switch(input$not_type,
#           "email" = textInput("emailAddress", "Enter Notifcation Email Address",
#                               value = "fsweather1@usa.com"),
#           "text" = textInput("textMessage", "Enter Phone Number (no Dashes)",
#                              value = "5556667777")
#    )
#  })
#  output$carrier<-renderUI({
#    if (is.null(input$not_type))
#      return()
#    switch(input$not_type,
#           
#           "text" = selectInput("carrier","Select Carrier",choices=list("AT&T"="att","Verizon"="verizon","Sprint"="sprint","T-Mobile"="tmobile","Virgin Mobile"="virgin"),selected = 1)
#    )
#  })
##########################################################################
##
## Sanity Checks: Check to make sure user inputs are legal/reasonable
##
##########################################################################
  latNum<-reactive({
    validate(
      
      need(is.numeric(input$Lat),"Please Input A Valid Latitude (00.00) (Decimal Degrees)")
#       need(input$Lat>0,"WARNING! Please choose a Latitude in North America.")
    )
  })
  output$latVal<-renderPrint({latNum()})
  
  lonNum<-reactive({
    validate(
      
      need(is.numeric(input$Lon),"Please Input A Valid Longitude (00.00) (Decimal Degrees)"),
      need(input$Lon<0,"WARNING! Longitude Must Be Negative!")
    )
  })
  output$lonVal<-renderPrint({lonNum()})
  
output$lonVal2<-renderPrint({lonNum()})
output$latVal2<-renderPrint({latNum()})
observeEvent(input$radius,{
#     output$radiusOut<-renderText(input$radius)
    output$radiusOut<-renderText(paste("Radius set to: ",input$radius," miles; ",round(input$radius*1.60934,digits=2)," kilometers",sep=""))


})
observeEvent(input$expire,{
    if (input$expire<48)
    {
      output$slideOut<-renderText({paste("Alert will expire in ",input$expire," Hours",sep="")})
    }
    if (input$expire>=48)
    {
#       output$slideOut<-renderText(paste("Alert will expire in ",round(input$expire/24,digits = 2)," Days (",input$expire," hours)",sep=""))
      dInt<-as.integer(input$expire/24)
      rHour<-input$expire-dInt*24
      
      if (rHour>0){
        output$slideOut<-renderText(paste("Alert will expire in ",dInt,
                                          " days and ",rHour," hours",sep=""))
      }
      if (rHour==0){
        output$slideOut<-renderText(paste("Alert will expire in ",dInt," days",sep=""))
      }
    }
})



  
  rHNum<-reactive({
    validate(
      need(is.numeric(input$RelativeHumidity),"Please Input A Valid Relative Humidity.")
    )
  })
  output$rHVal<-renderPrint({rHNum()})
  
  windSpeedNum<-reactive({
    validate(
      need(is.numeric(input$wind_speed),"Please Input A Valid Wind Speed.")
    )
  })
  output$windSpeedVal<-renderPrint({windSpeedNum()})
  
  gustNum<-reactive({
    validate(
      need(is.numeric(input$gust),"Please Input A Valid Wind Gust Speed")
    )
  })
  output$gustVal<-renderPrint({gustNum()})
  
  
  temperatureNum<-reactive({
    validate(
      need(is.numeric(input$temp),"Please Input A Valid Temperature.")
    )
  })
  output$tempVal<-renderPrint({temperatureNum()})
  
  nameChecker<-reactive({
    validate(
      need(input$runName!="","WARNING! No Alert Name has been set! YOU WILL NOT RECEIVE AN ALERT!")
    )
  })
  output$nameCzecher<-renderPrint({nameChecker()})
  
  notifChecker<-reactive({
    validate(
      need(input$email!=FALSE || input$nText!=FALSE,"WARNING! No notifcation information has been provided! YOU WILL NOT RECEIVE AN ALERT!")
    )
  })
  output$notifCzecher<-renderPrint({notifChecker()})
##########################################################################
##
## Updates Inputs based on Presets (See UI.R for preset options)
##
##########################################################################
  
  observeEvent(input$presets,{
    x<-input$presets
    
    if (x==1)
    {
      updateNumericInput(session,"RelativeHumidity",value=20)
      updateNumericInput(session,"wind_speed",value=10)
      updateNumericInput(session,"gust",value=15)
      updateNumericInput(session,"temp",value=80)
      # updateNumericInput(session,"RelativeHumidity",value=20)
      updateCheckboxInput(session,"precip",value=TRUE)
      updateTextInput(session,"runName",value="")
      updateNumericInput(session,"Lat",value=46.92)
      updateNumericInput(session,"Lon",value=-114.1)
    }
    if (x==2)
    {
      updateNumericInput(session,"RelativeHumidity",value=20)
      updateNumericInput(session,"wind_speed",value=10)
      updateNumericInput(session,"gust",value=20)
      updateNumericInput(session,"temp",value=89)
      updateCheckboxInput(session,"precip",value=FALSE)
      updateTextInput(session,"runName",value="Sapphire Complex Preset")
      updateNumericInput(session,"Lat",value=46.588)
      updateNumericInput(session,"Lon",value=-113.584)
    }
  })

  
##########################################################################
##
## Enable/Disable Elements based on user requests
##
##########################################################################
  
#   shinyjs::disable('tStorm')

  observeEvent(input$email,{
    shinyjs::toggleState('emailAddress')
  })
  observeEvent(input$nText,{
    shinyjs::toggleState('textMessage')
    shinyjs::toggleState('carrier')
  })
  
##########################################################################
##
## Check For Duplicates in Alert Name & Email
##
##########################################################################

  duplicate_name<-reactive({
    email_arg="_"
    text_arg="_"
    
    if (input$email==TRUE)
    {
      email_arg<-input$emailAddress
    }
    if (input$email==FALSE)
    {
      email_arg<-"_"
    }
    if (input$nText==TRUE)
    {
      text_arg<-input$textMessage
    }
    if (input$nText==FALSE)
    {
      text_arg<-"_"
    }
    
    name_arg<-input$runName
    if (name_arg=="")
    {
      name_arg<-"_"
    }
    if (input$emailAddress=="")
    {
      email_arg<-"_"
    }
    if (input$textMessage=="")
    {
      text_arg<-"_"
    }
    
#     gArgs=paste(name_arg,email_arg,text_arg,sep=" ")
    gArgs=paste("\"",name_arg,"\" \"",email_arg,"\" \"",text_arg,"\"",sep="")   
    dupeCheck<-system2(command=dupePath,args=gArgs,stdout=TRUE)
    validate(
      need(dupeCheck!='TrueBoth',paste("WARNING! Alert Name:",input$runName,"Already exists for",input$emailAddress,"and",input$textMessage,"Please Choose Another Alert Name.",sep=" ")),
      need(dupeCheck!='TrueEmail',paste("WARNING! Alert Name:",input$runName,"Already exists for",input$emailAddress,"Please Choose Another Name.",sep=" ")),
      need(dupeCheck!='TruePhone',paste("WARNING! Alert Name:",input$runName,"Already exists for",input$textMessage,"Please Choose Another Name.",sep=" "))
      
      
      )   
  })
  output$dupe<-renderPrint({duplicate_name()})
  output$dupe2<-renderPrint({duplicate_name()})

  
##########################################################################
##
## Controls for NEXRAD Data, this is not available and not used right now
##
##########################################################################
  
  observeEvent(input$nex,{
    # shinyjs::disable('radarName')
    shinyjs::toggleState('radarName')
    
  })
  observeEvent(input$radarName,{
    nLoc<-match(input$radarName,radarData[[2]])
    stid<<-radarData[[1]][nLoc]
  })
##########################################################################
##
## Controls for  run_wn Button
##
##########################################################################
  
  #Change run button base on Alert Name
  observeEvent(input$runName,{
    # shinyjs::disabled(input$run_wn)
    if (input$runName==""){
      shinyjs::disable("run_wn")
    }
    if (input$runName!=""){
      shinyjs::enable("run_wn")
    }
  })
  
##########################################################################
##
## Write Config File
##
##########################################################################
  
  
  writeCfg <- reactive({
    # isolate({
      fileLoc<-paste("threshold-","USERNAME","-",format(Sys.time(),"%Y-%m-%d_%H-%-M-%S"),".cfg",sep="")
      cfg<-paste("/srv/shiny-server/fwas/data/",fileLoc,sep="")
      # cfg<-"/home/tanner/src/FWAS/ui/thresholds/threshold.cfg"
      #cfg<-paste("/home/tanner/src/breezy/fwas/data/",fileLoc,sep="")
      cat("[FWAS_Threshold_File]\n",file=cfg)
      cat(paste("alert_name = ",input$runName,"\n",collapse=""),file=cfg,append=TRUE)
      if (input$locationType==1) #Use Lat/Lon
      {
        cat(paste("latitude = ",input$Lat,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("longitude = ",input$Lon,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if (input$locationType==2) #Use GeoLocation
      {
        cat(paste("latitude = ",input$geoLat,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("longitude = ",input$geoLon,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if (input$locationType==3) #Use Fire Location
      {
        naLoc<-match(input$fire_name,fireData[[1]])
        fireLat<-fireData[[3]][naLoc]
        fireLon<-fireData[[2]][naLoc]
        cat(paste("latitude = ",fireLat,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("longitude = ",fireLon,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat(paste("radius = ",input$radius,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("limit = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("time_zone = ",input$timeZone,"\n",collapse=""),file=cfg,append=TRUE)
      if (input$email==TRUE)
      {
        cat(paste("email = ",input$emailAddress,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if (input$email==FALSE)
      {
        cat(paste("email = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if (input$nText==TRUE)
      {
        cat(paste("phone = ",input$textMessage,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("carrier = ",input$carrier,"\n",collapse=""),file=cfg,append=TRUE)      
      }
      if (input$nText==FALSE)
      {
        cat(paste("phone = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("carrier = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)   
      }
#      if(input$not_type=="email")
#      {
#        cat(paste("email = ",input$emailAddress,"\n",collapse=""),file=cfg,append=TRUE)
#        cat(paste("phone = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
#        cat(paste("carrier = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
#        # identifier<-input$emailAddress
#      }
#      if(input$not_type=="text")
#      {
#        cat(paste("email = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
#        cat(paste("phone = ",input$textMessage,"\n",collapse=""),file=cfg,append=TRUE)
#        cat(paste("carrier = ",input$carrier,"\n",collapse=""),file=cfg,append=TRUE)
#        # identifier<-input$textMessage
#      }
      cat(paste("alert_time = ",Sys.time(),"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("expires_after = ",input$expire,"\n",collapse=""),file=cfg,append=TRUE)

      cat("[Threshold_Values]\n",file=cfg,append=TRUE)
      if(input$addRH==TRUE)
      {
        cat(paste("relative_humidity = ", input$RelativeHumidity, "\n", collapse=""), file=cfg,append=TRUE)
      }
      if(input$addRH==FALSE)
      {
        cat(paste("relative_humidity = ",NaN, "\n", collapse=""), file=cfg,append=TRUE)
      }
      if(input$addWS==TRUE)
      {
        cat(paste("wind_speed = ", input$wind_speed,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addWG==TRUE)
      {
        cat(paste("wind_gust = ",input$gust,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addWS==FALSE)
      {
        cat(paste("wind_speed = ", NaN,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("wind_gust = ", NaN,"\n",collapse=""),file=cfg,append=TRUE)
        
      }
      if(input$addWG==FALSE)
      {
        cat(paste("wind_gust = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
      }
      # cat(paste("wind_direction = ", input$wind_direction,"\n",collapse=""),file=cfg,append=TRUE)
      if(input$addT==TRUE)
      {
       cat(paste("temperature = ", input$temp,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addT==FALSE)
      {
        cat(paste("temperature = ", NaN,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat("[Threshold_Units]\n",file=cfg,append=TRUE)
      if(input$addWS==TRUE)
      {
        cat(paste("wind_speed_units = ", input$wind_speed_units,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addWS==FALSE)
      {
        cat(paste("wind_speed_units = ", NaN,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addT==TRUE)
      {
        cat(paste("temperature_units = ", input$temp_units,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$addT==FALSE)
      {
        cat(paste("temperature_units = ", NaN,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat("[HRRR_Options]\n",file=cfg,append=TRUE)
#       if(input$fCast==TRUE)
#       {
      cat(paste("forecast_on = ",1, "\n", collapse=""), file=cfg,append=TRUE)
#       }
#       if(input$fCast==FALSE)
#       {
#         cat(paste("forecast_on = ",0, "\n", collapse=""), file=cfg,append=TRUE)
#       }
      cat(paste("forecast_duration = ",6, "\n", collapse=""), file=cfg,append=TRUE)
      cat("[Precipitation]\n",file=cfg,append=TRUE)
      if(input$precip==TRUE)
      {
        cat(paste("precip_on = ",1,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$precip==FALSE)
      {
        cat(paste("precip_on = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat(paste("precip_units = ",input$precip_units, "\n", collapse=""), file=cfg,append=TRUE)
      cat("[NEXRAD_Options]\n",file=cfg,append=TRUE)
      cat(paste("radar_on = ",1,"\n",collapse=""),file=cfg,append=TRUE)
#       if(input$tStorm==TRUE)
#       {
#         cat(paste("radar_on = ",1,"\n",collapse=""),file=cfg,append=TRUE)
#       }
#       if(input$tStorm==FALSE)
#       {
#         cat(paste("radar_on = ",0,"\n",collapse=""),file=cfg,append=TRUE)
#       }
      cat(paste("radar_name = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("radar_time = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      
      cat("[WWA_Options]\n",file=cfg,append=TRUE)
      if(input$wwa==TRUE)
      {
        cat(paste("wwa_on = ",1,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat(paste("wwa_time = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      if(input$wwa==FALSE)
      {
        cat(paste("wwa_on = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      }
      cat("[THUNDERSTORM_Options]\n",file=cfg,append=TRUE)
      if(input$tStorm==TRUE)
      {
        cat(paste("thunderstorm_on = ",1,"\n",collapse=""),file=cfg,append=TRUE)
      }
      if(input$tStorm==FALSE)
      {
        cat(paste("thunderstorm_on = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      }

#       if(input$nex==TRUE)
#       {
   
#       }
#       if(input$nex==FALSE)
#       {
#         cat(paste("radar_on = ",0,"\n",collapse=""),file=cfg,append=TRUE)
#         cat(paste("radar_name = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
#       }
      
      return(cfg)
    # })
  })
  # runWN <- reactive({
  #   # if(length(input$run_wn) > 0 && input$run_wn == 1){
  # observeEvent(input$run_wn,{
  #   skaCfg<-writeCfg()
  #   system(paste("/home/tanner/src/breezy/FWAS/instantAlert.py",skaCfg,sep=" "))
  #   # system(paste("/home/ubuntu/src/FWAS/instantAlert.py",skaCfg,sep=" "))
  # })
  
##########################################################################
##
## Run Button: Runs Initial Alert Py and 
## Hides Run Button to prevent Duplicates
##
##########################################################################
  useShinyjs()
#   observe({
#     if (input$alert_name=="")
#     {
#     shinyjs::hide("run_wn")
#     }
#     if (input$alert_name!="")
#     {
#     shinyjs::show("run_wn")
#     }
#   })
  observe({
    if(input$run_wn>0)
    {      
      output$runResult<-renderPrint("Alert Created! Reload the App to create another Alert.")
      shinyjs::hide("run_wn")
    }
    
    if(input$run_wn==0)
      shinyjs::show("run_wn")
    # shinyjs::show("ska")
  })
  observeEvent(input$run_wn,{
    skaCfg<-writeCfg()
    #system(paste("/home/tanner/src/breezy/FWAS/instantAlert.py",skaCfg,sep=" "))
    system(paste("/home/ubuntu/src/FWAS/instantAlert.py",skaCfg,sep=" "))
  })
  #     
      # withProgress(session, min=1, max=15, {
      #   i = 1
      #   unlink ("wnpipe")
      #   system("mkfifo wnpipe")
      #   
      #   system(paste("NINJA_FILL_DEM_NO_DATA=YES", "/home/natalie/src/windninja/build/src/cli/WindNinja_cli", 
      #                "windninja.cfg", ">> wnpipe"
      #   ), intern=FALSE, wait=FALSE)
      #   fileName="wnpipe"
      #   con=fifo(fileName,open="rt",blocking=TRUE)
      #   linn = " "
      #   while ( length(linn) > 0) {
      #     i = i + 1
      #     linn=scan(con,nlines=1,what="character", sep=" ", quiet=TRUE)
      #     setProgress(message = 'WindNinja is running.',
      #                 detail = paste(linn, collapse=" "), value = i)
      #   }
      #   close(con)
      #   unlink ("wnpipe")
      # })
    # }
  # })
  
  # output$wnText <- renderPrint({
  #   runWN()
  # })

  createRelativeHumidityBox <- reactive({
    textInputRow("RelativeHumidity", "Relative Humidity (%):", "50")
  })
  

  output$RelativeHumidityField <- renderUI({
    createRelativeHumidityBox()
  })

})  

