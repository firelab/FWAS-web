library(shiny)

row <- function(...) {
  tags$div(class="row", ...)
}

col <- function(width, ...) {
  tags$div(class=paste0("span", width), ...)
}

shinyUI(bootstrapPage(
  tags$head(tags$link(rel='stylesheet', type='text/css', href='styles.css')),
  tags$div(
      class = "container",
      
    tags$hr(),
    
    row(
      col(5, h2('RMRS Application Center')),
      col(1, img(src = "wn-desktop.ico", height = 40, width = 40)),
      col(1, img(src = "FVSlogo.png", height = 43, width = 43))
    ),
    
    tags$hr(),

    row(
      col(8, h4('Choose an application:'))
    ),
    

   row(
      col(4,
         radioButtons("shinyApp", " ", 
                    c( "WindNinja" = "windninja",
                       "WindNinja-Dust" = "windninja_dust",
                       "Forest Vegetation Simulator" = "fvs",
                       "High-resolution Surface Wind Data Access" = "hireswind",
                       "LiDAR Tree Extractor" = "lidar" ))
         )
       ),
    tags$br(),
    row(
      col(8, 
         div(style="display:inline-table", htmlOutput("appMessage")) 
         )
    ),
    tags$br(),
    
    row(
      col(4,
         div(style="display:inline-table", htmlOutput("emailField"))
      )
    ),
    row(
      col(4,
         div(style="display:inline-table", htmlOutput("projectField"))
      )
    ),

   tags$br(),    

    row(
      col(8,
        div(style="display:inline-table", htmlOutput("launchButton"))
      )
    ),
    
    tags$br(),
    
    row(
      col(8,
        htmlOutput("projectText")# style = "color:darkblue"),
      )
    ),

    tags$hr(),
    
    row(
      col(12,
        h4("Already have an existing project? You can request a list of your exisitng projects.")
      )
    ),

    row(
      col(8, 
          div(style="display:inline-table", textInput("email2", "Email:", " "))
      )
    ),

    tags$br(),

    row(
      col(8,
          actionButton('projectList', "Get my projects")
      )
    ),

    row(
      col(8,
          htmlOutput("projectListText")
      )
    ),

    tags$hr(),
    
    row(
      col(2, img("About")),
      col(2, img("Support"))
    ),
    
    row(
      tags$br(),
      col(2, HTML('<a href="http://www.firemodels.org/index.php/windninja-introduction">WindNinja</a>')),
      col(8, HTML("nwagenbrenner@fs.fed.us - WindNinja, WindNinja-Dust, Wind Data Access"))
      #col(2, HTML('<a href="http://www.fs.fed.us/research/people/profile.php?alias=ncrookston">Contact</a>'))
    ),
    row(
      col(2, HTML('<a href="http://www.fs.fed.us/fmsc/fvs/">FVS</a>')),
      col(8, HTML("ncrookston.fs@gmail.com - Forest Vegetation Simulator"))
    ),
    row(
      col(2, HTML('<a href="http://www.firemodels.org/index.php/windwizard-introduction/windwizard-publications">Wind Data Project</a>')),
      col(8, HTML("ahudak@fs.fed.us - LiDAR Tree Extractor"))
    )
  )
))
