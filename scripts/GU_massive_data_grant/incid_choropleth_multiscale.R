
## Name: Elizabeth Lee
## Date: 7/1/14
## Function: Draw incidence choropleth of HHS regions and states
### Extract mean zOR data by state from create_fluseverity_figs/extract_meanzOR_by_region.py (states in the same region had the same mean zOR)
## Filename: 
### Extract incidence per 100,000 by state from /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/scripts/GU_massive_data_grant/export_ILI_by_state.py
### Filename: Py_export/AR100000_state_season.csv, Py_export/AR100000_region_season.csv
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

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')

#########################################
## plot data by HHS region ##

# region level AR per 100,000
d_reg <- read.csv('AR100000_region_season.csv', header=TRUE, colClasses='numeric')
names(d_reg) <- c('season', 'region', 'AR')
d_reg$AR_cut <- cut(d_reg$AR, breaks = c(seq(0, 3750, by=750), 6000, 10000, 18000))

us_state_map <- map_data('state')
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_3_26/choropleths')

# crosswalk hhs regions with call letter abbreviations
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
hhs_abbr <- read.csv('stateabbr_regnum_crosswalk.csv', header=TRUE, colClasses=c('character', 'numeric'))
orig2 <- merge(d_reg, hhs_abbr, by.x = 'region', by.y = 'HHSregion')


# crosswalk call letter abbreviations with full lowercase state names
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census')
abbr <- read.csv('state_abbreviations.csv', header=TRUE, colClasses='character')
names(abbr) <- c('region', 'state')
abbr$region <- tolower(abbr$region) # convert state names to lower case
orig3 <- merge(orig2, abbr, by = 'state')
names(orig3) <- c('state', 'regnum', 'season', 'AR', 'AR_cut', 'region')

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_3_26/choropleths')

# region level map
for (seas in 5:5){
  orig_season <- orig3[(orig3$season == seas),]
  choropleth <- merge(us_state_map, orig_season, by='region', all=T)
  choropleth <- choropleth[order(choropleth$order),]
  seasonmap <- ggplot(choropleth, aes(long, lat, group=group)) +
    geom_polygon(aes(fill=AR_cut), size = 0.2) +
    geom_polygon(data=us_state_map, color='white', fill=NA) +
    theme_minimal(base_size = 16, base_family = "") +
    theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
    labs(x=NULL, y=NULL) +
    scale_fill_brewer("AR per 100,000", type='div', palette=7, labels=levels(orig_season$AR_cut), drop=FALSE)
  ggsave(seasonmap, width=6, height=3, file=paste('AR_region_S', seas, '.png', sep=''))
}

#########################################
## plot data by state ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')

# state level AR per 100,000
d_st <- read.csv('AR100000_state_season.csv', header=TRUE, colClasses = c('numeric', 'character', 'numeric'))
names(d_st) <- c('season', 'state', 'AR')
d_st$AR_cut <- cut(d_st$AR, breaks = c(seq(0, 3750, by=750), 6000, 10000, 18000))


# crosswalk state names with call letter abbreviations
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census')
abbr <- read.csv('state_abbreviations.csv', header=TRUE, colClasses='character')
names(abbr) <- c('region', 'state')
abbr$region <- tolower(abbr$region) # convert state names to lower case because orig2 state names are lower case
orig3 <- merge(d_st, abbr, by = 'state', all=T)

us_state_map <- map_data('state')
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/graph_outputs/current_14_3_26/choropleths')

for (seas in 5:5){
  orig_season2 <- orig3[(orig3$season == seas),]
  choropleth2 <- merge(us_state_map, orig_season2, by='region', all=T)
  choropleth2 <- choropleth2[order(choropleth2$order),]
  seasonmap2 <- ggplot(choropleth2, aes(long, lat, group=group)) +
    geom_polygon(aes(fill=AR_cut), size = 0.2) +
    geom_polygon(data=us_state_map, color='white', fill=NA) +
    theme_minimal(base_size = 16, base_family = "") +
    theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
    labs(x=NULL, y=NULL) +
    scale_fill_brewer("AR per 100,000", type='div', palette=7, labels=levels(orig_season2$AR_cut), drop=FALSE)
  ggsave(seasonmap2, width=6, height=3, file=paste('AR_state_S', seas, '.png', sep=''))
}
