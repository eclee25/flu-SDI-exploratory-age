## Name: Elizabeth Lee
## Date: 7/19/13
## Function: 
### 1. draw OR map per season, popsize as bubble size
### 1b. draw log(OR map) per season 7/31/13, popsize as bubble size
### 1c. draw OR map per season, incidence as bubble size
### 2. draw incidence map per season
### 3) incidence maps by week 7/23/13
## Note: need 11 color bins because that is the max that the diverging color brewer palette will take

## Input Filenames: lat/long- mapping_code/cleanedmapdata/zip3_ll.txt; 1) 
#### OR data by season (includes only 545 zip3s where data is present for all 10 seasons) - mapping_code/cleanedmapdata/zip3_OR_season.txt
#### incidence data by season OR popstat data for weekly incdence maps (includes only 843 zip3s where data is present for all 10 seasons) - mapping_code/cleanedmapdata/zip3_incid_season.txt
#### incidence data by week (includes only 843 zip3s where there is popstat data for all 10 seasons) - mapping_code/cleanedmapdata/zip3_incid_week.txt
## Output Filenames: 
## Data Source: SDI, mapping_code/Coord3digits.csv (lat/long data)
## 


library(ggplot2)

dfsumm<-function(x) {
  if(!class(x)[1]%in%c("data.frame","matrix"))
    stop("You can't use dfsumm on ",class(x)," objects!")
  cat("\n",nrow(x),"rows and",ncol(x),"columns")
  cat("\n",nrow(unique(x)),"unique rows\n")
  s<-matrix(NA,nrow=6,ncol=ncol(x))
  for(i in 1:ncol(x)) {
    iclass<-class(x[,i])[1]
    s[1,i]<-paste(class(x[,i]),collapse=" ")
    y<-x[,i]
    yc<-na.omit(y)
    if(iclass%in%c("factor","ordered"))
      s[2:3,i]<-levels(yc)[c(1,length(levels(yc)))] else
        if(iclass=="numeric")
          s[2:3,i]<-as.character(signif(c(min(yc),max(yc)),3)) else
            if(iclass=="logical")
              s[2:3,i]<-as.logical(c(min(yc),max(yc))) else
                s[2:3,i]<-as.character(c(min(yc),max(yc)))
    s[4,i]<-length(unique(yc))
    s[5,i]<-sum(is.na(y))
    s[6,i]<-!is.unsorted(yc)
  }
  s<-as.data.frame(s)
  rownames(s)<-c("Class","Minimum","Maximum","Unique (excld. NA)","Missing values","Sorted")
  colnames(s)<-colnames(x)
  print(s)
} 


##############################################################################################
# 1) OR maps by season
#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)
  
latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata = merge(communities, latlong, by.x='zip3', by.y='zip3')

