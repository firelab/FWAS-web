# modifies the "summary" statistics so that it is ready to plot. This is done by adding a row
# for post thin so that variables like "TPA" show the trace over time with the removals being 
# as sharp dip.
fvsSetupSummary <- 
function(asum)
{
  std=c("Tpa","TCuFt","MCuFt","BdFt")
  rstd=paste("R",std,sep="")
  stdden = c("BA","SDI","CCF","TopHt","QMD")
  new=asum[,"RTpa"] > 0
  rtpaLoc  = match("RTpa",colnames(asum))
  if (sum(new) > 0) 
  {
    dups=unlist(lapply(1:length(new),function(x,new) if (new[x]) rep(x,2) else x, new))
    asum=asum[dups,]
    for (row in 1:(nrow(asum)-1))
    {
      nrow=row+1
      if (dups[row] == dups[nrow])
      {
        asum[nrow,std]  = asum[nrow,std] - asum[nrow,rstd]
        asum[nrow,stdden]=asum[nrow,paste0("AT",stdden)]
        asum[row,rstd] = 0
        asum[row,rtpaLoc:(rtpaLoc+3)] = 0
        dups[nrow]=0
      }
    }
  }
  tprd=apply(asum[,rstd],2,cumsum)+asum[,std]
  colnames(tprd)=paste("TPrd",std,sep="")
  asum=cbind(asum,tprd)
  asum
}  
     
  
