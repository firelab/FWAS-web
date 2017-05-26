library(shiny)

row <- function(...) {
  tags$div(class="row", ...)
}

col <- function(width, ...) {
  tags$div(class=paste0("span", width), ...)
}

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


  
  

       selectInput("vegetation", "Vegetation type:",
                   list("Grass" = "grass", 
                        "Brush" = "brush",
                        "Trees" = "trees")),
       selectInput("meshChoice", "Mesh choice:",
                   list("Coarse" = "coarse",
                        "Medium" = "medium",
                        "Fine" = "fine"
                   )),
       br(),
       
       div(style = "display:inline-table", htmlOutput("outputHeightField")),
       div(style = "display:inline-table; width: 70px;",htmlOutput("unitsOutputHeightField")),

       fluidRow(
         column(4, htmlOutput('runButtonText'))
       ),
       fluidRow(
         column(2, htmlOutput('runButton'))
         


)))