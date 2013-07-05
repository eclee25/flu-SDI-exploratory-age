## Name: Elizabeth Lee
## Date: 7/1/13
## Function: 
### clean data for incidence by zip3 choropleth
## Input Filenames: choropleth_7-1-13.csv
## Output Filenames: 
## Data Source: SDI 
## 

## functions
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

# load libraries
library(plyr)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export')

# read in SDI data and cleanup
sqld<-read.csv('choropleth_v7-1-13.csv', colClasses='character')
dfsumm(sqld)
names(sqld)<-c('season','week','zip3','ILI','popstat')
dfsumm(sqld)
sqld$week<-as.Date(sqld$week, format="%Y-%m-%d")
sqld$ILI<-as.numeric(sqld$ILI)
sqld$popstat<-as.numeric(sqld$popstat)
sqld$incid<-sqld$ILI/sqld$popstat*100000
sqld$incid[1:100] # incidence per 100000
sqld[1:20,]

# read in 
d<-read.csv('zipcode_bysseas_6-12-13.csv', header=FALSE, col.names=c('season','c_m','zip3','agegroup','ILI','popstat'), colClasses='character')

