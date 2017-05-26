library(shiny)

# Define UI for high-res wind application
shinyUI(pageWithSidebar(

  # Application title
  headerPanel("Online Test Interface for WindNinja"),

  sidebarPanel(
    tabsetPanel(
      tabPanel("Inputs",
        selectInput("elevation", "Elevation input:",
                list("Upload DEM" = "uploadDem", 
                     "Select from map" = "swoopMap",
                     "Enter bounding box coordinates" = "boundingBox")),
        selectInput("vegetation", "Choose predominant vegetation type:",
                list("Grass" = "grass", 
                     "Shrubs" = "shrubs",
                     "Trees" = "trees")),
    
        selectInput("runType", "Choose simulation type:",
                list("Domain average" = "domainAvg", 
                     "Point initialization" = "pointInitialization",
                     "Weather model" = "wxModel")),
    
        htmlOutput("selectUI")),
    
      tabPanel("Additional Options", h4("Additional options (to be added later).")),
      tabPanel("Outputs",
        downloadButton('downloadData', 'Download output file')
      )
    )
  ),

  # Show the caption and plot of the requested variable against speed
  mainPanel(
    tabsetPanel(
      tabPanel("Inputs", h3("Map for selecting/viewing DEM bounds (coming soon).")), 
      tabPanel("Outputs", h4("Select and view ouptut fields here."))
    )
        
    #h3(textOutput("caption"))
    
    )
    
  ))


