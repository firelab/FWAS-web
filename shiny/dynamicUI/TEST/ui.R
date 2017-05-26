#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)



fluidPage(
  titlePanel("Dynamically generated user interface components"),
  fluidRow(
    
    column(3, wellPanel(
      # selectInput("input_type", "Input type",
      #             c("slider", "text", "numeric", "checkbox",
      #               "checkboxGroup", "radioButtons", "selectInput",
      #               "selectInput (multi)", "date", "daterange"
      #             )
      # )
      
      radioButtons("input_type",label=h3("Select Notifcation Type"),choices=list("email"="email","text message"="text"))
      
      
    )),
    
    column(5, wellPanel(
      # This outputs the dynamic UI component
      uiOutput("ui"),
      uiOutput("ui2")
      
    ))
      # This outputs the dynamic UI component
    
    
  )
)

