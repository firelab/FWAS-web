library(shiny)



fluidPage(
  
  # Copy the line below to make a text input box
  textInput("text", label = h3("Enter Relative Humidity Threshold (%)"), value = ""),
  
  hr(),
  fluidRow(column(3, verbatimTextOutput("value")))
  
)

