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
library(sp)
options(rgl.useNULL=TRUE)
library(rgl)
library(shiny)
library(shinyRGL)
library(shinyGridster)
library(ShinyDash)
library(shinyIncubator)
################################################################################
#options(shiny.maxRequestSize=30*1024^2)
################################################################################
# server.r
options(shiny.maxRequestSize = 50*1024^2)
shinyServer(function(input, output, session) {
  
  
  # TM - Tree metrics
  source("00_functions/serverFindTree.r",local = TRUE)
    
  })
################################################################################
