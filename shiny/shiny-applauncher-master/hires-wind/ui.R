library(shiny)

# Define UI for high-res wind application
shinyUI(pageWithSidebar(

  # Application title
  headerPanel("High-Resolution Wind Data Access"),

  sidebarPanel(
    selectInput("site", "Choose a site:",
                list("BSB" = "BSB", 
                     "SRC" = "SRC")),
    
    htmlOutput("selectUI"),

    checkboxInput("vectorPlot", "Create a vector plot (not active)", FALSE),
   
    htmlOutput("setDates"),

    downloadButton('downloadData', 'Download')
  ),

  # Show the caption and plot of the requested variable against speed
  mainPanel(
    tabsetPanel( #tell user to make choices to left and then inspect tabs to right
      tabPanel("Overview", 
                h3(paste("This page provides access to near-surface wind data collected from a tall isolated mountain, ",
                   "Big Southern Butte (BSB), and a steep river canyon, the Salmon River Canyon (SRC).",
                   "Choose a site, sensor, and date range in the panel to the left and explore the ",
                   "Site Map, Plot, Summary, and Table tabs. "), sep = ""),
                 plotOutput("overviewMap", width="50%"),
                 h5("*See here for additional field campaign details, sensor specs, etc.")), 
      tabPanel("Site Map"),
      tabPanel("Plot", plotOutput("speedPlot")), 
      tabPanel("Summary", verbatimTextOutput("summary")), 
      tabPanel("Table", tableOutput("table"))
    )
        
    #h3(textOutput("caption"))
    
    )
    
  ))