# ORs are floats, so they need to be binned
# how many bins should there be?
hist(communities$OR, breaks=50, freq=FALSE)
hist(communities$OR, breaks=50, freq=FALSE,xlim=c(0,30))
hist(communities$OR, breaks=50, freq=FALSE,xlim=c(15,65), ylim=c(0, 0.03))
quantile(communities$OR) #    0% (0.3044887)       25% (2.2441 670)       50% (3.4471814)        75% (5.4550541)      100% (64.2965544)
# explore the large ORs
highOR<-communities[communities$OR>20,] # seems to include both urban and rural communities
mergeddata$OR_bin<-cut(mergeddata$OR, breaks=c(seq(0,16, by=2), 20, 30, 65)) # bin the ORs

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',] # use popstat values from season 6 since it is in the middle of the dataset
# are all zip3s from mergeddata present in popstat10?
sum(unique(mergeddata$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in rucc
mergethree <- merge(mergeddata, popstat6[,2:4], by = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)
mergethree$OR_bin<-factor(mergethree$OR_bin, rev(levels(mergethree$OR_bin)))

# 7/29/13 unused factors are not dropped
for (i in 1:10){
  Sdat<-mergethree[mergethree$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("odds ratio", type="div", palette=7, labels=sort(unique(mergethree$OR_bin)), drop=FALSE) 
#   ggsave(g, width=6, height=4, filename=paste("OR_map_S",i,".png", sep=''))
}

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("odds ratio", type="div", palette=7, labels=sort(unique(mergefour$OR_bin)), drop=FALSE)   
  ggsave(g, width=6, height=4, filename=paste("OR_continentalmap_S",i,".png", sep=''))
}

############# check that the maps are drawing the same thing ############
mergethree[mergethree$zip3=='331',] # Miami, check that bins and colors and legend seem to match
mergethree[mergethree$zip3=='900',] # LA
mergethree[mergethree$zip3=='770',] # Houston

# test with a few cities since there are many different OR bins
Houston<-mergethree[(mergethree$zip3=='770' | mergethree$zip3=='945' | mergethree$zip3=='200' | mergethree$zip3=='900' | mergethree$zip3=='600' | mergethree$zip3=='331'),] # Houston & Norcal & DC & LA & Chicago
for (i in 1:5){
  Sdat<-Houston[Houston$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(9,10))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("odds ratio", type="div", palette=7, labels=sort(unique(mergethree$OR_bin)), drop=FALSE) 
}
Houston[Houston$season=="5",]
############ end checks ################


# 7/19/13 plots, labels were wrong
# for (i in 1:10){
#   Sdat<-mergetwo[mergetwo$season==as.character(i),]
#   g <- ggplot(data=Sdat)
#   g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_legend), size=1)
#   g <- g + labs(x=NULL, y=NULL)
#   g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
#   g <- g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergeddata$OR_bin), decreasing=TRUE)) 
# #   ggsave(g, width=6, height=4, filename=paste("OR_map_S",i,".png", sep=''))
# }


########################################################################################
# 1a) Normalized OR maps by season
#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

# import reference dataset that has season ORs -- use for normalizing zip3 ORs
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Reference_datasets')
seasOR <- read.csv('pk6OR-allzip3_season.csv', header = TRUE, sep = ',', colClasses = 'character')

mergeddata = merge(communities, latlong, by.x = 'zip3', by.y = 'zip3')
mergetwo <- merge(mergeddata, seasOR, by.x = 'season', by.y = 'season') # add ref OR to dataset
mergetwo$pk6_OR <- as.numeric(mergetwo$pk6_OR)
mergetwo$OR_norm <- mergetwo$OR/mergetwo$pk6_OR

# ORs are floats, so they need to be binned
# how many bins should there be?
hist(mergetwo$OR_norm, breaks=50, freq=FALSE)
hist(mergetwo$OR_norm, breaks=50, freq=FALSE,xlim=c(0,10))
hist(mergetwo$OR_norm, breaks=100, freq=FALSE,xlim=c(0,4))
quantile(mergetwo$OR_norm) #   0% 0.0615112    25%  0.5976017  50%  0.8529960  75% 1.2638488  100% 19.3109002
mergetwo$ORnorm_bin<-cut(mergetwo$OR_norm, breaks=c(seq(0, 2.2, by = 0.3), 3, 4, 20)) # bin the ORs

# bubble size = popsize
popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',] # use popstat values from season 6 since it is in the middle of the dataset
# are all zip3s from mergeddata present in popstat10?
sum(unique(mergetwo$zip3) %in% popstat6$zip3) # 545 zip3s
length(unique(mergetwo$zip3)) # 545 zip3s - all zip3s from mergeddata are present in rucc
mergethree <- merge(mergetwo, popstat6[,2:4], by = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)
mergethree$ORnorm_bin<-factor(mergethree$ORnorm_bin, rev(levels(mergethree$ORnorm_bin)))

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/mapoutputs')
for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=ORnorm_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("normalized OR", type="div", palette=7, labels=sort(unique(mergefour$ORnorm_bin)), drop=FALSE)   
  ggsave(g, width=6, height=4, filename=paste("ORnorm_continentalmap_S0",i,".png", sep=''))
}


####################################################################################
# 1b) log OR maps by season
#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)
communities$logOR<-log(communities$OR)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata = merge(communities, latlong, by.x='zip3', by.y='zip3')

# ORs are continuous, so they need to be binned
# how many bins should there be?
hist(communities$logOR, breaks=50, freq=FALSE)

quantile(communities$logOR) #    0% (-1.1891212)       25% (0.8083344)       50% (1.2375569)        75% (1.6965425)      100% (4.1635060)
# explore the large ORs
highOR<-mergeddata[mergeddata$logOR>3,] # seem to be mostly rural areas
mergeddata$logOR_bin<-cut(mergeddata$logOR, breaks=c(seq(-1.5,3.5, by=0.5), 4.5)) # bin the ORs

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',] # use popstat values from season 6 since it is in the middle of the dataset
# are all zip3s from mergeddata present in popstat10?
sum(unique(mergeddata$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in rucc
mergethree <- merge(mergeddata, popstat6[,2:4], by = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)
mergethree$logOR_bin<-factor(mergethree$logOR_bin, levels=c("(-1.5,-1]", "(-1,-0.5]", "(-0.5,0]", "(0,0.5]", "(0.5,1]", "(1,1.5]", "(1.5,2]", "(2,2.5]", "(2.5,3]", "(3,3.5]", "(3.5,4.5]"))
mergethree$logOR_bin<-factor(mergethree$logOR_bin, levels=rev(levels(mergethree$logOR_bin)))

for (i in 1:10){
  Sdat<-mergethree[mergethree$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Log Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=logOR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("log odds ratio", type="div", palette=7, labels=sort(unique(mergethree$logOR_bin)), drop=FALSE) 
#   ggsave(g, width=6, height=4, filename=paste("logOR_map_S",i,".png", sep=''))
}

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Log Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=logOR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("log odds ratio", type="div", palette=7, labels=sort(unique(mergethree$logOR_bin)), drop=FALSE) 
  ggsave(g, width=6, height=4, filename=paste("logOR_continentalmap_S",i,".png", sep=''))
}

#############################################################################################
# 1c. draw OR map per season, incidence as bubble size

#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata = merge(communities, latlong, by.x='zip3', by.y='zip3')

# ORs are floats, so they need to be binned
# how many bins should there be?
hist(communities$OR, breaks=50, freq=FALSE)
hist(communities$OR, breaks=50, freq=FALSE,xlim=c(0,30))
hist(communities$OR, breaks=50, freq=FALSE,xlim=c(15,65), ylim=c(0, 0.03))
quantile(communities$OR) #    0% (0.3044887)       25% (2.2441 670)       50% (3.4471814)        75% (5.4550541)      100% (64.2965544)
# explore the large ORs
highOR<-communities[communities$OR>20,] # seems to include both urban and rural communities
mergeddata$OR_bin<-cut(mergeddata$OR, breaks=c(seq(0,16, by=2), 20, 30, 65)) # bin the ORs

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
# 9/13/13 attack rate was only shown for season6 but we want to show different attack rates by season
# create a uq ID combining season number and zip3 - this will be used to merge the dataset with the ORs
popstat$uqid <- paste(popstat$season, popstat$zip3, sep = '')
mergeddata$uqid <- paste(mergeddata$season, mergeddata$zip3, sep = '')

# are all of the zip3s in mergeddata also in popstat? - check before merging
# there are a greater number of zip3s in popstat than in mergeddata, so 
sum(unique(mergeddata$zip3) %in% popstat$zip3) # 545 zip3s
length(unique(mergeddata$zip3)) # 545 zip3s - all zip3s from mergeddata are present in rucc

# create attack rate variable in popstat
popstat$AR1000 <- as.numeric(popstat$ILI)/as.numeric(popstat$popstat)*1000

mergethree <- merge(mergeddata, popstat[,5:6], by = 'uqid')
mergethree$OR_bin<-factor(mergethree$OR_bin, rev(levels(mergethree$OR_bin)))

# 7/29/13 unused factors are not dropped
for (i in 1:10){
  Sdat<-mergethree[mergethree$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=AR1000))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("attack rate per 1000")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("odds ratio", type="div", palette=7, labels=sort(unique(mergethree$OR_bin)), drop=FALSE) 
  ggsave(g, width=6, height=4, filename=paste("OR_map_S0",i,"_ARsize.png", sep=''))
}

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=AR1000))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("attack rate per 1000")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("odds ratio", type="div", palette=7, labels=sort(unique(mergefour$OR_bin)), drop=FALSE)   
  ggsave(g, width=6, height=4, filename=paste("OR_continentalmap_S0",i,"_ARsize.png", sep=''))
}

