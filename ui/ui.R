#================================= 
#            FWAS
#=================================

library(shiny)
library(shinythemes)
library(shinyjs)


shinyUI(fluidPage(
  theme = shinythemes::shinytheme("cosmo"),
  
    fluidRow(
      column(12,
             h2('FWAS')
      )),


    
    fluidRow(
      column(12,
             h3('Set Location')
      )
    ),
    hr(),
    fluidRow(
      column(5,wellPanel(
             numericInput("Lat", label = ("Enter Latitude"), value = 46.92,step=0.1),
             verbatimTextOutput("latVal"),
             numericInput("Lon", label = ("Enter Longitude"), value = -114.10,step=0.1),
             verbatimTextOutput("lonVal")),
             sliderInput("radius", label = h3("Grab Stations within a radius of: (miles)"), min = 0, 
                         max = 25, value = 12)
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),
             
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),

      ),
      column(5,
             selectInput("timeZone", label = ("Select Time Zone"), 
                         choices = list("America/Los_Angeles" = 1, "America/Denver" = 2, "America/Phoenix" = 3,"America/Chicago" = 4,"America/New_York"=5), 
                         selected = 2),
             # sliderInput("limit", label = h3("Maximum Number of Stations"), min = 0, 
             #             max = 10, value = 5),
             sliderInput("expire", label = h3("Alert Expires After: (hours)"), min = 0, 
                         max = 10, value = 5),
             br(),br(),br(),
             wellPanel(textInput("runName",label="Name Your Alert",value="alert"))
             
             # textInput("email",label=("Enter Notification Email Address"),value="fsweather1@usa.com")
             # textInput("RelativeHumidity", label = ("Relative Humidity (%)"), value = "50")
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),


      )

    ),
    fluidRow(
      column(12,h3("Select Notifcation Type"))
      ),
    hr(),
    wellPanel(
    fluidRow(
      column(3,
      radioButtons("not_type","",choices=list("email"="email","text message"="text"))),
      column(4, 
             uiOutput("address")),
      column(3,                
             uiOutput("carrier"))
             )),
    fluidRow(
      column(12,
             h3('Set Thresholds')
      )
    ),
    hr(),
    fluidRow(
      column(5,
             wellPanel(checkboxInput("addRH", label = "Add Relative Humidity?", value = TRUE),
             numericInput("RelativeHumidity", label = ("Relative Humidity (%)"), value = 75,step=0.5),
             verbatimTextOutput("rHVal")),
             wellPanel(checkboxInput("addWS", label = "Add Wind Speed?", value = TRUE),
             numericInput("wind_speed", label = ("Enter Wind Speed"), value = 2, step=0.5),
             verbatimTextOutput("windSpeedVal"),
             checkboxInput("addWG",label="Add Wind Gusts?",value = TRUE),
             numericInput("gust",label=("Enter Wind Gust"),value=10,step=1),
             verbatimTextOutput("gustVal"),
             selectInput("wind_speed_units", label = ("Wind Speed Units"), 
                         choices = list("meters per second (mps)" = 1, "miles per hour (mph)" = 2), 
                         selected = 2))
             # textInput("wind_direction", label = ("Enter Change in Wind Direction"), value = 180),


      ),
      column(5,
            wellPanel(
            checkboxInput("addT", label = "Add Temperature?", value = TRUE),
            numericInput("temp", label = ("Enter Temperature"), value = 5,step=1),
            verbatimTextOutput("tempVal"),
            selectInput("temp_units", label = ("Temperature Units"), 
                        choices = list("Celcius (C)" = 1, "Farenheit (F)" = 2), 
                        selected = 2))

            )

    ),
    fluidRow(
      column(3, h3('Create Alert'))
    ),
    hr(),
    useShinyjs(),
    fluidRow(
      # column(2, htmlOutput('runButton'))
      column(2, actionButton('run_wn', label="Go!"))),
      fluidRow(
      column(8,verbatimTextOutput("runResult"))),
    hr(),
    fluidRow(
      column(4, htmlOutput('wnText'), style = "color:darkblue"),
      br()
    ),

    br()
))
