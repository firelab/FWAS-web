#================================= 
#            FWAS
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
             h2('FWAS')   
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
             div(style = "display:inline-table", htmlOutput("RelativeHumidityField"))
      )
      
    ),
    hr(),
    fluidRow(
      column(3, h3('Set Thresholds'))
    ),
    
    fluidRow(
      # column(2, htmlOutput('runButton'))
      column(2, actionButton('run_wn', label="Go! Mokulele"))
    ),
    hr(),
    fluidRow(
      column(4, htmlOutput('wnText'), style = "color:darkblue"),
      br()
    ),

    br()
  ) #end tags$div(class='container') 
))