#############################################################################################
# 1d) normalized OR by season, attack rate as bubble size

#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

# import reference dataset that has season ORs -- use for normalizing zip3 ORs
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Reference_datasets')
seasOR <- read.csv('pk6OR-allzip3_season.csv', header = TRUE, sep = ',', colClasses = 'character')

mergeddata = merge(communities, latlong, by.x = 'zip3', by.y = 'zip3')
mergetwo <- merge(mergeddata, seasOR, by.x = 'season', by.y = 'season') # add ref OR to dataset
mergetwo$pk6_OR <- as.numeric(mergetwo$pk6_OR)
mergetwo$OR_norm <- mergetwo$OR/mergetwo$pk6_OR

# ORs are floats, so they need to be binned
# how many bins should there be?
hist(mergetwo$OR_norm, breaks=50, freq=FALSE)
hist(mergetwo$OR_norm, breaks=50, freq=FALSE,xlim=c(0,10))
hist(mergetwo$OR_norm, breaks=100, freq=FALSE,xlim=c(0,4))
quantile(mergetwo$OR_norm) #   0% 0.0615112    25%  0.5976017  50%  0.8529960  75% 1.2638488  100% 19.3109002
mergetwo$ORnorm_bin<-cut(mergetwo$OR_norm, breaks=c(seq(0, 2.2, by = 0.3), 3, 4, 20)) # bin the ORs

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
# create a uq ID combining season number and zip3 - this will be used to merge the dataset with the ORs
popstat$uqid <- paste(popstat$season, popstat$zip3, sep = '')
mergetwo$uqid <- paste(mergetwo$season, mergetwo$zip3, sep = '')

