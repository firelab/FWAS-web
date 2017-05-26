################################################################################
#               ___________________________________________________            #
#                                                                              #
#                               WEB - LiDAR :                                  #
#               Web Application to processing and visualization                #
#                             LiDAR data                                       #
#                            ui.r Individual tree Metrics-LiDAR                #
#               ___________________________________________________            #
#                                                                              #
#                            Carlos Alberto Silva                              #
#                              Forest Engineer                                 #
#                            MSc Forest Resource                               #
#                         Carlos_engflorestal@outlook.com                      #
#                              US Forest Service                               #
#                     Rocky Mountain Reserach Station                          #
################################################################################

gridster(tile.width = 250, tile.height = 250,
         
        gridsterItem(col = 1, row = 1, size.x = 1, size.y = 3,style="background: light green;",
                      h3(style="margin-left:15px;",style = "margin-top: -5px; width: 300px; ",style="color:#003300", HTML("SETTINGS MENU")),
                     div(style = "margin-top: -15px;", HTML("<hr />")),
                      
div(style = "margin-top: -15px;",radioButtons("Mydata", "Input LiDAR data",
                                   list("Custom data" = "CD",
                                        "Example data" = "ED"))),
                     
conditionalPanel(condition="input.Mydata=='CD'", 
                                       

div(style = "margin-top: -10px;", fileInput('las','',accept='.las'))),
                                           
                      uiOutput("HtreshoudAlpha"),
                                          
                      radioButtons("radiustype", "Tree crown radius - TCR (m)",
                                   list("Fixed Radius" = "FR",
                                        "Variable Radius" = "VR")),
                      
                      tags$head(tags$style(type="text/css",
                                           "label.radio { display: inline-block; }",
                                           ".radio input[type=\"radio\"] { float: none; }"
                      )),
                      
                      conditionalPanel(condition="input.radiustype=='VR'", 
                                       radioButtons("equation", " Equation: TCR = f(ht)",
                                                    list("Deciduous" = "DC",
                                                         "Pines" = "PI",
                                                         "Combined"="CB",
                                                         "Use custom polynomial"="YR")),
                                    
                                       conditionalPanel(condition="input.equation=='YR'", 
                        HTML("|--Inter--------ht--------ht^2-------ht^3--|"),                                
                        div(class="row-fluid", div(class="span6",style = "margin-left: 0px;",numericInput("Ang", "", "")), 
                                                   div(class="span6",style = "margin-left: 55px;margin-top: -45px",numericInput("ht1", "", "")),
                                                   div(class="span6",style = "margin-left: 115px;margin-top: -45px",numericInput("ht2", "", "")),
                                                   div(class="span6",style = "margin-left: 175px;margin-top: -45px",numericInput("ht3", "", ""))))),
                      
                    
                      conditionalPanel(condition="input.radiustype=='FR'", 
                                       numericInput("frv", "", 5)),
                      

                     div(class="row-fluid", div(class="span6",style = "margin-left: 0px; text-align:center",selectInput("backApha", "Background color", 
                                                                                                      choices = c("white","black","gray",
                                                                                                                  "green","forestgreen","red",
                                                                                                                  "blue","yellow","Purple", "Brown"),
                                                                                                      selected="white")), div(class="span6",style = "margin-right: 0px;",style = "margin-top: 0px;text-align:center;",
                                                                                                                              selectInput("legendcolor", "Lengend color", 
                                                                                                                                          choices = c("black","white","gray",
                                                                                                                                                      "green","forestgreen","red",
                                                                                                                                                      "blue","yellow","Purple", "Brown"),selected="forestgreen"))),                     
                     
div(class="row-fluid", div(class="span6",style = "margin-left: 0px;",checkboxInput("Trunkcbox2", "Plot tree trunk", TRUE),div(class="span6",style = "margin-left: 120px;",style = "margin-top: -25px; width: 250px;",checkboxInput("PlotAxes", "Plot Axes", TRUE)))),
                      
div(class="row-fluid", div(class="span6",style = "margin-left: 0px;text-align:center",conditionalPanel(condition="input.Trunkcbox2==true", 
                                       selectInput("trunkcolor", "Trunk color:", 
                                                   choices = c("white","black","gray",
                                                               "green","forestgreen","red",
                                                               "blue","yellow","purple","brown"),selected="brown"))),div(class="span6",style = "margin-right: 0px;text-align:center",conditionalPanel(condition="input.PlotAxes==true", 
                                                                                                                                                                                    selectInput("Axescolor", "Axes color:", 
                                                                                                                                                                                                choices = c("white","black","gray",
                                                                                                                                                                                                            "green","forestgreen","red",
                                                                                                                                                                                                            "blue","yellow","Purple","Brown"),selected="black")))),
                      
                                        
                   
                     div(actionButton("action_button","Run"), downloadButton('downloadTree2', 'Download Results')),
                      
                      div(style = "margin-top: 0px; width: 200px; ",style="color:#003300", HTML("<hr />")),
                      #helpText(HTML("ForestCAS")),
                      div(style = "margin-top: 0px;", HTML("<a href='http://www.fs.fed.us/rmrs/'><img style='width: 300px;height:70px;margin-top: -10px;border-radius: 5px;' src='http://www.fs.fed.us/rm/boise/local_resources/SAIweb/RMRS_LOGO_SAI.jpg'/>")),
                      #div(style = "margin-top: 0px; width: 400px; ",style="color:#003300", HTML("Moscow Forestry Sciences Laboratory")),
                      div(style = "margin-top: 0px;",style="color:#003300", HTML("<a href=' http://www.fs.fed.us/'>USDA Forest Service</a>")),      
                      #div(style = "margin-top: 0px; width: 200px; ",style="color:#003300", HTML("Moscow, ID, USA")),
                      div(style = "margin-top: 0px; width: 200px;", style="color:#003300", HTML("SILVA, C.A; HUDAK, A.T. and CROOKSTON, N. L. (2014)"))
         ),
         tags$div(class = "container",style="border-radius: 5px;",style = "margin-top: 15px;",style="border: 2px solid white;"
                  ,style="margin-left:580px;",style="margin-top: 300px;",style="background: white;",style="float: left; width: 545px;height: 540px;", 
              
                  #plotOutput("distPlot5"),
                  webGLOutput("sctPlotAlpha")),
                  #webGLOutput("sctPlot2")),
         

         gridsterItem(col = 2, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("Summary of LiDAR metrics"))
                      ,tags$div(style = "margin-left: 50px;",tableOutput("summaryTrees"))),
         gridsterItem(col = 3, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("UTM Easting"))
                      ,plotOutput("plotUTMx",width = "100%")),
         gridsterItem(col = 4, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("UTM Northing"))
                      ,plotOutput("plotUTMy",width = "100%")),
         gridsterItem(col = 2, row = 2, size.x = 1, size.y = 2,
                      h4(style = "margin-top: -5px; width: 250px; ",style="text-align: center;",style="color:#003300", HTML("Canopy Height Model Profile")),
                      plotOutput("histTree")),
         progressInit())
