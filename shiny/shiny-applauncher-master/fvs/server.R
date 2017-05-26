library(shiny)
library(shinyIncubator)
library(xtable)
library(ggplot2)
library(RSQLite)


source("fvsSetupSummary.R")
source("fvsCompositeSum.R")
source("ggplotColours.R")
source("dbStdTab.R")

options(shiny.trace = F)  # change to T for trace

unlink ("fvsOutData.RData")
fvsOutDataClass <<- 
  setRefClass("fvsOutData", 
    fields = list(dbLoadData = "list", dbData = "data.frame", dbName = "character",
      dbVars    = "character", browseVars    = "character", 
      dbSelVars = "character", browseSelVars = "character",
      plotSpecs = "list"))

if (file.exists("fvsOut.RData")) load("fvsOutData.RData") else
{
  fvsOutData <<- fvsOutDataClass()
  fvsOutData$plotSpecs <<- list(res=144,height=4,width=6)
}

dbFiles <<- dir(pattern="db")
outs = grep("out",tolower(dbFiles))
if (length(outs) > 0) dbFiles <<- dbFiles[outs]
dbDrv <<- dbDriver("SQLite")

filterRows <- function (dat, stdid, mgtid, year, species, dbhclass)
{
  rows = rep (TRUE,nrow(dat))
  rows = if (!is.null(stdid)    & !is.null(dat$StandID))  rows & dat$StandID  %in% stdid    else rows
  rows = if (!is.null(mgtid)    & !is.null(dat$MgmtID))   rows & dat$MgmtID   %in% mgtid    else rows
  rows = if (!is.null(year)     & !is.null(dat$Year))     rows & dat$Year     %in% year     else rows
  rows = if (!is.null(species)  & !is.null(dat$Species))  rows & dat$Species  %in% species  else rows
  rows = if (!is.null(dbhclass) & !is.null(dat$DBHClass)) rows & dat$DBHClass %in% dbhclass else rows
  rows
}

bindRagged <- function (all,sum,pfxs=c("ForType","SizeCls","StkCls"))
{
  for (pfx in pfxs)
  {
    cols = union(colnames(all)[grep(pfx,colnames(all))],colnames(sum)[grep(pfx,colnames(sum))])
    for (col in cols) 
    {
      if (is.na(match(col,colnames(all)))) all[[col]]=0
      if (is.na(match(col,colnames(sum)))) sum[[col]]=0
    }
  }
  both = rbind(all,sum)
}

  

