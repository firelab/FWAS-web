library(shiny)


shinyUI(pageWithSidebar(

  HTML(paste0('<title>FVS Output Database Browser</title>',
              '<h2><img src="FVSlogo.png" align="middle"</img>',
              '&nbsp;FVS Output Database Browser</h2>'
              )),
 
  sidebarPanel(

    tabsetPanel(id = "loadtabs",
      tabPanel("Load data", 
      	radioButtons("selectdb", "Select database", 
	        choices  = as.list(dbFiles), selected = NULL),
 
      progressInit(),

      uiOutput("buildDerivedButton"),
    
	    gsub ("multiple=","size=10 multiple=",
    	  selectInput("selectdbtables", "Database tables to consider", 
	        choices  = list(), 
	        selected = NULL, multiple = TRUE)),
       # defines width of panel (old: 330px;)	
       # applies to all "select" items
      tags$head(
          tags$style(type="text/css", "select { width: 95%; }") 
           ),
	    gsub ("multiple=","size=50 multiple=",
    	  selectInput("selectdbvars", "Database variables to consider", 
	        choices  = list(), 
	        selected = NULL, multiple = TRUE))
	    ), 
      tabPanel("Explore Data", 
  	    selectInput("stdid", "Select stand", 
	          choices  = list("None loaded"), 
	          selected = NULL, multiple = TRUE),
        div(class="row-fluid",
          div(class="span5",selectInput("mgmid", "Select management", 
	          choices  = list("None loaded"), 
	          selected = NULL, multiple = TRUE)),
          div(class="span5",selectInput("year", "Select years", 
	          choices  = list("None loaded"), 
	          selected = NULL, multiple = TRUE))),
        div(class="row-fluid",	     
	        div(class="span5",selectInput("species", "Select species", 
	          choices  = list("None loaded"), 
	          selected = NULL, multiple = TRUE)),
	        div(class="span5",selectInput("dbhclass", "Select DBHClass", 
	          choices  = list("None loaded"), 
	          selected = NULL, multiple = TRUE))),
	      checkboxGroupInput("browsevars","Select variables",
	          choices = list("None"),selected = NULL)
   	  )
  	)
  ),

  mainPanel(


    tabsetPanel(id = "displaytabs",
      tabPanel("Table", 
        tableOutput("table")),
      tabPanel("Plot",
        includeHTML("plotType.html"),
        includeHTML("colors.html"),
# this codes is replaced by the includeHTML code above.        
#         radioButtons("plotType", "Plot type:", 
#	          choices = as.list(c("line","scatter")), selected = "line"),
#        gsub("label class=\"checkbox\"", "label class=\"checkbox inline\"",
#  	      checkboxGroupInput("lineColors","Colors",
#	          choices = list("default","black","red","green","blue","cyan","magenta"),
#  	        selected = "default")) , 
        div(class="row-fluid",
          div(class="span5",selectInput("xaxis", "X-axis", 
	              choices  = list("None"), selected = NULL)),
          div(class="span5",selectInput("yaxis", "Y-axis", 
	                choices  = list("Year"), selected = NULL, multiple = TRUE))),
        div(class="row-fluid",
          div(class="span4",selectInput("hfacet", "Horizontal facet",
	              choices = list("None","StandID","MgmtID","Year","Species"),
                selected="None")),
	        div(class="span4",selectInput("vfacet", "Vertical facet",
	              choices = list("None","StandID","MgmtID","Year","Species"),
	              selected="None")),
	        div(class="span4",selectInput("pltby", "Plot by code",
	              choices = list("None","StandID","MgmtID","Year","Species"),
	              selected="None"))),
        div(class="row-fluid",
          div(class="span4",textInput("xlabel", "X-label", value = "")),
	        div(class="span4",textInput("ylabel", "Y-label", value = "")),
          div(class="span4",textInput("ptitle", "Title", value = ""))),

        div(class="row-fluid",
          div(class="span4",textInput("width",  "Width (inches)", 
                value = fvsOutData$plotSpecs$width)),
	        div(class="span4",textInput("height", "Height (inches)",
               value = fvsOutData$plotSpecs$height)),        
	        div(class="span4",textInput("res", "Resolution (ppi)",      
               value = fvsOutData$plotSpecs$res))),

	      plotOutput("plot")
	      
	    )
    )  
  )
)) 
