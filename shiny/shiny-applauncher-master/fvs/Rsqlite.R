require(RSQLite)

m <- dbDriver("SQLite")
fn = "FVSieFireOutput.db"
con <- dbConnect(m,fn)    
tbn = dbListTables(con)

db = lapply(tbn, function (x,con) dbReadTable(con,x), con)
names(db) = tbn


t1 = db[["FVS_SnagSum"]]
t2 = stack(t1[,5:19])
t3 = cbind(Stand = rep(t1$StandID,15),Year=rep(t1$Year,15),t2)


ggplot(t3) + geom_point(aes(y=values,x=Year,color=ind,stat="bin"))


t1 = db[["FVS_PotFire"]]
t2 = stack(t1[,5:ncol(t1)])
nreps = ncol(t1) - 5 + 1
t3 = cbind(Stand = rep(t1$StandID,nreps),Year=rep(t1$Year,nreps),t2)

t3[,1] = as.factor(t3[,1])
t3[,4] = as.factor(t3[,4])
t3[,2] = as.numeric(t3[,2])
t3[,3] = as.numeric(t3[,3])

p = ggplot(t3[grep("PTorch",t3$ind),]) + geom_line(aes(y=values,x=Year,color=ind,stat="bin"))
p + facet_grid(.~Stand)
p + facet_grid(Stand~.)


