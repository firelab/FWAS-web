fvsCompositeSum <- 
function(allsum)
{ 
  if (class(allsum) != "list") stop("allsum must be a list.")
  if (length(allsum) == 0) return (NULL)

  yrs=allsum[[1]][,"Year"]
  for (x in allsum) yrs = intersect(x[,"Year"],yrs)
   
  if (is.null(yrs) | length(yrs) < 1) stop("no common years.")

  mxyr=max(yrs)
  warn=FALSE  
  comp = NULL; sumwt = 0
  fty = NULL
  for (i in 1:length(allsum))
  {
    one = subset (allsum[[i]],allsum[[i]][,"Year"] %in% yrs)
    fty = if (is.null(fty)) one[,c(1,3,27,28,29)] else rbind(fty,one[,c(1,3,27,28,29)])
    
    # check for removals outside of common years
    if (! warn) 
    {
      rmv = allsum[[i]][,c(3,14)]    
      noncom=setdiff(rmv[,1],yrs)
      if (length(noncom) > 0)
      {
        rmv = subset(rmv,rmv[,1] %in% noncom)
        rmv = subset(rmv,rmv[,1] <= mxyr)
        if (nrow(rmv) > 0)
        {
          if (sum(rmv[,2]) > 0) 
          {
            warn=TRUE
            warning (paste("Composite removals do not",
                "include removals in cycle years that are not",
                "common to all summary tables."))     
    }}}}
         
    sum1 = apply(one[,3:26],2,function (x,one) x*one[,1], one)
    if (is.null(comp)) 
    {
      sumwt = one[,1]
      comp = sum1
    } else
    {
      sumwt = sumwt + one[,1]
      comp  = comp + sum1
    }
  } 
  ans = apply(comp,2,function (x,sumwt) x/sumwt, sumwt)
  ans = cbind(ans,SampWt=sumwt)
  
  fts=as.character(unique(sort(fty[,3])))
  ForType = matrix(0,nrow=length(yrs),ncol=length(fts))
  colnames(ForType)=fts
  rownames(ForType)=yrs
  for (i in 1:length(allsum))
  {
    one = subset (allsum[[i]],allsum[[i]][,"Year"] %in% yrs)[,c(1,27)]
    for (n in fts) 
    {  
      add = n == one[,2]
      ForType[add,n] = ForType[add,n]+one[add,1]
    }
  }
  colnames(ForType) = paste("ForType",colnames(ForType),sep="_")
  
  fts=as.character(unique(sort(fty[,4])))
  SizeCls = matrix(0,nrow=length(yrs),ncol=length(fts))
  colnames(SizeCls)=fts
  rownames(SizeCls)=yrs
  for (i in 1:length(allsum))
  {
    one = subset (allsum[[i]],allsum[[i]][,"Year"] %in% yrs)[,c(1,28)]
    for (n in fts) 
    {  
      add = n == one[,2]
      SizeCls[add,n] = SizeCls[add,n]+one[add,1]
    }
  }
  colnames(SizeCls) = paste("SizeCls",colnames(SizeCls),sep="_")

  fts=as.character(unique(sort(fty[,5])))
  StkCls = matrix(0,nrow=length(yrs),ncol=length(fts))
  colnames(StkCls)=fts
  rownames(StkCls)=yrs
  for (i in 1:length(allsum))
  {
    one = subset (allsum[[i]],allsum[[i]][,"Year"] %in% yrs)[,c(1,29)]
    for (n in fts) 
    {  
      add = n == one[,2]
      StkCls[add,n] = StkCls[add,n]+one[add,1]
    }
  }
  colnames(StkCls) = paste("StkCls",colnames(StkCls),sep="_")
  ans=cbind(ans,ForType,SizeCls,StkCls)
  ans
}

