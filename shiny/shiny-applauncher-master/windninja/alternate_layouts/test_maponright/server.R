library(leaflet)
library(ggplot2)
library(maps)

data(uspop2000)

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

shinyServer(function(input, output, session) {
    runWNtextOut <- reactive({
        if(input$run_wn == 1){
            print("WindNinja is running...")
        }
    })
    
    output$wnRunningText <- renderText({
        runWNtextOut()
    })
    
    runWN <- reactive({
      if(input$run_wn == 1){
         L<-system2("/home/natalie/windninja_trunk/build/src/cli/./WindNinja_cli", "/home/natalie/windninja_trunk/test_runs/bigbutte_domainAvg.cfg", stdout=TRUE, stderr=TRUE)
         paste(L, sep="\n")
      }
    })
    
    runWN2 <- reactive({
      if(input$run_wn == 1){
         unlink ("wnpipe")
         system("mkfifo wnpipe")
         system("/home/natalie/windninja_trunk/build/src/cli/./WindNinja_cli /home/natalie/windninja_trunk/test_runs/bigbutte_domainAvg.cfg > wnpipe &")
         Sys.sleep (2)
         fileName="wnpipe"
         con=fifo(fileName,open="rt",blocking=TRUE)
         linn = " "
         while ( length(linn) > 0) {
           linn=scan(con,nlines=1,what="character", sep=" ", quiet=TRUE)
           cat(linn,"\n") #flush.console()
         }
         close(con)
         unlink ("wnpipe") 
       }
    })
    
    
    output$wn_progress <- renderText({
        runWN()
    })
    
  output$text1 <- renderText({ 
      paste("WindNinja messages could be directed here. Press the button and wait",
             "for a few seconds (to let the run finish) to see the output below. Should be able to pipe this in line by line",
             "so user can see status. For now it's just being read in as a full stream once the process ends.", collapse="")
    })



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
})  

