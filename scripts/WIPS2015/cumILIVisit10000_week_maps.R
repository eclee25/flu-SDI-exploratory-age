
## Name: Elizabeth Lee
## Date: 2/1/15
## Function: Plot cumulative incidence per 1000,000 maps
## Filenames: zip3_cumILIVisit10000_week.txt
## Data Source: create_fluseverity_figs_v6/cumILIVisit_week_mapping_dataExport.py and create_choropleth_data.py
## Notes: 
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")

setwd('/home/elee/R/source_functions')
source("dfsumm.R")
require(ggplot2)
require(RColorBrewer)
##############################################################################################
# cumulative incidence maps by week 2/1/15
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
d <- read.table('zip3_cumILIVisit10000_week.txt', header=FALSE, colClasses='character', sep=',', na.strings='nan')
names(d) <- c('season','zip3','week','cumIncid','popstat') # cumulative incidence rate per 10,000 individuals
d$week <- as.Date(d$week, format="%Y-%m-%d")
d$cumIncid <- as.numeric(d$cumIncid)
d$popstat <- as.numeric(d$popstat)
dfsumm(d)
# import latlong coords
latlong <- read.csv('zip3_ll.txt', header=F, sep=',', colClasses='character') # file for source of lat/longs
names(latlong) <- c('zip3', 'latitude', 'longitude')
latlong$latitude <- as.numeric(latlong$latitude)
latlong$longitude <- as.numeric(latlong$longitude)
# merge data and latlong coords
mergeddata <- merge(d, latlong, by.x='zip3', by.y='zip3')

## test code for correct cumulative aggregation ##
a <- mergeddata[(mergeddata$zip3=='022' & mergeddata$season=='1'),1:4]
b <- a[order(a[3]),]
##################################################
# cum incidence are floats, so they need to be binned
# how many bins should there be?
hist(mergeddata$cumIncid, breaks=1000, freq=FALSE)
hist(mergeddata$cumIncid, breaks=1000, freq=FALSE,xlim=c(0,1000), ylim=c(0, .001))
quantile(mergeddata$cumIncid, na.rm=TRUE) 
#    0% (0.000000)       25% (7.30304)       50% (23.17235)        75% (57.46179)      100% (677.16284)

mergeddata$cumIncid_bin<-cut(mergeddata$cumIncid, breaks=c(-999, 0, 1, 5, 10, 20, 30, 40, 50, 60, 100, 200, 680), right=TRUE) # bin the rates
# mergeddata[(mergeddata$cumIncid_bin=='(-999,0]'),] # examine new bins, all of the incidences for the first bin are 0.
uqwk <- sort(unique(mergeddata$week))
colorPalette <- rev(brewer.pal(11, 'RdYlBu'))

### change marker size based on size of urban area ### 2/1/15
# approach 1: use popstat values for every week
quantile(mergeddata$popstat, na.rm=TRUE)
mergeddata$cumIncid_bin[mergeddata$cumIncid_bin=='(-999,0]'] <- NA
mergeddata$cumIncid_bin <- factor(mergeddata$cumIncid_bin) # drop 0 level
# mergeddata$cumIncid_bin <- factor(mergeddata$cumIncid_bin, levels=rev(levels(mergeddata$cumIncid_bin))) 

# # approach 2: use popstat values in season 6 (2005)
# setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata')
# popstat<-read.csv('zip3_incid_season.txt', header=T, sep=",", colClasses='character')
# popstat6<-popstat[popstat$season=='6',]
# # are all zip3s from mergeddata present in popstat6?
# sum(unique(mergeddata$zip3) %in% popstat6$zip3) # 843 zip3s
# length(unique(mergeddata$zip3)) # 843 zip3s - all zip3s from mergeddata are present in popstat
# mergethree <- merge(mergeddata, popstat6, by.x = 'zip3', by.y = 'zip3')
# mergethree$popstat<-as.numeric(mergethree$popstat)
# mergethree[mergethree$attack_bin=="(-Inf,0]",]$attack_bin<-NA
# mergethree$attack_bin<-factor(mergethree$attack_bin) # drop (-Inf,0] level since it no longer occurs
# mergethree$attack_bin<-factor(mergethree$attack_bin, levels=rev(levels(mergethree$attack_bin))) # reversed so low values are blue and high values are red

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/mapoutputs/cumincidencebyweek')
for (i in 1:length(uqwk)){ # length(uqwk)
  Wdat<-mergeddata[mergeddata$week==uqwk[i],]
  g <- ggplot(data=Wdat, aes(size=popstat))
  g <- g + labs(title = paste("Cumulative Incidence per 10,000:", uqwk[i]))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=cumIncid_bin)) #, size=RUCCavg_m
  g <- g + labs(x=NULL, y=NULL)
  g <- g + scale_colour_manual('cum.incid.', values = colorPalette, drop=FALSE, na.value='grey85')
  g <- g + theme(panel.background = element_blank(), panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
 
  ggsave(g, width=6, height=4, filename=paste("cumIncid_map_",uqwk[i],".png", sep=''))
  print(i)
}

# g<- g + scale_color_brewer("cum. incid.", type="div", palette=7, labels=levels(mergeddata$cumIncid_bin), drop=FALSE, na.value="grey85")

## Continental US only ##
# remove Alaska and Hawaii dots - continental US only
AKHI<-c('995', '996', '997', '998', '999', '967', '968')
mergefour<-mergeddata[!(mergeddata$zip3 %in% AKHI),]

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/mapoutputs/cumincidencebyweek_continental')
for (i in 1:length(uqwk)){ # length(uqwk)
  Wdat<-mergefour[mergefour$week==uqwk[i],]
  g <- ggplot(data=Wdat, aes(size=popstat))
  g <- g + labs(title = paste("Cumulative Incidence per 10,000:", uqwk[i]))
  g <- g + scale_size_continuous(range=c(1,5))
  g <- g + scale_size("population size")
  g <- g + geom_point(aes(x=longitude, y=latitude, color=cumIncid_bin)) #, size=RUCCavg_m
  g <- g + labs(x=NULL, y=NULL)
  g <- g + theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank())
  g<- g + scale_colour_manual('cum.incid.', values = colorPalette, drop=FALSE, na.value='grey85')
  
  ggsave(g, width=6, height=4, filename=paste("cumIncid_continental_map_",uqwk[i],".png", sep=''))
  print(i)
}


