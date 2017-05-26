################################################################################
#               ___________________________________________________            #
#                                                                              #
#                               WEB - LiDAR :                                  #
#               Web Application to processing and visualization                #
#                             LiDAR data                                       #
#               ___________________________________________________            #
#                                                                              #
#                            Carlos Alberto Silva                              #
#                              Forest Engineer                                 #
#                            MSc Forest Resource                               #
#                         Carlos_engflorestal@outlook.com                      #
#                              US Forest Service                               #
#                     Rocky Mountain Reserach Station                          #
################################################################################

################################################################################
# Libraries
#library(shiny)
#library(shinyRGL)
#library(shinyGridster)
#library(ShinyDash)
#library(shinyIncubator)

################################################################################

################################################################################
# ui.r
shinyUI(navbarPage(collapsable = FALSE, inverse = T, 
 
                
                                # title 
HTML("<a href='http://www.fs.fed.us/rmrs/'><img style='width: 50px;height: 60px;' 
                                             src='usfs1.png'/>"),style="text-align: center;", 
tabPanel(h4(style="text-align:center;margin-top: -10px; color:gray", HTML("Welcome")),                   

div(class = "container",style="border-radius: 15px;",style = "margin-top: 15px;",style="border: 2px solid white;"
         ,style="margin-left:0px;",style="margin-top: 0px;",style="background: white;",style="float: center; width: 1330px;height:700px;",
    HTML("<img style='border-radius: 5px; width: 1230px; heigh:700px' src='FirstPage.png'/>"))), 
         

tabPanel(style="background: transparent;",h4(style="text-align:center;margin-top: 10px; color:gray",  HTML("Application")),
         includeCSS("www/style.css"),
         source("00_functions/uiFindTree.r")),

tabPanel(h4(style="text-align:center;margin-top: 10px; color:gray", HTML("About")), style="background: transparent;",
         
         gridster(tile.width = 250, tile.height = 250,
         gridsterItem(col = 1, row = 1, size.x = 1, size.y = 1,style="background: white;",
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("Carlos Alberto Silva")),
                      div(style="text-align: center;",HTML("<a href='http://www.fs.fed.us/research/'><img style='border-radius: 5px; width: 220px; hiegh:250' src='carlos.jpg'/>"))),
         gridsterItem(col = 1, row = 2, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("Andrew T. Hudak")),
                      div(style="text-align: center;",HTML("<a href='http://www.fs.fed.us/research/people/profile.php?alias=ahudak'><img style='border-radius: 5px; width: 220px; hiegh:250' src='ahudak.jpg'/>"))),
         gridsterItem(col = 1, row = 3, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("Nicholas L. Crookston")),
                      div(style="text-align: center;",HTML("<a href='http://www.fs.fed.us/research/people/profile.php?alias=ncrookston'><img style='border-radius: 5px; width: 220px; hiegh:100' src='nick.jpg'/>"))),
         gridsterItem(col = 2, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("Rocky Mountain Research Station - RMRS")),
                      div(style="text-align: center;",HTML("<a href='http://www.fs.fed.us/rmrs/'><img style='width: 200px; height:170px;margin-top: 5px;' src='rmrs.gif'/>"))),
         gridsterItem(col = 3, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("USDA Forest Service")),
                      div(style="text-align: center;",HTML("<a href='http://www.fs.fed.us/research/'><img style='width: 200px;height:200px;margin-top: 5px;'' src='usfs2.jpg'/>"))),
         gridsterItem(col = 4, row = 1, size.x = 1, size.y = 1,
                      h4(style = "margin-top: -5px; width: 250px;",style = "margin-bottom: 10px; width: 250px;",style="text-align: center;",style="color:#003300", HTML("R Programming Language")),
                      div(style="text-align: center;",HTML("<a href='http://www.r-project.org/'><img style='width: 200px;height:200px' src='R.jpg'/>"))),
        
        div(class = "container",style="border-radius: 5px;",style="border: 2px solid white;"
                      ,style="margin-left:300px;",style="margin-top:300px;",style="background: white;",style="float: left; width: 825px;height: 545px;", 
                      h4("Acknowledgement:"),
                      div(align="justify",style="width: 820px",h5("Funding to support Carlos Silva's development of Web-LiDAR and its underlying functions was provided through a grant (RC-2243) from the Department of Defense Strategic Environmental Research and Development Program: Patterns and processes: monitoring and understanding plant diversity in frequently burned longleaf pine landscapes. J. O'Brien, PI; R. Mitchell, A. Hudak, L. Dyer, Co-PIs.")),
                      div(align="justify",style="width: 820px",h5("The airborne lidar data provided as an example dataset is from a longleaf pine forest at Eglin AFB. It's collection was funded by a grant (11-2-1-11) from the Joint Fire Science Program: Data set for fuels, fire behavior, smoke, and fire effects model development and evaluation-the RxCADRE project. R. Ottmar, PI; multiple Co-Is.")),
                      h4("Objective:"),
                      div(align="justify",style="width: 820px",h5("Web-LiDAR was developed to support lidar-based forest inventory and management at Eglin Air Force Base (AFB), Florida, USA. However, it has general applicability to other forests in other ecosystems, and we encourage users to test it broadly.")),
            div(style = "margin-top: -15px;", HTML("<hr />")),
            h4(style = "margin-top: -20px;",style = "margin-top: 5px; width: 500px;",style = "margin-bottom: 10px;",style="text-align: left;",style="color:blue", HTML('<a href="Web-LiDAR_tutorial_CAS.pdf"> Tutorial - Web-LiDAR Forest Inventory Application</a>')),
            #h4(style = "margin-top: 5px; width: 500px;",style = "margin-bottom: 10px;",style="text-align: left;",style="color:blue", HTML('<a href="www.youtube.com/embed/UcnjmklOtQQ?feature=player_detailpage"> Tutorial - Web-LiDAR Forest Inventory Application (Youtube)</a>')),
            div(style = "margin-top: -10px;",style="text-align: left;",HTML("<a href='Web-LiDAR_tutorial_CAS.pdf'><img style='width: 300px;height:200px' src='tutorialPDF.png'/>"),HTML("<a href='Web-LiDAR_tutorial_CAS.pdf'><img style='width: 300px;height:200px' src='tutorialYoutube.png'/>")),
            div(style = "margin-top: -15px;",HTML("|------------------- PDF file ------------------------------------------------- Youtube ------------------------|")))
                      )),
                   div(style="margin-right",title=h4(style="margin-right;margin-top: 10px;", textOutput("pageviews")))
                   
                  
))
################################################################################
