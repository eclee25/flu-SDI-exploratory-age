
## Name: Elizabeth Lee
## Date: 11/2/14
## Function: Draw retrospective zOR choropleth of states
### Extract mean zOR data by state from create_fluseverity_figs_v5/export_zRR_classifState_v5.py
### Filename: /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export/SDI_state_classif_covCareAdj_v5_7st.csv
## Data Source: 
## Notes: ggplot2 references: http://blog.revolutionanalytics.com/2009/11/choropleth-challenge-result.html
# 7/21/15: update notation
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
## plot data by state (statelevel classif) ##
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Py_export')
orig2 <- read.csv('SDI_state_classif_covCareAdj_v5_7st.csv', header=TRUE, colClasses = c('numeric', 'character', 'numeric', 'numeric'))
names(orig2) <- c('season', 'state', 'retro_zOR', 'early_zOR', 'valid_normweeks')
orig2$mean_retro_zOR <- cut(orig2$retro_zOR, breaks = c(-10, -5, -1, 1, 5, 15), ordered_result=TRUE)
# 11/2/14: reverse order of levels so that severe values are red and at the top of the legend
orig2$mean_retro_zOR <- factor(orig2$mean_retro_zOR, levels=rev(levels(orig2$mean_retro_zOR)))

# crosswalk state names with call letter abbreviations
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Census')
abbr <- read.csv('state_abbreviations.csv', header=TRUE, colClasses='character')
names(abbr) <- c('region', 'state')
abbr$region <- tolower(abbr$region) # convert state names to lower case because orig2 state names are lower case
orig3 <- merge(orig2, abbr, by = 'state', all=T)

us_state_map <- map_data('state')
setwd('/home/elee/Dropbox (Bansal Lab)/Elizabeth_Bansal_Lab/Manuscripts/Age_Severity/Submission_Materials/BMCMedicine/Submission2/MainFigures')

for (seas in 2:9){
  orig_season2 <- orig3[(orig3$season == seas),]
  choropleth2 <- merge(us_state_map, orig_season2, by='region', all=T)
  choropleth2 <- choropleth2[order(choropleth2$order),]
  seasonmap2 <- ggplot(choropleth2, aes(long, lat, group=group)) +
    geom_polygon(aes(fill=mean_retro_zOR), size = 0.2) +
    geom_polygon(data=us_state_map, color='white', fill=NA) +
    theme_minimal(base_size = 16, base_family = "") +
    theme(panel.background = element_blank(),panel.grid.major = element_blank(), panel.grid.minor = element_blank(), axis.ticks = element_blank(), axis.text.y = element_blank(), axis.text.x = element_blank()) +
    labs(x=NULL, y=NULL) +
    scale_fill_brewer(expression(paste('severity, ', bar(rho["s,r"]))), type='div', palette=7, labels=levels(orig3$mean_retro_zOR), drop=FALSE)
  ggsave(seasonmap2, width=5, height=3, file=sprintf('RetrozRR_State_Season%s_stlvl.png', seas))
}
