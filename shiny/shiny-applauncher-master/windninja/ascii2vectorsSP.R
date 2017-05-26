library(raster)
library(plotGoogleMaps)

spd<-raster('/home/natalie/test/big_butte_220_10_138m_vel.asc')
ang<-raster('/home/natalie/test/big_butte_220_10_138m_ang.asc')

vectors<-brick(spd, ang)
names(vectors)<-c("speed", "angle")

vectors_sp<-rasterToPoints(vectors, spatial=TRUE)

vectors_sp$angle<-vectors_sp$angle - 180

vectors_sp$angle[vectors_sp$angle < 0] <- vectors_sp$angle[vectors_sp$angle < 0] + 360

#check CRS stuff
#coordinates(vectors_sp)
#vectors_sp@proj4string
wind_vect<-vectorsSP(vectors_sp, maxlength=200, zcol=c('speed','angle'))

pal<-colorRampPalette(c("blue","green","yellow", "orange", "red"))
m<-plotGoogleMaps(wind_vect, zcol='speed', colPalette=pal(5), mapTypeId='HYBRID',strokeWeight=1)
#plotKML(wind_vect)

