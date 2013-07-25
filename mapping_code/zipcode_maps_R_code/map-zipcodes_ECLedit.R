## Name: Elizabeth Lee
## Date: 7/19/13
## Function: 
### 1. draw OR map per season
### 2. draw incidence map per season
### 3) incidence maps by week 7/23/13
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

# 1) OR maps by season
#communities file should have a list of nodes and data (nodes = zipcodes, data = OR or incidence)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
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

r = data.frame(OR_bin=sort(unique(mergeddata$OR_bin)), OR_legend=as.character(rainbow(length(unique(mergeddata$OR_bin))))) 
# OR_legend does not represent the colors that will be displayed in the maps, but the colors won't display at all if I omit the "color" argument from aes
mergetwo <- merge(mergeddata, r, by.x='OR_bin', by.y='OR_bin')

popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',]
# are all zip3s from mergetwo present in popstat10?
sum(unique(mergetwo$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergetwo$zip3)) # 843 zip3s - all zip3s from mergetwo are present in rucc
mergethree <- merge(mergetwo, popstat6, by.x = 'zip3', by.y = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)

# 7/24/13
for (i in 1:10){
  Sdat<-mergetwo[mergethree$season==as.character(i),]
  g <- ggplot(data=Sdat, , aes(size=popstat))
  g <- g + labs(title = paste("Odds Ratio, Season", i))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_legend), size=1)
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergethree$OR_bin), decreasing=TRUE)) 
  #   ggsave(g, width=6, height=4, filename=paste("OR_map_S",i,".png", sep=''))
}


# 7/19/13 plots
# for (i in 1:10){
#   Sdat<-mergetwo[mergetwo$season==as.character(i),]
#   g <- ggplot(data=Sdat)
#   g <- g + geom_point(aes(x=longitude, y=latitude, color=OR_legend), size=1)
#   g <- g + labs(x=NULL, y=NULL)
#   g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
#   g <- g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergeddata$OR_bin), decreasing=TRUE)) 
# #   ggsave(g, width=6, height=4, filename=paste("OR_map_S",i,".png", sep=''))
# }


# 2) incidence maps by season
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
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

r = data.frame(attack1000_bin=sort(unique(mergeddata$attack1000_bin)), attack1000_legend=as.character(rainbow(length(unique(mergeddata$attack1000_bin))))) 
# attack1000_legend does not represent the colors that will be displayed in the maps, but the colors won't display at all if I omit the "color" argument from aes
mergetwo <- merge(mergeddata, r, by.x='attack1000_bin', by.y='attack1000_bin')

for (i in 1:10){
  Sdat<-mergetwo[mergetwo$season==as.character(i),]
  g <- ggplot(data=Sdat)
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack1000_legend), size=1)
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g <- g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergeddata$attack1000_bin), decreasing=TRUE)) 
#   ggsave(g, width=6, height=4, filename=paste("Incid_map_S",i,".png", sep=''))
}


# 3) incidence maps by week 7/23/13
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
d<-read.csv('zip3_incid_week_cl.txt', header=FALSE, colClasses='character')
names(d)<-c('season','zip3','week','attack') # attack rate per 10,000 individuals
d$week<-as.Date(d$week, format="%Y-%m-%d")
d$attack<-as.numeric(d$attack)
dfsumm(d)

latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong)<-c('zip3', 'latitude', 'longitude')
latlong$latitude<-as.numeric(latlong$latitude)
latlong$longitude<-as.numeric(latlong$longitude)

mergeddata = merge(d, latlong, by.x='zip3', by.y='zip3')

# attack are floats, so they need to be binned
# how many bins should there be?
hist(mergeddata$attack, breaks=1000, freq=FALSE)
hist(mergeddata$attack, breaks=500, freq=FALSE,xlim=c(0,15), ylim=c(0, .1))
hist(mergeddata$attack, breaks=50, freq=FALSE,xlim=c(15,65), ylim=c(0, 0.03))
quantile(mergeddata$attack) #    0% (0.000000)       25% (0.000000)       50% (0.000000)        75% (0.000000)      100% (1074.533)
# explore the large attack10000s
highattack<-mergeddata[mergeddata$attack>8,] # relatively few instances and most of them fall during the 2008-2009 seasons, 786
hist(highattack$attack, freq=FALSE)

mergeddata$attack_bin<-cut(mergeddata$attack, breaks=c(seq(0,8, by=1), 15, 30, 70, 110), right=FALSE) # bin the attack rates
# 
r = data.frame(attack_bin=sort(unique(mergeddata$attack_bin)), attack_legend=as.character(rainbow(length(unique(mergeddata$attack_bin))))) 
# # attack_legend does not represent the colors that will be displayed in the maps, but the colors won't display at all if I omit the "color" argument from aes
mergetwo <- merge(mergeddata, r, by.x='attack_bin', by.y='attack_bin')
uqwk <- sort(unique(mergetwo$week))

### change marker size based on size of urban area ### 7/24/13
# # approach 1: use RUCC bin means
# rucc<-read.csv('zip3_RUCC2013avg_crosswalk.csv', header=T, colClasses='character')
# # are all zip3s from mergetwo present in rucc?
# sum(unique(mergetwo$zip3) %in% rucc$zip3) # 843 zip3s
# length(unique(mergetwo$zip3)) # 843 zip3s - all zip3s from mergetwo are present in rucc
# mergethree <- merge(mergetwo, rucc, by.x = 'zip3', by.y = 'zip3') # RUCCavg_m: 1 = metro urban, 2 = nonmetro urban, 3, rural
# mergethree$RUCCavg_m<-as.numeric(mergethree$RUCCavg_m)

# approach 2: use popstat values in season 6 (2005)
popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
popstat6<-popstat[popstat$season=='6',]
# are all zip3s from mergetwo present in popstat10?
sum(unique(mergetwo$zip3) %in% popstat6$zip3) # 843 zip3s
length(unique(mergetwo$zip3)) # 843 zip3s - all zip3s from mergetwo are present in rucc
mergethree <- merge(mergetwo, popstat6, by.x = 'zip3', by.y = 'zip3')
mergethree$popstat<-as.numeric(mergethree$popstat)


for (i in 1:length(uqwk)){ 
  Wdat<-mergethree[mergethree$week==uqwk[i],]
  g <- ggplot(data=Wdat, aes(size=popstat))
  g <- g + labs(title = paste("Attack Rate per 10,000:", uqwk[i]))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=attack_legend)) #, size=RUCCavg_m
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g<- g + scale_color_brewer(type="div", palette=7, labels=sort(unique(mergethree$attack_bin), decreasing=TRUE)) 
ggsave(g, width=6, height=4, filename=paste("Incid_map_",uqwk[i],".png", sep=''))
}

# need to change it to 11 bins







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
