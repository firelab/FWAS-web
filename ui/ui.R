#================================= 
#            FWAS
#=================================

library(shiny)
library(shinythemes)
library(shinyjs)
#radarData<-read.csv(file="/media/tanner/vol2/NEXRAD_INFO/nexradID.csv",header=FALSE,sep=",")
radarData<-read.csv(file="/home/ubuntu/src/FWAS/data/nexradID.csv",header=FALSE,sep=",")

shinyUI(fluidPage(
  theme = shinythemes::shinytheme("cosmo"),
  tags$head(tags$title('FWAS Fire Weather Alert System')),

  
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
             sliderInput("radius", label = h3("Grab stations within a radius of: (miles)"), min = 1, 
                         max = 50, value = 12)
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),
             
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),

      ),
      column(5,
	     wellPanel(textInput("runName",label="Alert Name",value="Alert"),
             
             selectInput("timeZone", label = ("Select Time Zone"), 
                         choices = list("America/Los_Angeles" = 1, "America/Denver" = 2, "America/Phoenix" = 3,"America/Chicago" = 4,"America/New_York"=5,"Pacific/Honolulu"=6,"America/Anchorage"=7), 
                         selected = 2)),
             # sliderInput("limit", label = h3("Maximum Number of Stations"), min = 0, 
             #             max = 10, value = 5),
             sliderInput("expire", label = h3("Alert Expires After: (hours)"), min = 1, 
                         max = 48, value = 24)
            #br(),br(),br(),
             #wellPanel(textInput("runName",label="Name Your Alert",value="alert"))
             
             # textInput("email",label=("Enter Notification Email Address"),value="fsweather1@usa.com")
             # textInput("RelativeHumidity", label = ("Relative Humidity (%)"), value = "50")
             # div(style = "display:inline-table", htmlOutput("RelativeHumidityField")),


      )

    ),
    fluidRow(
      column(12,h3("Select Notifcation Type"),            verbatimTextOutput("dupe"))
      ),
    hr(),
  wellPanel(
    fluidRow(
      column(7,
      checkboxInput("email",label=("Enable Email Notificaitons")),
      textInput("emailAddress", "Enter Notifcation Email Address", value = "fsweather1@usa.com")
      )
    
      
    ),
    fluidRow(
      column(7,
             checkboxInput("nText",label=("Enable Text Message Notifications")),
             column(8,textInput("textMessage", "Enter Phone Number (no Dashes)", value = "5556667777")),
             column(4,selectInput("carrier","Select Carrier",choices=list("AT&T"="att","Verizon"="verizon","Sprint"="sprint","T-Mobile"="tmobile","Virgin Mobile"="virgin","Boost Mobile"="boost","U.S. Cellular"="uscellular","Metro PCS"="metro","Cricket Wireless"="cricket","Project Fi"="projectfi"),selected = 1)
             
             
             )
    )
  )
  ),
#    wellPanel(
#    fluidRow(
#      column(3,
#      radioButtons("not_type","",choices=list("email"="email","text message"="text"))),
#      column(4, 
#             uiOutput("address")),
#      column(3,                
#             uiOutput("carrier"))
#             )),
  fluidRow(
    column(12,
           h3('Select Data Sources'),
           ('RAWS Fetching is currently required, HRRR Forecasts are optional. Enabling HRRR also enables forecasted lightning and storm alerts. HRRR data is currently only available for the continential United States.')
           # ('RAWS fetching is enabled by continental, Short term weather forecasts can be enabled via the HRRR.')
           )
),  
  hr(),    
  wellPanel(
  fluidRow(
    column(4,
           checkboxInput("raws",label = "Fetch Real Time RAWS Data",value = TRUE)
           
           
           ),
    column(4,
           # wellPanel(
             checkboxInput("fCast",label="Short Term Weather Forecasts (HRRR)", value=TRUE)
             # sliderInput("fDur", label = ("Forecast Duration (hours)"), min = 1, 
             #             max = 6, value = 1)
           )

    )
  ),
  wellPanel(
    fluidRow(
      column(2,
             checkboxInput("nex",label="Radar (NEXRAD)",value=FALSE)
      ),
      # verbatimTextOutput('radarNameOut'),
      # verbatimTextOutput('radarID'),
      # column(4,
      #          selectInput('radarName', 'Select Radar Station', c(Choose='', radarData[2]), selectize=TRUE)
      # ),
      column(4,
             ('Enable NEXRAD for storm alerts. Radar stations update every 15 minutes, and have a maximum range of 145 miles (230km).'),
             br(), 
             a('Radar Coverage Maps',href="https://www.roc.noaa.gov/WSR88D/Maps.aspx",target="_blank"),
             br(),
             a('National Radar Mosaic',href="http://www.weather.gov/Radar",target="_blank")
             ),
      column(4,('Radar Alerts will update every 20 minutes. Data is acquired from the CONUS Base Reflectivity Radar Mosaic. Radar Data is currently only available for the continental United States.'))
      
      
    )
  ),
