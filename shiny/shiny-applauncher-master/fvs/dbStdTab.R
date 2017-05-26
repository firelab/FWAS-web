mkStdTab = function (tl,cases,dClassWidth=4)
{
  mx = max(tl$DBH) 
  nc = mx %/% dClassWidth
  if (nc*dClassWidth < mx) nc=nc+1
  brks = seq(0,nc*dClassWidth,dClassWidth)
  tl$DBHClass = cut(tl$DBH, breaks=brks)
  levels(tl$DBHClass) = sprintf("%2.2i",brks[2:length(brks)])
  tl$Species = gsub(" ","",tl$Species)
  tl$Species = as.factor(tl$Species)
  tl$CaseID  = as.factor(tl$CaseID)
  tl$Year = as.factor(tl$Year)

  tlLevs = list(CaseID=levels(tl$CaseID),Year=levels(tl$Year),
                Species=c(levels(tl$Species),"+All"), DBHClass=c(levels(tl$DBHClass),"+All"))
  
  tab = by (tl,list(tl$CaseID,tl$Year,tl$Species,tl$DBHClass), function(x)
    c(CaseID=as.numeric(x$CaseID[1]),
      Year=as.numeric(x$Year[1]),
      Species=as.numeric(x$Species[1]),
      DBHClass=as.numeric(x$DBHClass[1]),
      LiveTPA=sum(x$TPA),
      MortTPA=sum(x$MortPA),
      LiveTCuFt=sum(x$TCuFt*x$TPA),
      DeadTCuFt=sum(x$TCuFt*x$MortPA)))
  
  for (i1 in 1:dim(tab)[1]) for (i2 in 1:dim(tab)[2]) for (i3 in 1:dim(tab)[3]) 
    for (i4 in 1:dim(tab)[4]) if (is.null(tab[i1,i2,i3,i4][[1]])) tab[i1,i2,i3,i4][[1]] <-
      c(CaseID=i1,Year=i2,Species=i3,DBHClass=i4,LiveTPA=0,MortTPA=0,LiveTCuFt=0,DeadTCuFt=0)
  
  tab = as.data.frame(do.call(rbind,tab))
  
  # sum over DBHClass, make +All DBHClass
  t2 = by (tab,list(tab$CaseID,tab$Year,tab$Species), function(x,clsCd)
    c(CaseID=x$CaseID[1],
      Year=x$Year[1],
      Species=x$Species[1],
      DBHClass=clsCd,
      LiveTPA=sum(x$LiveTPA),
      MortTPA=sum(x$MortPA),
      LiveTCuFt=sum(x$LiveTCuFt),
      DeadTCuFt=sum(x$DeadTCuFt)),length(tlLevs$DBHClass))
  t2 = as.data.frame(do.call(rbind,t2))  
      
  # sum over Species, make +All Species
  t3 = by (tab,list(tab$CaseID,tab$Year,tab$DBHClass), function(x,clsCd)
    c(CaseID=x$CaseID[1],
      Year=x$Year[1],
      Species=clsCd,
      DBHClass=x$DBHClass[1],
      LiveTPA=sum(x$LiveTPA),
      MortTPA=sum(x$MortPA),
      LiveTCuFt=sum(x$LiveTCuFt),
      DeadTCuFt=sum(x$DeadTCuFt)),length(tlLevs$Species))
  t3 = as.data.frame(do.call(rbind,t3))
   
  # sum over both DBHClass and Species, make +All DBHClass and Species
  t4 = by (tab,list(tab$CaseID,tab$Year), function(x,clsCd1,clsCd2)
    c(CaseID=x$CaseID[1],
      Year=x$Year[1],
      Species=clsCd1,
      DBHClass=clsCd2,
      LiveTPA=sum(x$LiveTPA),
      MortTPA=sum(x$MortPA),
      LiveTCuFt=sum(x$LiveTCuFt),
      DeadTCuFt=sum(x$DeadTCuFt)),length(tlLevs$Species),length(tlLevs$DBHClass))
  t4 = as.data.frame(do.call(rbind,t4))
   
  tab = rbind(tab,t2,t3,t4)     
     
  tab = tab[order(tab$CaseID,tab$Year,tab$Species,tab$DBHClass),] 
  tab$CaseID   = tlLevs$CaseID [tab$CaseID]
  tab$Year     = tlLevs$Year    [tab$Year]
  tab$Species  = tlLevs$Species [tab$Species]
  tab$DBHClass = tlLevs$DBHClass[tab$DBHClass]
  tab$CaseID   = as.factor(tab$CaseID)
  tab$Year     = as.factor(tab$Year)
  tab$Species  = as.factor(tab$Species)
  tab$DBHClass = as.factor(tab$DBHClass)
  tab = merge(x=cases[,c(1,3,4)],y=tab,by="CaseID")
  tab
}
