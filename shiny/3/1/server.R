#================================= 
#            FWAS
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

shinyServer(function(input, output, session) {
  
  addRunButton <- reactive({
    actionButton('run_wn', label ="GO Mokulele!")
  })

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
  
  #-----------------------------------------------------
  #    write the cfg
  #-----------------------------------------------------   
  
  writeCfg <- reactive({
    # isolate({
      cfg<-"threshold.txt"
      cat(paste("relative_humidity = ", input$RelativeHumidity, "\n", collapse=""), file=cfg, append=FALSE)

    # })
  })
  
  # runWN <- reactive({
  #   # if(length(input$run_wn) > 0 && input$run_wn == 1){
  observeEvent(input$run_wn,{
    writeCfg()
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

