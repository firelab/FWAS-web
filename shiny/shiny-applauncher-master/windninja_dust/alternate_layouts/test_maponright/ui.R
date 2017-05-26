library(leaflet)
library(ShinyDash)
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

shinyUI(bootstrapPage(

  #tags$head(tags$link(rel='stylesheet', type='text/css', href='styles.css')),
  
  
  #row(
    #tags$br(),
    #col(1, tags$br()),
    #col(2, img(src = "wn-icon.png", height = 72, width = 72))
    #col(3, tags$br()),
    #col(4, h2('Test WindNinja Interface'))
  #),
  
  tags$div(
      class = "container",
      #tags$p(tags$br()),
    row(
      #tags$br(),
      col(4, h2('Test WindNinja Interface')),
      tags$br()
      #col(1, img(src = "wn-icon.png", height = 40, width = 40))
    ),
     
    tags$hr(),

    #tags$br(),
    row(
      col(2.5,
        h4('1. Input'),
        selectInput("elevation", "Elevation input:",
                list("Select from map" = "swoopMap",
                     "Upload DEM" = "uploadDem", 
                     "Enter bounding box coordinates" = "boundingBox")),
        tags$br(),
        selectInput("vegetation", "Vegetation type:",
                list("Grass" = "grass", 
                     "Shrubs" = "shrubs",
                     "Trees" = "trees")),
    
        selectInput("runType", "Simulation type:",
                list("Domain average" = "domainAvg", 
                     "Point initialization" = "pointInitialization",
                     "Weather model" = "wxModel"))
      ),

      col(2.5,
        h4('2. Additional options'),
        selectInput("meshResolution", "Mesh resolution:",
                list("Fine" = "fine", 
                     "Medium" = "medium",
                     "Coarse" = "coarse")),
        selectInput("timeZone", "Time zone:",
                list("America/Boise" = "america_boise")),
        tags$br(),
        checkboxInput("dirunalInput", "Use dirunal wind", FALSE),
        tags$br(),
        checkboxInput("stabilityInput", "Use non-neutral stability", FALSE),
        tags$br()

      ),
      col(2.5,
        h4('3. Output'),
        selectInput("outputFiles", "Output:",
                list("Google Earth" = "google", 
                     "Fire Behavior" = "fire",
                     "Shape Files" = "shape",
                     "VTK Files" = "vtk"))
      ),

      col(4,
  leafletMap(
    "map", "100%", 400,
    initialTileLayer = "http://{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
    initialTileLayerAttribution = HTML('Maps by <a href="http://www.mapbox.com/">Mapbox</a>'),
    options=list(
      center = c(40.45, -110.85),
      zoom = 4,
      maxBounds = list(list(17, -180), list(59, 180))
    )
  )
  )
      ),
      
      tags$hr(),

      row(
      col(3, helpText("Click to run WindNinja:", style="color:blue"), actionButton('run_wn', img(src = "wn-icon.png", height = 40, width = 40))),
      #col(3, actionButton('run_wn', strong('Run WindNinja', style = "color:blue"))),
      #col(8, textOutput("text1"))
      col(8, htmlOutput("text1"), style = "color:blue"),
      #col(4, htmlOutput('wnRunningText')),
      col(4, htmlOutput('wn_progress'))
      )
      
    )
))