# are all of the zip3s in mergeddata also in popstat? - check before merging
# there are a greater number of zip3s in popstat than in mergeddata, so 
sum(unique(mergetwo$zip3) %in% popstat$zip3) # 545 zip3s
length(unique(mergetwo$zip3)) # 545 zip3s - all zip3s from mergeddata are present in rucc

# create attack rate variable in popstat
popstat$AR1000 <- as.numeric(popstat$ILI)/as.numeric(popstat$popstat)*1000

mergethree <- merge(mergetwo, popstat[,5:6], by = 'uqid')
mergethree$ORnorm_bin<-factor(mergethree$ORnorm_bin, rev(levels(mergethree$ORnorm_bin)))

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/mapoutputs')
for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=AR1000))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("attack rate per 1000")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=ORnorm_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("normalized OR", type="div", palette=7, labels=sort(unique(mergefour$ORnorm_bin)), drop=FALSE)   
  ggsave(g, width=6, height=4, filename=paste("ORnorm_continentalmap_S0",i,"_ARsize.png", sep=''))
}

#############################################################################################
# 1e) normalized OR by season, normalized attack rate as bubble size

#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_OR_season.txt', header=F, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
names(communities)<-c('season','zip3','OR')
communities$OR<-as.numeric(communities$OR)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

# import reference dataset that has season ORs -- use for normalizing zip3 ORs
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Reference_datasets')
seasOR <- read.csv('pk6OR-allzip3_season.csv', header = TRUE, sep = ',', colClasses = 'character')

mergeddata = merge(communities, latlong, by.x = 'zip3', by.y = 'zip3')
mergetwo <- merge(mergeddata, seasOR, by.x = 'season', by.y = 'season') # add ref OR to dataset
mergetwo$pk6_OR <- as.numeric(mergetwo$pk6_OR)
mergetwo$OR_norm <- mergetwo$OR/mergetwo$pk6_OR

# ORs are floats, so they need to be binned
# how many bins should there be?
hist(mergetwo$OR_norm, breaks=50, freq=FALSE)
hist(mergetwo$OR_norm, breaks=50, freq=FALSE,xlim=c(0,10))
hist(mergetwo$OR_norm, breaks=100, freq=FALSE,xlim=c(0,4))
quantile(mergetwo$OR_norm) #   0% 0.0615112    25%  0.5976017  50%  0.8529960  75% 1.2638488  100% 19.3109002
mergetwo$ORnorm_bin<-cut(mergetwo$OR_norm, breaks=c(seq(0, 2.2, by = 0.3), 3, 4, 20)) # bin the ORs

# import attack rate for bubble size
popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
# create a uq ID combining season number and zip3 - this will be used to merge the dataset with the ORs
popstat$uqid <- paste(popstat$season, popstat$zip3, sep = '')
mergetwo$uqid <- paste(mergetwo$season, mergetwo$zip3, sep = '')

# are all of the zip3s in mergeddata also in popstat? - check before merging
# there are a greater number of zip3s in popstat than in mergeddata, so 
sum(unique(mergetwo$zip3) %in% popstat$zip3) # 545 zip3s
length(unique(mergetwo$zip3)) # 545 zip3s - all zip3s from mergeddata are present in rucc

