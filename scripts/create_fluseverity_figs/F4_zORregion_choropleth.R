
## Name: Elizabeth Lee
## Date: 5/13/14
## Function: Draw retrospective zOR choropleth of HHS regions
### Extract mean zOR data by state from create_fluseverity_figs/extract_meanzOR_by_region.py
## Filenames: /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/meanzOR_by_state.csv
## Data Source: 
## Notes: ggplot2 references: http://blog.revolutionanalytics.com/2009/11/choropleth-challenge-result.html
## 
## useful commands:
## install.packages("pkg", dependencies=TRUE, lib="/usr/local/lib/R/site-library") # in sudo R
## update.packages(lib.loc = "/usr/local/lib/R/site-library")


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

require(maps)
require(ggplot2)

# one <- c("connecticut","maine","massachusetts","new hampshire","rhode island","vermont")
# two <- c("new york","new jersey")
# three <- c("delaware","district of columbia","maryland","pennsylvania","virginia","west virginia")
# four <- c("alabama", "florida","georgia","kentucky","mississippi","north carolina","south carolina","tennessee")
# five <- c("illinois","indiana","michigan","minnesota","ohio","wisconsin")
# six <- c("arkansas","louisiana","new mexico","oklahoma","texas")
# seven <- c("iowa","kansas","missouri","nebraska")
# eight <- c("colorado","montana","north dakota","south dakota","utah","wyoming")
# nine <- c("arizona","california","nevada")
# ten <- c("idaho","oregon","washington")

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
orig <- read.csv('meanzOR_by_state.csv', header=TRUE, colClasses = c('numeric', 'numeric', 'character', 'numeric', 'numeric'))
names(orig) <- c('season', 'HHSreg', 'region', 'retro_zOR', 'early_zOR')
orig$mean_retro_zOR <- cut(orig$retro_zOR, breaks = c(-10, -5, -1, 0, 1, 5, 10, 30))

us_state_map <- map_data('state')
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_3_26/choropleths')

for (seas in 2:9){
  orig_season <- orig[(orig$season == seas),]
  choropleth <- merge(us_state_map, orig_season, by='region', all=T)
  choropleth <- choropleth[order(choropleth$order),]
  seasonmap <- ggplot(choropleth, aes(long, lat, group=group)) +
    geom_polygon(aes(fill=mean_retro_zOR), size = 0.2) +
    geom_polygon(data=us_state_map, color='white', fill=NA) +
    theme_minimal(base_size = 16, base_family = "") +
    theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
    labs(x=NULL, y=NULL) +
    scale_fill_brewer("mean retro zOR", type='div', palette=7, labels=levels(orig$mean_retro_zOR), drop=FALSE)
  ggsave(seasonmap, file=paste('RetrozOR_Season', seas, '.png', sep=''))
}
