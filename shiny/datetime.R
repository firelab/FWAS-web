

time<-format(Sys.time(),"%Y%m%d_%H%M%S")

base<-"threshold"
cap<-".cfg"
email<-"a@.com"

loc=paste(base,"-",email,"-",time,cap,sep="")

print(loc)