#  wellPanel(
#    fluidRow(
#      column(2,
#             checkboxInput("nex",label="Radar (NEXRAD)",value=FALSE)
#      ),
#      # verbatimTextOutput('radarNameOut'),
#      # verbatimTextOutput('radarID'),
#      column(4,
#               selectInput('radarName', 'Select Radar Station', c(Choose='', radarData[2]), selectize=TRUE)
#      ),
#      column(4,
#             ('Enable NEXRAD for storm alerts. Radar stations update every 15 minutes, and have a maximum range of 145 miles (230km).'),
#             br(), 
#             a('Radar Coverage Maps',href="https://www.roc.noaa.gov/WSR88D/Maps.aspx",target="_blank"),
#             br(),
#             a('National Radar Mosaic',href="http://www.weather.gov/Radar",target="_blank")
#             )
#      
#    )
#  ),
  # column(2,br()),
  
  
  
    fluidRow(
      column(12,
             h3('Set Thresholds'),
	       ('Enable checks for various weather variables and enter threshold values'),
		br(),
	       ('Each threshold is independent of the other thresholds')
      )
    ),
    hr(),
    fluidRow(
      column(5,
             wellPanel(checkboxInput("addRH", label = "Relative Humidity", value = TRUE),
                       ('Alerts will be generated when relative humidity is less than the specified value.'),
             numericInput("RelativeHumidity", label = ("Relative Humidity (%)"), value = 75,step=0.5),
             verbatimTextOutput("rHVal")),
             wellPanel(checkboxInput("addWS", label = "Wind Speed", value = TRUE),
                       ('Alerts will be generated when wind speed exceeds the set value.'),
             numericInput("wind_speed", label = ("Enter Wind Speed"), value = 2, step=0.5),
             verbatimTextOutput("windSpeedVal"),
             checkboxInput("addWG",label="Wind Gusts",value = TRUE),
             numericInput("gust",label=("Enter Wind Gust"),value=10,step=1),
             verbatimTextOutput("gustVal"),
             selectInput("wind_speed_units", label = ("Wind Speed Units"), 
                         choices = list("meters per second (mps)" = 1, "miles per hour (mph)" = 2), 
                         selected = 2))
             # textInput("wind_direction", label = ("Enter Change in Wind Direction"), value = 180),


      ),
      column(5,
            wellPanel(
            checkboxInput("addT", label = "Temperature", value = TRUE),
            ('Alerts will be generated when temperature exceeds the set value.'),
            numericInput("temp", label = ("Enter Temperature"), value = 5,step=1),
            verbatimTextOutput("tempVal"),
            selectInput("temp_units", label = ("Temperature Units"), 
                        choices = list("Celcius (C)" = 1, "Farenheit (F)" = 2), 
                        selected = 2)),
            # ('Enable HRRR to monitor weather forecasts for set thresholds.'),
            # hr()
            wellPanel(
              checkboxInput("precip",label="Precipitation", value=FALSE),
              ('Enable for forecasted rain and recorded RAWS station precip.'),
              selectInput("precip_units", label = ("Precip Units"), 
                          choices = list("millimeters (mm)" = 1, "inches (in)" = 2), 
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
    br(),
    fluidRow(column(4,('Clicking Go! will send an email immediately and then every hour afterwards until expiration'))),
    hr(),
    fluidRow(
      column(4, htmlOutput('wnText'), style = "color:darkblue"),
      br()
    ),
    fluidRow( 
      column(4,tags$p("Data Sources"),	tags$a(href="https://synopticlabs.org/api/mesonet/",tags$img(src = "/ninja/fwas_images/meso-api-logo-dark.png", width = "292px", height = "50px"))),
      column(5,br(),tags$a(href="https://rapidrefresh.noaa.gov/hrrr/",tags$img(src = "/ninja/fwas_images/hrrr.jpg", width = "388px", height = "55px"))),
      column(3,tags$a(href="https://radar.weather.gov/",tags$img(src = "/ninja/fwas_images/noaa-logo-960x962.png", width = "100px", height = "100px")))
              
              ),
    # fluidRow(
    #     column(5,'UI made with Shiny')
    # ),
    fluidRow(
      column(5,br()),
      column(3,tags$a(href="https://firelab.org",tags$img(src = "/ninja/fwas_images/3028309.png", width = "200px", height = "200px")))
    ),
    br()
))
