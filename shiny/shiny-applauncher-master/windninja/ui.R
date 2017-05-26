#================================= 
#            WindNinja
#=================================

library(leaflet)
library(shiny)
#install_github('ShinyDash', 'trestletech')
#install_github('ShinyDash', 'trestletech')
#install_github('leaflet-shiny', 'jcheng5')

row <- function(...) {
  tags$div(class="row", ...)
}

col <- function(width, ...) {
  tags$div(class=paste0("span", width), ...)
}

actionLink <- function(inputId, ...) {
  tags$a(href='javascript:void',
         id=inputId,
         class='action-button',
         ...)
}

textInputRow<-function (inputId, label, value = "") 
{
    div(
        tags$label(label, `for` = inputId), 
        tags$input(id = inputId, type = "text", value = value, class="input-small"))
}


shinyUI(fluidPage(
#shinyUI(fluidPage(theme = "bootstrap.css",
  #plotOutput('main_plot'),

    tags$head(tags$link(rel='stylesheet', type='text/css', href='styles.css'), 
           tags$style("label.radio { display: inline-block; }", ".radio input[type=\"radio\"] { float: none; }")
             ),
    #leafletMap(
    #           "map", "100%", 400,
               #initialTileLayer = "http://{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
               #initialTileLayerAttribution = HTML('Maps by <a href="http://www.mapbox.com/">Mapbox</a>'),
    #           options=list(
    #           center = c(40.45, -110.85),
    #           zoom = 5,
    #           maxBounds = list(list(17, -180), list(59, 180))
    #           )
    #),
  

  tags$div(
      class = "container",
    fluidRow(
    column(5, 
          h2('Test WindNinja Interface')   
    )
    ), 

    hr(),

   fluidRow(
      column(12,
        h3('1. Input')
      )
    ),
    fluidRow(
      column(3,
        selectInput("elevation", "Elevation input:",
                list("Upload DEM" = "uploadDem",
                     "Enter center coordinates" = "centerLatLon", 
                     "Enter bounding box coordinates" = "boundingBox")),

        div(style="width:220px", htmlOutput("demUploader")),
        
        div(style="display:inline-table", htmlOutput("latField")),
        div(style="display:inline-table", htmlOutput("lonField")),
        br(),
        div(style="display:inline-table", htmlOutput("xBufferField")),
        div(style="display:inline-table", htmlOutput("yBufferField")),
        div(style="display:inline-table; width: 80px", htmlOutput("bufferUnits")),
        br(),
        div(style="display:inline-table", htmlOutput("nField")),
        div(style="display:inline-table", htmlOutput("sField")),
        br(),
        div(style="display:inline-table", htmlOutput("wField")),
        div(style="display:inline-table", htmlOutput("eField")),
        
        br(),
        br()

        ),
        column(3, offset = 1,
    
        selectInput("initializationMethod", "Simulation type:",
                list(#"Point initialization" = "pointInitialization",
                     "Weather model" = "wxModelInitialization",
                     "Domain average" = "domainAverageInitialization")),
        
        br(),
        
        div(style="display:inline-table; width: 275px", htmlOutput("inputWxModelType")),
        br(),
        div(style="display:inline-table", htmlOutput("forecastDuration")),

        br(),

        div(style="display:inline-table", htmlOutput("inputHeightField")),
        div(class="input-mini",style="display:inline-table; width: 70px",htmlOutput("unitsInputHeightField")),
        
        br(),

        div(style="display:inline-table", htmlOutput("inputSpeedField")),
        div(class="input-mini",style="display:inline-table; width: 70px;",htmlOutput("unitsInputSpeedField")),
        
        br(),
        
        htmlOutput("inputDirectionField")

        ),
        column(3, offset = 1,

        selectInput("vegetation", "Vegetation type:",
                list("Grass" = "grass", 
                     "Brush" = "brush",
                     "Trees" = "trees")),
        selectInput("meshChoice", "Mesh choice:",
                list("Coarse" = "coarse",
                     "Medium" = "medium",
                     "Fine" = "fine"
                     )),
        br(),
               
        div(style = "display:inline-table", htmlOutput("outputHeightField")),
        div(style = "display:inline-table; width: 70px;",htmlOutput("unitsOutputHeightField"))
      )
    ),
    hr(),
    fluidRow(
      column(3, h3('2. Additional options'))
    ),

    fluidRow( 
      column(3,

        checkboxInput("diurnalInput", "Use diurnal wind", TRUE),
        checkboxInput("stabilityInput", "Use non-neutral stability", FALSE),
        
        br(),
        
        div(style="display:inline-table", htmlOutput("yearField")),
        div(style="display:inline-table", htmlOutput("monthField")),

        div(style="display:inline-table", htmlOutput("dayField")),
        div(style="display:inline-table", htmlOutput("hourField")),
        div(style="display:inline-table", htmlOutput("minuteField")),
        
        br(),
        br(),
        
        div(style="display:inline-table", htmlOutput("inputAirTempField")),
        div(class="input-mini",style="display:inline-table; width: 90px", htmlOutput("unitsInputAirTempField")),
        
        br(),

        div(style="display:inline-table", htmlOutput("inputCloudCoverField")),
        div(class="input-mini",style="display:inline-table; width: 90px;",htmlOutput("unitsInputCloudCoverField"))
 
      )
    ),
    hr(),
    fluidRow(
      column(3, h3('3. Output options'))
    ),

    fluidRow(
      column(3,
        h5("Choose output format(s):"),
        checkboxInput("outGoogleMaps", "Google Maps", TRUE),
        helpText(em("Viewable on your smart phone")), 
        checkboxInput("outGoogleEarth", "Google Earth", FALSE), 
        checkboxInput("outFire", "Fire Behavior", FALSE),
        checkboxInput("outShape", "Shape Files", FALSE),
        checkboxInput("outVtk", "VTK Files", FALSE)
      )
      ),
      hr(),

      fluidRow(
        column(3, h3('4. Start a run'))
      ),
      fluidRow(
        column(8, textOutput("runMessage"))
      ),
      fluidRow(
        column(4, htmlOutput('runButtonText'))
      ),
      fluidRow(
        column(2, htmlOutput('runButton'))
        #column(2, actionButton('run_wn', img(src = "wn-icon.png", height = 40, width = 40))),
      ),
      hr(),
      fluidRow(
        column(4, h3('5. Output'))
      ),
      fluidRow(
        column(4, htmlOutput('wnText'), style = "color:darkblue"),
        column(4, htmlOutput('convertToGoogleMapsText')),
        br()
      ),
      fluidRow(
        column(8,
        div(style="display:inline-table", htmlOutput('downloadButton'))
        #column(8, htmlOutput('downloadButton'))
        )
      ),
      
      br(),

      fluidRow(
        column(3,
          htmlOutput("mapSelection"),
          br()
        )
      ),  
      
      fluidRow(
      column(12,
          br(),
          uiOutput('mymap')
      )
      ),
      
      br(),

      fluidRow(
         column(3, htmlOutput('cleanupButton')) 
      ),

      fluidRow(
         column(12, 
         htmlOutput('cleanupText')
         )
      ),

      hr(),

      fluidRow(
      column(3, HTML('<a href="http://www.firemodels.org/index.php/windninja-introduction">About WindNinja</a>')),
      column(3, HTML('<a href="http://www.firemodels.org/index.php/windninja-support/windninja-contact-us">Contact</a>')),
      column(3, HTML('<a href="https://collab.firelab.org/software/projects/windninja">Development</a>'))
      ),
      
      br()
    ) #end tags$div(class='container') 
))