# create attack rate variable in popstat
popstat$AR <- as.numeric(popstat$ILI)/as.numeric(popstat$popstat)

mergethree <- merge(mergetwo, popstat[,5:6], by = 'uqid')
mergethree$ORnorm_bin<-factor(mergethree$ORnorm_bin, rev(levels(mergethree$ORnorm_bin)))


# import seasonal attack rate reference
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Reference_datasets')
AR_ref <- read.csv('AR-allzip3_season.csv', header = TRUE, colClasses = 'character')
mergethree <- merge(mergethree, AR_ref, by = 'season')
mergethree$attackrate <- as.numeric(mergethree$attackrate)
mergethree$AR_norm <- mergethree$AR / mergethree$attackrate

# bin normalized attack rates bc they are floats
# how many bins should there be?
hist(mergethree$AR_norm, breaks=50, freq=FALSE)
quantile(mergethree$AR_norm) #   0.02399209 0.45435468 0.76870995 1.26884483 6.74975292 
mergethree$ARnorm_bin<-cut(mergethree$AR_norm, breaks=c(seq(0, 2.2, by = 0.3), 3, 4, 7)) # bin the ORs


## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/mapoutputs')
for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=AR_norm))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("normalized attack rate")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=ORnorm_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("normalized OR", type="div", palette=7, labels=sort(unique(mergefour$ORnorm_bin)), drop=FALSE)   
  ggsave(g, width=6, height=4, filename=paste("ORnorm_continentalmap_S0",i,"_ARnorm.png", sep=''))
}

#############################################################################################
# 2) incidence maps by season
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
communities <- read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
communities$ILI<-as.numeric(communities$ILI)
communities$popstat<-as.numeric(communities$popstat)
communities$attack1000<- communities$ILI/communities$popstat*1000 # attack rate per 1000

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata = merge(communities, latlong, by.x='zip3', by.y='zip3')

