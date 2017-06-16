library(shiny)
library(shinyjs)

shinyUI(

  fluidPage(
    
    # Copy the line below to make a text input box
    textInput("text", label = h3("Text input"), value = "Enter text..."),
    
    hr(),
    fluidRow(column(3, verbatimTextOutput("value"))),
    hr(),
    fluidRow(
    # actionButton("action", label = "Action"),
    
      

    useShinyjs(),
    column(3, actionButton("action", "RUN"))),
    # column(3,verbatimTextOutput("value2"))),
    fluidRow(
    column(3,verbatimTextOutput("ska")))
  )
  
)