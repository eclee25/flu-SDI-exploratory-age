## Name: Elizabeth Lee
## Date: 7/1/13

## Purpose: To draw a choropleth of OR for each season using peak incidence week +/- 6 week season definitions

## Function: 
### 1. delete popstat=0 data entries
### 2. delete zip3s for which at least one A or C sub-agegroup is missing in any season (how many zip3s are left?)
### 3. convert zip3s to fips codes - it turns out zip3s and fips codes are not compatible. multiple fips codes are in a single zip3 and multiple zip3s are in a single fips code
### 4. calculate OR per fips code per season
### 5. export data in format: fips code, OR
## Input Filenames: OR_swk6_zip3.csv (season, peak +/- 6wk season) choropleth_7-1-13.csv (weekly, Oct-May season)
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

###########################################################################
#### ORs by SEASON MOVIE ####


## read data
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export')
d<-read.csv('OR_swk6_zip3.csv', header=FALSE, col.names=c('season','zip3','c_m','agegroup','ILI','popstat'), colClasses='character')
dfsumm(d)

## program ##
### 1. delete popstat=0 data entries
length(d[(d$popstat=='0'),6]) # how many entries have popstat=0? # 523 of 57824 entries have 0 for popstat
d2<-d[!(d$popstat=='0'),] # delete entries

### 2. delete zip3s for which at least one A or C sub-agegroup is missing in any season (how many zip3s are left?)
d2_age<-ddply(.data=d2, .variables='zip3', summarise, nagegrp=length(unique(c_m))) # number of unique age group markers for each zip3 (possibilites are only 1 or 2)
d2_age[d2_age$nagegrp<2,1] # list of zip3s that are missing at least one age group # all zip3s have both agegroups across entire dataset
d2_allage<-ddply(.data=d2, .variables='zip3', summarise, nagegrp=length(c_m)) # each zip3 should have 70 entries 
dropthese<-d2_allage[d2_allage$nagegrp<70,1] # drop zip3s that have fewer than 70 entries
length(d2_allage[d2_allage$nagegrp<70,1]) # 340 or 885 unique zip3s are missing at least one agegroup entry across all 10 seasons
length(unique(d2$zip3)) # 885 unique zip3s in dataset
d3<-d2[!(d2$zip3 %in% dropthese),] # delete entries with those 340 zip3s that are missing agegroup entries

### 3. convert zip3s to fips codes
#### alt1: choose one fips code per zip3
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Rural_Urban/R_export')
cw<-read.csv('zip3_RUCC2013.csv', colClasses='character', header=T)
# for each zip3, identify the most populous FIPS code affiliated with the zip3
# check that the number of unique zip3s is equal to the number of unique FIPS codes


### 4. calculate OR per fips code per season
### 5. export data in format: fips code, OR 

############################################################################
#### ORs by WEEK MOVIE ####

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