# attack1000 are floats, so they need to be binned
# how many bins should there be?
hist(communities$attack1000, breaks=50, freq=FALSE)
hist(communities$attack1000, breaks=50, freq=FALSE,xlim=c(0,30))
hist(communities$attack1000, breaks=50, freq=FALSE,xlim=c(15,65), ylim=c(0, 0.03))
quantile(communities$attack1000) #    0% (0.000000)       25% (1.087103)       50% (2.913078)        75% (6.270440)      100% (57.018699)
# explore the large attack1000s
highattack1000<-communities[communities$attack1000>30,] # seems to include both urban and rural communities
mergeddata$attack1000_bin<-cut(mergeddata$attack1000, breaks=c(seq(0,20, by=2), 60), right=FALSE) # bin the attack1000s

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',]
# are all zip3s from mergeddata present in popstat10?
sum(unique(mergeddata$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in rucc

mergethree <- merge(mergeddata, popstat6[,2:4], by = 'zip3')
mergethree$popstat.y<-as.numeric(mergethree$popstat.y) # when popstat dataset was merged, popstat.y represents the popstat value in season 6.
mergethree$attack1000_bin<-factor(mergethree$attack1000_bin, levels=rev(levels(mergethree$attack1000_bin)))

for (i in 1:10){
  Sdat<-mergethree[mergethree$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat.y))
  g <- g + labs(title = paste("Incidence per 1000, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack1000_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("incidence", type="div", palette=7, labels=levels(mergethree$attack1000_bin), drop=FALSE) 
  ggsave(g, width=6, height=,4 filename=paste("Incid_map_S",i,".png", sep=''))
}

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

for (i in 1:10){
  Sdat<-mergefour[mergefour$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat.y))
  g <- g + labs(title = paste("Incidence per 1000, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack1000_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("incidence", type="div", palette=7, labels=levels(mergethree$attack1000_bin), drop=FALSE) 
  ggsave(g, width=6, height=4, filename=paste("Incid_continentalmap_S0",i,".png", sep=''))
}


############# check that the maps are drawing the same thing ############
mergethree[mergethree$zip3=='331',] # Miami, check that bins and colors and legend seem to match
mergethree[mergethree$zip3=='900',] # LA
mergethree[mergethree$zip3=='770',] # Houston

# test with a few cities since there are many different OR bins
Houston<-mergethree[(mergethree$zip3=='770' | mergethree$zip3=='945' | mergethree$zip3=='200' | mergethree$zip3=='900' | mergethree$zip3=='600' | mergethree$zip3=='331'),] # Houston & Norcal & DC & LA & Chicago
for (i in 1:3){
  Sdat<-Houston[Houston$season==as.character(i),]
  g <- ggplot(data=Sdat, aes(size=popstat.y))
  g <- g + labs(title = paste("Incidence, Season", i))
  g <- g + scale_size_continuous(range=c(9,10))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack1000_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("incidence", type="div", palette=7, labels=levels(mergethree$attack1000_bin), drop=FALSE) 
}
Houston[Houston$season=="3",]
############ end checks ################






##############################################################################################
# 3) incidence maps by week 7/31/13
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
d<-read.csv('zip3_incid_week_cl.txt', header=FALSE, colClasses='character')
names(d)<-c('season','zip3','week','attack') # attack rate per 10,000 individuals
d$week<-as.Date(d$week, format="%Y-%m-%d")
d$attack<-as.numeric(d$attack)
dfsumm(d)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata <- merge(d, latlong, by.x='zip3', by.y='zip3')

# attack are floats, so they need to be binned
# how many bins should there be?
hist(mergeddata$attack, breaks=1000, freq=FALSE)
hist(mergeddata$attack, breaks=1000, freq=FALSE,xlim=c(0,4), ylim=c(0, .1))
hist(mergeddata$attack, breaks=50, freq=FALSE,xlim=c(15,65), ylim=c(0, 0.03))
quantile(mergeddata$attack) #    0% (0.000000)       25% (0.000000)       50% (0.000000)        75% (0.000000)      100% (1074.533)
# explore the large attack10000s
highattack<-mergeddata[mergeddata$attack>8,] # relatively few instances and most of them fall during the 2008-2009 seasons, 786
hist(highattack$attack, freq=FALSE)

mergeddata$attack_bin<-cut(mergeddata$attack, breaks=c(-Inf, seq(0,2, by=0.25), 5, 30, 110), right=TRUE) # bin the attack rates
mergeddata[(mergeddata$attack_bin=='(-Inf,0]' & mergeddata$attack != 0),] # examine new bins, all of the incidences for the first bin are 0.
uqwk <- sort(unique(mergeddata$week))

### change marker size based on size of urban area ### 7/24/13
# # approach 1: use RUCC bin means
# rucc<-read.csv('zip3_RUCC2013avg_crosswalk.csv', header=T, colClasses='character')
# # are all zip3s from mergeddata present in rucc?
# sum(unique(mergeddata$zip3) %in% rucc$zip3) # 843 zip3s
# length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in rucc
# mergethree <- merge(mergeddata, rucc, by.x = 'zip3', by.y = 'zip3') # RUCCavg_m: 1 = metro urban, 2 = nonmetro urban, 3, rural
# mergethree$RUCCavg_m<-as.numeric(mergethree$RUCCavg_m)

# approach 2: use popstat values in season 6 (2005)
popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',]
# are all zip3s from mergeddata present in popstat10?
sum(unique(mergeddata$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in rucc
mergethree <- merge(mergeddata, popstat6, by.x = 'zip3', by.y = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)
mergethree[mergethree$attack_bin=="(-Inf,0]",]$attack_bin<-NA
mergethree$attack_bin<-factor(mergethree$attack_bin) # drop (-Inf,0] level since it no longer occurs
mergethree$attack_bin<-factor(mergethree$attack_bin, levels=rev(levels(mergethree$attack_bin))) # reversed so low values are blue and high values are red

for (i in 1:length(uqwk)){ # length(uqwk)
  Wdat<-mergethree[mergethree$week==uqwk[i],]
  g <- ggplot(data=Wdat, aes(size=popstat))
  g <- g + labs(title = paste("Incidence per 10,000:", uqwk[i]))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack_bin)) #, size=RUCCavg_m
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g<- g + scale_color_brewer("incidence", type="div", palette=7, labels=levels(mergethree$attack_bin), drop=FALSE, na.value="grey85")
  ggsave(g, width=6, height=4, filename=paste("Incid_map_",uqwk[i],".png", sep=''))
  print(i)
}

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergethree[!(mergethree$zip3 %in% AKHI),]

for (i in 1:length(uqwk)){ # length(uqwk)
  Wdat<-mergefour[mergefour$week==uqwk[i],]
  g <- ggplot(data=Wdat, aes(size=popstat))
  g <- g + labs(title = paste("Incidence per 10,000:", uqwk[i]))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack_bin)) #, size=RUCCavg_m
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g<- g + scale_color_brewer("incidence", type="div", palette=7, labels=levels(mergefour$attack_bin), drop=FALSE, na.value="grey85")
  ggsave(g, width=6, height=4, filename=paste("Incid_continental_map_",uqwk[i],".png", sep=''))
  print(i)
}

############# check that the maps are drawing the same thing ############
mergethree[mergethree$zip3=='331',] # Miami, check that bins and colors and legend seem to match
mergethree[mergethree$zip3=='900',] # LA
mergethree[mergethree$zip3=='770',] # Houston

# test with a few cities since there are many different OR bins
Houston<-mergethree[(mergethree$zip3=='770' | mergethree$zip3=='945' | mergethree$zip3=='200' | mergethree$zip3=='900' | mergethree$zip3=='600' | mergethree$zip3=='331'),] # Houston & Norcal & DC & LA & Chicago
for (i in 1:10){
  Sdat<-Houston[Houston$week==uqwk[i],]
  g <- ggplot(data=Sdat, aes(size=popstat))
  g <- g + labs(title = paste("Incidence, Week", uqwk[i]))
  g <- g + scale_size_continuous(range=c(9,10))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack_bin))
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer("incidence", type="div", palette=7, labels=sort(unique(mergethree$attack_bin)), drop=FALSE) 
}
Houston[Houston$week==uqwk[i],]
############ end check on maps ################


