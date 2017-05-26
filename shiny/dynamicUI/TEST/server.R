#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)



function(input, output) {
  
  output$ui <- renderUI({
    if (is.null(input$input_type))
      return()
    
    # Depending on input$input_type, we'll generate a different
    # UI component and send it to the client.
    switch(input$input_type,
           "email" = textInput("emailAddress", "Enter Notifcation Email Address",
                                  value = "fsweather1@usa.com"),
           "text" = textInput("textMessage", "Enter Phone Number (no Dashes)",
                              value = "5556667777")
    )
  })
  output$ui2<-renderUI({
    if (is.null(input$input_type))
      return()
    switch(input$input_type,
           
           "text" = selectInput("carrier","Select Carrier",choices=list("AT&T"="att","Verizon"="verizon","Sprint"="sprint","T-Mobile"="tmobile","Virgin Mobile"="virgin"),selected = 1)
           
           
           )
    
    
  })

}

