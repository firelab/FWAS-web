library(shiny)
library(windtools)
library(RSQLite)

#set some initial data
#db_src<-'/FVS/shiny-server/shinyWindTools/src.sqlite'
db_src<-'/home/natalie/src/hires-shiny/src.sqlite'

#db_bsb<-'/FVS/shiny-server/shinyWindTools/bsb.sqlite'
db_bsb<-'/home/natalie/src/hires-shiny/bsb.sqlite'

#sloooow:
#src_mindate<-dbFetch(db_src, "SELECT MINdate_time) FROM mean_flow_obs")
#set manually for now
src_mindate<-'2011-07-13 23:00:00'
src_maxdate<-'2011-09-14 03:13:30'
#src_plot_ids<-dbFetch(db_src, "SELECT DISTINCT plot_id FROM mean_flow_obs")
src_plot_ids<-c("K1", "K2", "NE1", "NE2", "NE3", "NE4",     
                "NM1", "NM2", "NM3", "NM4", "NW1", "NW2",     
                "NW3", "NW4", "Natalie1", "Natalie2", "Natalie3", "Natalie4",
                "SE1", "SE2", "SE3", "SE4", "SE5", "SM1",     
                "SM4", "SW2", "SW3", "SW4")  

bsb_mindate<-'2010-06-13 00:00:00'
bsb_maxdate<-'2010-09-10 13:01:32'
#bsb_plot_ids<-dbFetch(db_bsb, "SELECT DISTINCT plot_id FROM mean_flow_obs")
bsb_plot_ids<-c("R1", "R10", "R11", "R12", "R13", "R14", "R15", "R16",
                "R17", "R18", "R19", "R2", "R20", "R21", "R22", "R23", 
                "R24", "R25", "R26", "R27", "R28", "R29", "R3",  "R30",   
                "R31", "R32", "R33", "R34", "R35", "R4", "R5",  "R6",    
                "R7",  "R8",  "R9",  "TSW1", "TSW10", "TSW11", "TSW12", "TSW13", 
                "TSW2", "TSW3", "TSW4", "TSW5", "TSW6", "TSW7", "TSW8", "TSW9",  
                "TWSW1", "TWSW10", "TWSW11", "TWSW3",  "TWSW4",  "TWSW5",  "TWSW6",  "TWSW8", 
                "TWSW9")
    
# Define server logic
shinyServer(function(input, output) {
  
  # Compute the forumla text in a reactive expression
  formulaText <- reactive({
    paste("Wind Speed: ", input$variable)
  })

  # Return the formula text for printing as a caption
  output$caption <- renderText({
    formulaText()
  })

  output$setDates <- renderUI({ 
    if(input$site == 'SRC'){
      dateRangeInput('daterange', 'Date range:', 
                     start = "2011-08-10", #default start date
                     end = "2011-08-15", #default end date
                     min = src_mindate, 
                     max = src_maxdate)
    }
    else if(input$site == 'BSB'){
      dateRangeInput('daterange', 'Date range:', 
                     start = "2010-08-15", #default start date
                     end = "2010-08-20", #default end date
                     min = bsb_mindate,
                     max  = bsb_maxdate)
    }
  })

  output$selectUI <- renderUI({
    if(input$site == 'SRC'){
      selectInput('variable', 'Choose a sensor:', src_plot_ids)
    }
    else if(input$site == 'BSB'){
      selectInput('variable', 'Choose a sensor:', bsb_plot_ids)
    }
  })
  
  #Overview map of sites
  output$overviewMap <- renderPlot({
      library(maptools)
      library(maps)
      library(ggmap)
      #-------------------------------------
      #   make a US map with sites labeled
      #-------------------------------------
      xlim<-c(-125, -110)
      ylim<-c(42, 49)
      domain<-map("state", regions = c("idaho","Montana","Wyoming","oregon", "washington", "california", "Nevada", "utah",      "colorado", "new mexico", "arizona"), plot = FALSE, fill = TRUE)
      IDs<-sub("^idaho,", "", domain$names)
      domain_sp<-map2SpatialPolygons(domain, IDs, CRS("+proj=longlat"))
      sites<-cbind(-113.0283, 43.40202)
      sites<-rbind(sites, cbind(-116.2314, 45.40276))
      sp<-SpatialPoints(sites, proj4string=CRS("+proj=longlat +datum=WGS84"))
      plot(domain_sp, axes = TRUE, xlim=xlim, ylim=ylim)
      plot(sp, add=TRUE, pch = 19)
      text(-113, 43, "BSB")
      text(-115.6, 45.1, "SRC")
  })

  # Generate a plot of the requested sensor speed 
  output$speedPlot <- renderPlot({
     library(ggplot2)
     if(input$site == 'SRC'){
       start_time<-min(input$daterange)
       end_time<-max(input$daterange)
       s<-dbFetchSensor(db_src, input$variable, start_time, end_time)
     }
     else if(input$site == 'BSB'){
       start_time<-min(input$daterange)
       end_time<-max(input$daterange)
       s<-dbFetchSensor(db_bsb, input$variable, start_time, end_time)
       colnames(s)<-c("plot_id", "date_time", "wind_speed", "wind_gust", "wind_dir", "qualtiy", "sensor_qual")
     }
     
     p<-shinyPlotSensorSpeed(s)
     
     print(p)
  })

  # Generate a summary of the data
  output$summary <- renderPrint({
    if(input$site == 'SRC'){
         s<-dbFetchSensor(db_src, input$variable, min(input$daterange), max(input$daterange))
    }
    else if(input$site == 'BSB'){
         s<-dbFetchSensor(db_bsb, input$variable, min(input$daterange), max(input$daterange))
    }
    summary(s)
  })

  # Generate an HTML table view of the data
  output$table <- renderTable({
    if(input$site == 'SRC'){
         s<-dbFetchSensor(db_src, input$variable, min(input$daterange), max(input$daterange))
    }
    else if(input$site == 'BSB'){
         s<-dbFetchSensor(db_bsb, input$variable, min(input$daterange), max(input$daterange))
    }
    data.frame(x=s)
  })
})


