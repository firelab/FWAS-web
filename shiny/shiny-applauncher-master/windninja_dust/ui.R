library(leaflet)
library(ShinyDash)
library(shiny)
library(shinyIncubator)

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
  
  fluidRow(
    column(4,
      h2("Test WindNinja-Dust Interface")
    ),
    column(5,
      br(),
      img(src = "wn-desktop.ico", height = 40, width = 40)
    )
  ),
  
  fluidRow(
    column(12, hr())
  ),
      
  fluidRow(
    column(3, 
      wellPanel(
      h4('1. Input'),
        
      div(style="width:220px", 
          fileInput("firePerimeterFile", "Upload fire perimeter shapefiles (as .zip):", multiple=FALSE, accept=NULL)
         ),
         
      selectInput("initializationMethod", "Wind input:",
                list("Domain average" = "domainAverageInitialization")), 
                     #"Point initialization" = "pointInitialization",
                     #"Weather model" = "wxModelInitialization")),
        
      br(),
        
      div(style="display:inline-table", htmlOutput("inputHeightField")),
      div(style="display:inline-table; width: 70px",htmlOutput("unitsInputHeightField")),
        
      br(),

      div(style="display:inline-table", htmlOutput("inputSpeedField")),
      div(style="display:inline-table; width: 70px;",htmlOutput("unitsInputSpeedField")),
        
      br(),
        
      htmlOutput("inputDirectionField"),

      selectInput("meshChoice", "Mesh choice:",
                list("Coarse" = "coarse",
                     "Medium" = "medium",
                     "Fine" = "fine"
                     ))
      )
    ),

    column(2,
      wellPanel(
      h4('2. Additional options'),
      
      checkboxInput("diurnalInput", "Use diurnal wind", FALSE),
      checkboxInput("stabilityInput", "Use non-neutral stability", FALSE),
      
      br(),
      
      div(style="display:inline-table", htmlOutput("yearField")),
      div(style="display:inline-table", htmlOutput("monthField")),
      #br(),
      div(style="display:inline-table", htmlOutput("dayField")),
      div(style="display:inline-table", htmlOutput("hourField")),
      div(style="display:inline-table", htmlOutput("minuteField")),
        
      br(),
      br(),
        
      div(style="display:inline-table", htmlOutput("inputAirTempField")),
      div(style="display:inline-table; width: 90px",htmlOutput("unitsInputAirTempField")),
        
      br(),

      div(style="display:inline-table", htmlOutput("inputCloudCoverField")),
      div(style="display:inline-table; width: 90px;",htmlOutput("unitsInputCloudCoverField"))
        
      )
    ),
    column(2,
      wellPanel(
      h4('3. Output'),
      paste("Choose output format(s):"),
      br(),
      br(),
      checkboxInput("outGoogleMaps", "Google Maps", TRUE),
      helpText(em("Viewable on your smart phone")), 
      checkboxInput("outGoogleEarth", "Google Earth", FALSE), 
      checkboxInput("outFire", "ASCII files", FALSE)
      )
    )
  ),
  
  fluidRow(
    column(2, htmlOutput('runButtonText')),
    column(1, htmlOutput('runButton')),
    column(3, textOutput("runMessage")),
    progressInit(),
    column(3, htmlOutput('wnText'))
  ),
  hr(),
      
  br(),
  
      
  fluidRow(
    column(2, htmlOutput('downloadButton'))
  ),
  
  br(),
           
  fluidRow(
    column(11,
      tags$br(),
      uiOutput('mymap')
    )
  ),
      
  hr(),

  fluidRow(
    column(3, HTML('<a href="http://www.firemodels.org/index.php/windninja-introduction">About WindNinja</a>')),
    column(3, HTML('<a href="http://www.firemodels.org/index.php/windninja-support/windninja-contact-us">Contact</a>')),
    column(3, HTML('<a href="https://collab.firelab.org/software/projects/windninja">Development</a>'))
  ),
      
  br()
  
  ))
  