############ checks that attack rates seem reasonable #############
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
d2<-read.csv('zip3_incid_week.txt', header=TRUE, colClasses='character')
d2$ILI<-as.numeric(d2$ILI)
d2$popstat<-as.numeric(d2$popstat)
d2$week<-as.Date(d2$week)


AR <- rep(0,10)
for (i in 1:10){
  ili<-sum(d2[d2$season==as.character(i),]$ILI)
  pstat<-303615090
  print(ili)
  print(pstat)
  AR[i]<-ili/pstat*100
}
 # compare AR in week and season data
d3 <- read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character') # includes zip3s that are present for all 10 seasons
d3$ILI<-as.numeric(d3$ILI)
d3$popstat<-as.numeric(d3$popstat)
ARs <- rep(0,10)
for (i in 1:10){
  ili <-sum(d3[d3$season==as.character(i),]$ILI)
  pstat<-sum(d3[d3$season==as.character(i),]$popstat)
  ARs[i]<-ili/pstat*100
}
############## end checks on attack rates ###############





#### pre-existing snippets of code, saved for syntax reference ####

# b <- c(0,1,2,3,5,6,7,8,10,15,16,17,18,28) # test set of data values (previously called community ids)
# b <- scan('zipcode_unique_commid.txt') # list of unique data values

# g = g + labs(x=NULL, y=NULL)
# g = g + theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), legend.position = "top right", axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
# g = g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergeddata$OR_bin))
# ggsave(g, width=6, height=4, filename="zipcode_weighted_S1.png")


#b <- c(0,1,2,3,5,6,7,8,10,15,16,17,18,28)
#g = ggplot(data=mergeddata) + geom_point(aes(x=longitude, y=latitude, colour=V2, group=V2)) 

# g = g + theme_bw() + scale_x_continuous(limits = c(-125, -66), breaks=NA)
# g = g + scale_y_continuous(limits=c(25,50), breaks=NA)

# r <- scan('colors.txt', what="")
# r <- c("#FF0000","#FFFFFF","#00FFFF","#C0C0C0","#0000FF","#808080","#0000A0","#000000","#FF0080","#FFA500","#800080","#A52A2A","#FFF00","#800000","#00FF00","#008000","#FF00FF","#808000","#56A5EC")

# g = g + scale_colour_manual(values=r, breaks=b)
# g = g + scale_colour_manual(values=r)
# g = g + scale_colour_brewer(palette="Spectral", breaks=b)

# g = g + scale_colour_gradientn(breaks=b, labels=format(b), colours=rainbow(40))
# g = g + labs(x=NULL, y=NULL)
# ggsave(g, width=6, height=4, filename="zips.png")
