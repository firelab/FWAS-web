library(shiny)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {


    # You can access the value of the widget with input$text, e.g.
    output$value <- renderPrint({ input$text })
    
    write<-reactive({
      
      cfg<-"/home/tanner/src/FWAS/shiny/1/new/a.txt"
      cat(paste("ska!","\n",collapse=""),file=cfg,append=FALSE)
      
    })
    output$value2 <- renderPrint({ input$action })
    observeEvent(input$action,{
      write()
    })

  
})
