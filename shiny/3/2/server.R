library(shiny)

textInputRow<-function (inputId, label, value = "") 
{
  div(
    tags$label(label, `for` = inputId), 
    tags$input(id = inputId, type = "text", value = value, class="input-small"))
}

shinyServer(function(input, output, session) {
  
  addRunButton <- reactive({
        actionButton('run_wn', img(src = "wn-icon.png", height = 40, width = 40))
  })
  
  output$runButton <- renderUI({
    addRunButton()
  })
  
  addRunButtonText <- reactive({

          h4("Start run!")
        
      
    
  })
  
  output$runButtonText <- renderUI({
    addRunButtonText()
  })
  writeCfg <- reactive({
    isolate({
      cfg<-"windninja.cfg"
      cat(paste("output_wind_height = ", input$outputWindHeight, "\n", collapse=""), file=cfg, append=TRUE)
    })
  })
  
  

  
  createOutputHeightBox <- reactive({
    textInputRow("outputWindHeight", "Output height:", "20.0")
  })
  output$outputHeightField <- renderUI({
    createOutputHeightBox()
  })
  
  runWN <- reactive({
    if(input$run_wn == 1){
    writeCfg()
    }
  })
  
  
})