shinyServer(function(input, output, session) 
{
  on.exit(save(fvsOutData,file="fvsOutData.RData"))

  observe({ 
    # Explore Data
    if (input$loadtabs == "Explore Data")
    { 
      updateTabsetPanel (session, "displaytabs", selected = "Table")
      
      if (is.null(fvsOutData$dbName)) return()
      if (length(fvsOutData$dbSelVars) == 0) return()
      con = dbConnect(get(x="dbDrv",envir=.GlobalEnv),fvsOutData$dbName)
      tbs = unique(unlist(lapply(strsplit(fvsOutData$dbSelVars,":"),function (x) x[1])))
      if (length(tbs) == 0) return()
      cols = unique(unlist(lapply(strsplit(fvsOutData$dbSelVars,":"),function (x) x[2])))
      if (length(cols) == 0) return()
      dat = list()
      for (tb in tbs) 
      {
        dtab = dbReadTable(con,tb)
        if (tb == "FVS_Summary") 
        { 
          dtab = by(dtab,as.factor(dtab$CaseID),FUN=function (x) fvsSetupSummary(x))
          dtab = do.call("rbind",dtab)
          dtab$ForTyp =as.factor(dtab$ForTyp)
          dtab$SizeCls=as.factor(dtab$SizeCls)
          dtab$StkCls =as.factor(dtab$StkCls)
        }
        if (tb == "Derived_Composite") 
        { 
          dtab = by(dtab,as.factor(dtab$MgmtID),FUN=function (x) fvsSetupSummary(x))
          dtab = do.call("rbind",dtab)
        }
        cls = intersect(cols,colnames(dtab))
        if (length(cls) > 0) dtab = dtab[,cls,drop=FALSE]
        
        for (col in colnames(dtab)) if (is.character(dtab[,col])) dtab[,col] = as.factor(dtab[,col])
        if (!is.null(dtab$Year))    dtab$Year    =as.factor(dtab$Year)        
        if (!is.null(dtab$TreeVal)) dtab$TreeVal =as.factor(dtab$TreeVal)        
        if (!is.null(dtab$PtIndex)) dtab$PtIndex =as.factor(dtab$PtIndex)        
        if (!is.null(dtab$SSCD))    dtab$SSCD    =as.factor(dtab$SSCD)    
        rownames(dtab) = 1:nrow(dtab)
        dat[[tb]] = dtab
      }

      dbDisconnect(con)
      mdat = dat$FVS_Cases
      dat$FVS_Cases = NULL
      if (is.null(mdat)) 
      {
        mdat = dat[[1]]
        dat[[1]] = NULL
      }
      if (is.null(mdat)) return()
      if (length(dat) > 0) for (dtab in dat) mdat = merge(mdat,dtab,all=TRUE)
      vars = colnames(mdat)
      if (length(vars) == 0) return()
      updateSelectInput(session, "stdid", choices=as.list(levels(mdat$StandID)), 
                        selected=levels(mdat$StandID))
      updateSelectInput(session, "mgmid", choices=as.list(levels(mdat$MgmtID)), 
                        selected=levels(mdat$MgmtID))
      updateSelectInput(session, "year", choices=as.list(levels(mdat$Year)), 
                        selected=levels(mdat$Year))
      updateSelectInput(session, "species", choices=as.list(levels(mdat$Species)), 
                        selected=levels(mdat$Species))
      updateSelectInput(session, "dbhclass", choices=as.list(levels(mdat$DBHClass)), 
                        selected=levels(mdat$DBHClass))
      selVars = setdiff(vars,c("CaseID","SamplingWt"))
      updateCheckboxGroupInput(session, "browsevars", choices=as.list(vars), 
                               selected=selVars)
      fvsOutData$dbData        <<- mdat
      fvsOutData$browseVars    <<- vars
      fvsOutData$browseSelVars <<- selVars    
    } else updateTabsetPanel (session, "displaytabs", selected = "Table")   
  })
  
  observe({
    if (is.null(input$buildDerived)) return()
    if (input$buildDerived == 0) return()
    if (length(fvsOutData$dbName) == 0) return()
    db <- fvsOutData$dbName
    con <- dbConnect(dbDrv,db)    
    tbs <- dbListTables(con)
    if (!is.na(match("FVS_Summary",tbs)) && !is.na(match("FVS_Cases",tbs)))
    {
      cases = dbReadTable (con,"FVS_Cases")
      mgmts = unique(cases$MgmtID)
      maxProgress = length(mgmts) + length(cases) + 5
    }
    withProgress(session, {  
    i = 1
    if (!is.na(match("FVS_TreeList",tbs)) && !is.na(match("FVS_Cases",tbs)))
    {
      setProgress(message = "Building Derived_StandAndStock", 
                  detail  = "Reading FVS_TreeList", value = i); i = i+1
 
      tl = dbReadTable (con,"FVS_TreeList")
      cases = dbReadTable (con,"FVS_Cases")

      setProgress(message = "Building StandAndStock", 
                  detail  =  paste0("Computing values for ",cases," cases"), value = i); i = i+1

      tab = mkStdTab(tl,cases,dClassWidth=4)

      setProgress(message = "Building StandAndStock", 
                  detail  = "Writing table", value = i); i = i+1

      dbWriteTable(con,"Derived_StandAndStock",tab,overwrite=TRUE,row.names=FALSE) 
    }
    if (!is.na(match("FVS_Summary",tbs)) && !is.na(match("FVS_Cases",tbs)))
    {

      setProgress(message = "Building Derived_Composite", 
                  detail  = "Reading FVS_Summary", value = i); i = i+1

      allsums = dbReadTable (con,"FVS_Summary")
      cases = dbReadTable (con,"FVS_Cases")
      mgmts = sort(unique(cases$MgmtID))
      all = NULL

      for (mgmt in mgmts)
      {
        setProgress(message = "Building Derived_Composite", 
                    detail  =  paste0("Computing values for MgmtID=",mgmt), value = i); i = i+1
                    
        sums = merge(subset(cases,MgmtID==mgmt)[,c(1,6)],allsums[,2:ncol(allsums)])
        sums = by(sums,sums$CaseID,function (x) x[,2:ncol(x)])
        attributes(sums) = NULL
        sums = as.data.frame(fvsCompositeSum(sums))
        sums = cbind(MgmtID=mgmt,sums)
        all = if(is.null(all)) sums else bindRagged (all,sums)
      }


      if (length(mgmts) > 1)
      {
        setProgress(message = "Building Derived_Composite", 
                    detail  = "Computing values for +All", value = i); i = i+1
        sums = merge(cases[,c(1,6)],allsums[,2:ncol(allsums)])
        sums = by(sums,sums$CaseID,function (x) x[,2:ncol(x)])
        attributes(sums) = NULL
        sums = as.data.frame(fvsCompositeSum(sums))
        sums = cbind(MgmtID="+All",sums)
        all = bindRagged(all,sums)
      }

      setProgress(message = "Building Derived_Composite", 
                  detail  = "Finish and write Derived_Composite", value = i); i = i+1

      fft = grep("ForType",colnames(all))[1]
      anms = colnames(all)
      anms = c(anms[1:(fft-1)],sort(anms[fft:length(anms)]))
      all = all[,anms]
      dbWriteTable(con,"Derived_Composite",all,overwrite=TRUE,row.names=FALSE)
      updateSelectInput(session, "selectdbtables", choices=as.list(dbListTables(con)),
                  selected=c("FVS_Cases","FVS_Summary"))
      dbDisconnect(con)
    }

    setProgress(value = NULL)          
    }, min=1, max=maxProgress) 
    
  })

  # selectdb  
  output$buildDerivedButton <- renderUI({
    db <- input$selectdb
    fvsOutData$dbName <<- db
    if (length(fvsOutData$dbName) == 0) return()
    con <- dbConnect(dbDrv,db)    
    tbs <- dbListTables(con)
    dbd = lapply(tbs,function(tb,con) dbListFields(con,tb), con)
    dbDisconnect(con)
    names(dbd) = tbs
    if (!is.null(dbd$FVS_Summary)) 
    { 
      dbd$FVS_Summary = c(dbd$FVS_Summary,c("TPrdTpa","TPrdTCuFt","TPrdMCuFt","TPrdBdFt"))
    }  
    if (!is.null(dbd$Derived_Composite)) 
    { 
      dbd$Derived_Composite = c(dbd$Derived_Composite,c("TPrdTpa","TPrdTCuFt","TPrdMCuFt","TPrdBdFt"))
    }  
    updateSelectInput(session, "selectdbtables", choices=as.list(names(dbd)),
                      selected=c("FVS_Cases","FVS_Summary"))
    fvsOutData$dbLoadData <<- if (is.null(dbd)) list() else dbd
    msg = NULL
    if (!is.null(dbd$FVS_Summary) &&  is.null(dbd$FVS_TreeList)) msg = "Build Composite Table" 
    if ( is.null(dbd$FVS_Summary) && !is.null(dbd$FVS_TreeList)) msg = "Build StandAndStock Table"  
    if (!is.null(dbd$FVS_Summary) && !is.null(dbd$FVS_TreeList)) msg = "Build Composite and StandAndStock Tables"  
    if (!is.null(msg) && (!is.null(dbd$Derived_Composite) || !is.null(dbd$Derived_StandAndStock)))
       msg = sub ("Build","Rebuild",msg)
    if (is.null(msg)) NULL else list(actionButton("buildDerived",msg),h4(" "))
  })

  # selectdbtables
  observe({
    if (is.null(fvsOutData$dbLoadData)) return()
    tables = input$selectdbtables
    vars = lapply(tables,function (tb,dbd) paste0(tb,":",dbd[[tb]]), fvsOutData$dbLoadData)
    vars = unlist(vars)
    if (length(vars) == 0) return()
    preSel = unlist(lapply(c("CaseID","StandID","MgmtID", "SamplingWt","Year",
        "FVS_TreeList:Species$","FVS_TreeList:DBH$","FVS_TreeList:DG$","FVS_TreeList:Ht$","FVS_TreeList:Htg$",
        "FVS_Summary:TCuFt","FVS_Summary:TPrdTCuFt",
        "Derived_Composite:TCuFt","Derived_Composite:TPrdTCuFt"), function (x,vs) 
    {
       hits = unlist(grep(x,vs))
       hits = hits[hits>0]
       vs[hits]
    },vars))
    fvsOutData$dbVars    <<- vars
    fvsOutData$dbSelVars <<- if (is.null(preSel)) character(0) else preSel
    updateSelectInput(session, "selectdbvars",choices=as.list(vars), 
                      selected=preSel)
  })

  # selectdbvars
  observe({
    if (!is.null(input$selectdbvars)) fvsOutData$dbSelVars <<- input$selectdbvars
  })

  observe({
    if (!is.null(input$browsevars)) 
    {
      fvsOutData$browseSelVars <<- input$browsevars
      cats = NULL
      cont = NULL
      for (v in input$browsevars) 
      {
        if (is.factor(fvsOutData$dbData[,v])) cats = c(cats,v) else cont = c(cont,v)
        if (v == "Year") cont = c(cont,v)
      } 
      sel = if (length(intersect(cont,"Year")) > 0) "Year" else if (length(cont) > 0) cont[1] else NULL
      if (sel=="Year" && input$plotType == "scatter" && length(cont) > 1) sel = setdiff(cont,"Year")[1]
      updateSelectInput(session, "xaxis",choices=
             if (input$plotType == "line" || input$plotType == "scatter") as.list(cont) else as.list(cats), 
             selected=sel)
      sel = setdiff(cont,c(sel,"Year"))
      if (length(sel) > 0 && input$plotType != "line" && input$plotType != "scatter") sel = sel[1]
      updateSelectInput(session, "yaxis",choices=as.list(cont),
                      selected=if (length(sel) > 0) sel else NULL)     
      sel = if (length(intersect(cats,"StandID")) > 0) "StandID" else "None"
      updateSelectInput(session, "hfacet",choices=as.list(c("None",cats)),selected=sel) 
      sel = if (length(intersect(cats,"MgmtID")) > 0) "MgmtID" else "None"
      updateSelectInput(session, "vfacet",choices=as.list(c("None",cats)),selected=sel) 
      sel = if (length(intersect(cats,"Species")) > 0) "Species" else "None"
      updateSelectInput(session, "pltby",choices=as.list(c("None",cats)),selected=sel) 

    }
  })
 
  observe({
    updateTextInput(session, "xlabel", label = NULL, value=input$xaxis)
  })
    
  #### renderTable
  output$table <- renderTable(
  {
    if (length(input$selectdbvars) == 0) return(NULL) 
    if (length(input$browsevars) == 0)
    {
      fvsOutData$browseSelVars <<- character(0)
      return (NULL)
    }
    fvsOutData$browseSelVars <<- input$browsevars
    {
      if (length(input$browsevars) > 0) 
      {
        dat = fvsOutData$dbData[filterRows(fvsOutData$dbData, input$stdid, 
                 input$mgmid, input$year, input$species, input$dbhclass),,drop=FALSE]
               
        if (nrow(dat) > 3000) dat[1:3000,input$browsevars,drop=FALSE] else
                              dat[,input$browsevars,drop=FALSE]
      } else NULL
    }
  }) 

  #### renderPlot
  output$plot <- renderImage(
  {
    nullPlot <- function ()
    {
      outfile = "nullPlot.png" 
      png(outfile, width=3, height=2, res=72, units="in", pointsize=12)              
      plot.new()
      text(x=.5,y=.5,"Nothing to graph",col="red")
      dev.off()
      list(src = outfile)
    }

    if (length(input$selectdbvars) == 0 || (length(input$xaxis) == 0 && 
      length(input$yaxis) == 0)) return(nullPlot())

    vf = if (input$vfacet == "None") NULL else input$vfacet
    if (!is.null(vf) && (input$xaxis  == vf || input$yaxis == vf))  vf = NULL
    hf = if (input$hfacet == "None") NULL else input$hfacet
    if (!is.null(hf) && (input$xaxis  == hf || input$yaxis == hf))  hf = NULL
    pb = if (input$pltby  == "None") NULL else input$pltby
    if (!is.null(pb) && (input$xaxis  == pb || input$yaxis == pb))  pb = NULL

    dat = fvsOutData$dbData[filterRows(fvsOutData$dbData, input$stdid, input$mgmid, 
                                       input$year, input$species, input$dbhclass),]

    if (!is.null(vf) && nlevels(dat[,vf]) < 2) vf=NULL
    if (!is.null(hf) && nlevels(dat[,hf]) < 2) hf=NULL
    if (!is.null(pb) && nlevels(dat[,pb]) < 2) pb=NULL

    nlv  = 1 + (!is.null(pb)) + (!is.null(vf)) + (!is.null(hf))
    
    vars = c(input$xaxis, vf, hf, pb, input$yaxis)
                                         
    if (input$xaxis == "Year" && input$plotType != "box" && 
                                 input$plotType != "bar") dat$Year = as.numeric(as.character(dat$Year))

    nd = NULL  
    for (v in vars[(nlv+1):length(vars)])
    {
      if (is.na(v)) return(nullPlot())
      pd = dat[,c(vars[1:nlv],v),drop=FALSE]
      names(pd)[ncol(pd)] = "Y"
      nd = rbind(nd, data.frame(pd,Attribute=v,stringsAsFactors=FALSE))
    }
    nd = na.omit(nd)
    names(nd)[match(input$xaxis,names(nd))] = "X"
    if (!is.null(vf)) names(nd)[match(vf,names(nd))] = "vfacet"
    if (!is.null(hf)) names(nd)[match(hf,names(nd))] = "hfacet"      
    if (!is.null(pb) && !is.null(nd$Attribute)) 
    {
      alv = nlevels(as.factor(nd$Attribute))
      nd$Attribute = if (alv == 1) paste(pb,nd[,pb],sep=":") else
                                   paste(nd$Attribute,pb,nd[,pb],sep=":")
    }
      
    if (!is.null(nd$vfacet))    nd$vfacet    = as.factor(nd$vfacet)
    if (!is.null(nd$hfacet))    nd$hfacet    = as.factor(nd$hfacet)
    if (!is.null(nd$Attribute)) nd$Attribute = as.factor(nd$Attribute)

    fg = NULL
    fg = if (!is.null(nd$vfacet) && !is.null(nd$hfacet)) facet_grid(vfacet~hfacet)
    fg = if (is.null(fg)         && !is.null(nd$hfacet)) facet_grid(.~hfacet) else fg
    fg = if (is.null(fg)         && !is.null(nd$vfacet)) facet_grid(vfacet~.) else fg

    p = ggplot(data = nd) + fg + labs(x=input$xlabel, y=input$ylabel, title=input$ptitle)  + 
          theme(text = element_text(size=9),
          panel.background = element_rect(fill="gray95"),
          axis.text = element_text(color="black")) 

    # colors = rep(rgb(0,0,0,.7),nlevels(nd$Attribute)+1) else
    if (input$colBW == "B&W") colors = rep(rgb(0,0,0,seq(.5,.9,.05)),5) else
    {
      colors = input$colors
    
      if (length(colors) > 0)  
      {
        if (colors[1] == "defaults") colors = ggplotColours(n=nlevels(nd$Attribute)+1) else
        {
          colors = rep(colors,floor(50/length(colors)))
          colors = apply(rbind(col2rgb(colors),.7*255),2,
                   function (x) rgb(x[1],x[2],x[3],x[4],maxColorValue=255))                     
        }
      }
    } 
    if (!is.null(colors)) p = p + scale_colour_manual(values=colors) 
    plt = switch(input$plotType,
      line    = if (input$colBW == "B&W") geom_line    (aes(x=X,y=Y,color=Attribute,linetype=Attribute)) else
                                          geom_line    (aes(x=X,y=Y,color=Attribute)),
      scatter = if (input$colBW == "B&W") geom_point   (aes(x=X,y=Y,shape=Attribute,color=Attribute)) else
                                          geom_point   (aes(x=X,y=Y,shape=Attribute,color=Attribute)),
      bar     = if (input$colBW == "B&W") geom_bar     (aes(x=X,y=Y,color=Attribute,fill=Attribute,pattern=Attribute),position="dodge",stat="identity") else
                                          geom_bar     (aes(x=X,y=Y,color=Attribute,fill=Attribute),position="dodge",stat="identity"),
      box     = if (input$colBW == "B&W") geom_boxplot (aes(x=X,y=Y,color=Attribute,linetype=Attribute)) else
                                          geom_boxplot (aes(x=X,y=Y,color=Attribute))
      )

    outfile = "plot.png" 
    fvsOutData$plotSpecs$res    = as.numeric(input$res)
    fvsOutData$plotSpecs$width  = as.numeric(input$width)
    fvsOutData$plotSpecs$height = as.numeric(input$height)
        
    png(outfile, width=fvsOutData$plotSpecs$width, 
                 height=fvsOutData$plotSpecs$height, units="in", 
                 res=fvsOutData$plotSpecs$res)              
    print(p + plt)
    dev.off()
    list(src = outfile)            
  }, deleteFile = FALSE)
 
})

