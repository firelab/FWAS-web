#================================= 
#            FWAS
#=================================

library(shiny)
library(shinyjs)


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

shinyServer(function(input, output, session) {
  
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
  output$address <- renderUI({
    if (is.null(input$not_type))
      return()
    
    # Depending on input$input_type, we'll generate a different
    # UI component and send it to the client.
    switch(input$not_type,
           "email" = textInput("emailAddress", "Enter Notifcation Email Address",
                               value = "fsweather1@usa.com"),
           "text" = textInput("textMessage", "Enter Phone Number (no Dashes)",
                              value = "5556667777")
    )
  })
  output$carrier<-renderUI({
    if (is.null(input$not_type))
      return()
    switch(input$not_type,
           
           "text" = selectInput("carrier","Select Carrier",choices=list("AT&T"="att","Verizon"="verizon","Sprint"="sprint","T-Mobile"="tmobile","Virgin Mobile"="virgin"),selected = 1)
    )
  })
  
  latNum<-reactive({
    validate(
      
      need(is.numeric(input$Lat),"Please Input A Valid Latitude (00.00)")
    )
  })
  output$latVal<-renderPrint({latNum()})
  
  lonNum<-reactive({
    validate(
      
      need(is.numeric(input$Lon),"Please Input A Valid Longitude (00.00)")
    )
  })
  output$lonVal<-renderPrint({lonNum()})
  
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
  
  # skaCfg<-""
  
  writeCfg <- reactive({
    # isolate({
      fileLoc<-paste("threshold-","USERNAME","-",format(Sys.time(),"%Y-%m-%d_%H-%-M-%S"),".cfg",sep="")
      cfg<-paste("/home/tanner/src/FWAS/ui/thresholds/",fileLoc,sep="")
      # cfg<-"/home/tanner/src/FWAS/ui/thresholds/threshold.cfg"
      cat("[FWAS_Threshold_File]\n",file=cfg)
      cat(paste("alert_name = ",input$runName,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("latitude = ",input$Lat,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("longitude = ",input$Lon,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("radius = ",input$radius,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("limit = ",0,"\n",collapse=""),file=cfg,append=TRUE)
      cat(paste("time_zone = ",input$timeZone,"\n",collapse=""),file=cfg,append=TRUE)
      if(input$not_type=="email")
      {
        cat(paste("email = ",input$emailAddress,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("phone = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("carrier = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
        # identifier<-input$emailAddress
      }
      if(input$not_type=="text")
      {
        cat(paste("email = ",NaN,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("phone = ",input$textMessage,"\n",collapse=""),file=cfg,append=TRUE)
        cat(paste("carrier = ",input$carrier,"\n",collapse=""),file=cfg,append=TRUE)
        # identifier<-input$textMessage
      }
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
      return(cfg)
      # skaCfg<-cfg
    # })
  })
  # runWN <- reactive({
  #   # if(length(input$run_wn) > 0 && input$run_wn == 1){
  observeEvent(input$run_wn,{
    skaCfg<-writeCfg()
    # system(paste("/home/tanner/src/FWAS/instantAlert.py",skaCfg,sep=" "))
  })
  useShinyjs()
  observe({
    if(input$run_wn>0)
    {
      shinyjs::hide("run_wn")
      output$runResult<-renderPrint("Alert Created! Reload the App to create another Alert.")
    }
    
    if(input$run_wn==0)
      shinyjs::show("run_wn")
    # shinyjs::show("ska")
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

