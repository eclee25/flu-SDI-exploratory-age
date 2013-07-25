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
## Output Filenames: zip3_fips_popsize.csv (zip3, fips, population size in 2010 dictionary), zip3_ILI_season.csv (zip3, ILI by season dictionary)
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

### 3. convert zip3s to fips codes ## can't get this to work in R, switched over to python 7/10/13
#### alt1: choose one fips code per zip3
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Rural_Urban/R_export')
cw<-read.csv('zip3_RUCC2013.csv', colClasses='character',header=T, quote="\"") # read in zip3-fips crosswalk
cw$pop2010_ers2<-gsub(',', '',cw$pop2010_ers)
cw$pop2010_ers2<-as.numeric(cw$pop2010_ers2) # convert to numeric
dfsumm(cw)
# create fips-pop2010_ers dictionary
fips_pop<-data.frame(cbind(cw$FIPS_ers, cw$pop2010_ers))
fp<-unique(fips_pop)
names(fp)<-c('FIPS','pop2010')
fp$FIPS<-as.character(fp$FIPS)
fp$pop2010<-as.character(fp$pop2010)
fp$pop2010<-gsub(',', '',fp$pop2010)
fp$pop2010<-as.numeric(fp$pop2010)
# check fips_pop
fips_pop[1:50,]
fp[fp$FIPS=='02020',] # checks out
length(unique(fp$FIPS))
length(unique(fp$pop2010)) # some of the population sizes are the same for FIPs codes
# for each zip3, identify the most populous FIPS code affiliated with the zip3
attach(cw)
cw<-cw[complete.cases(cw),] # remove incomplete cases
z_maxfips<-ddply(.data=cw, .variables=c('zip3','FIPS_ers'), summarise, maxfips=max(pop2010_ers2), .fun = function(x) x[x$pop2010_ers2==max(x$pop2010_ers2),6][[1]]) ## why won't this work? grab first index only?

test<-cw[(cw$zip3 %in% c('978','979','980')),]
ddply(.data=test, .variables='zip3', summarize, .fun = function(x) x[(x$pop2010_ers2 == max(x$pop2010_ers2)),6][[1]]) 
test[(test$pop2010_ers2 ==max(test$pop2010_ers2)),6][[1]]
test<-test[1,]

### SWITCH TO PYTHON to finish data cleaning ### 7/10/13
# grab all unique zip3 and fips combinations from cw dataset
cw2<-data.frame(cbind(cw$zip3, cw$FIPS_ers, cw$pop2010_ers))
names(cw2)<-c('zip3','FIPS','pop2010')
cw_exp<-unique(cw2)
cw_exp$zip3<-as.character(cw_exp$zip3)
cw_exp$FIPS<-as.character(cw_exp$FIPS)
cw_exp$pop2010<-as.character(cw_exp$pop2010)
cw_exp$pop2010<-gsub(',', '',cw_exp$pop2010)
cw_exp$pop2010<-as.numeric(cw_exp$pop2010)

# sum ILI and popstat across d3 to remove the agegroup variable
d3$ID<-paste(d3$season, d3$zip3, d3$c_m, sep='') # sum ILI and popstat for each unique d3$ID
d3$ILI<-as.numeric(d3$ILI)
d3$popstat<-as.numeric(d3$popstat)
d4<-ddply(.data=d3, .variables='ID', summarize, ILI = sum(ILI), popstat = sum(popstat)) # ID = "season# (1 or 2 digits), zip3 (3 digits), child/adult (1 character"

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(cw_exp, file="zip3_fips_popsize.csv", row.names=FALSE) # zip3-fips-popsize dataset
write.csv(d4, file="zip3_ILI_season.csv", row.names=FALSE) # ILI data, cleaned zip3s, by season


####################################################################################

# check that the number of unique zip3s is equal to the number of unique FIPS codes


### 4. calculate OR per fips code per season
### 5. export data in format: fips code, OR 

############################################################################
#### INCIDENCE by SEASON MOVIE #### # 7/19/13
library(plyr)
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export')
d<-read.csv('choropleth_seasonincid_v7-1-13.csv', colClasses='character', header=FALSE)
names(d)<-c('season','zip3','ILI','popstat')
d$popstat<-as.numeric(d$popstat)
d$season<-as.numeric(d$season)
d$ILI<-as.numeric(d$ILI)
dno0<-d[d$popstat>0,] # remove zip3s where popstat is 0
dno0[dno0$popstat<dno0$ILI,] # show rows where popstat is less than ILI # none
d_zip3<-ddply(.data=dno0, .variables='zip3', summarise, nseas=length(season))
dropthese<-d_zip3[d_zip3$nseas<10,1]
d2<-dno0[!(dno0$zip3 %in% dropthese),] # 843 zip3s are represented
# this number is larger than the 545 zip3s represented in the OR by season charts because that dataset could include only zip3s for which there was complete adult and child data in order to divide by the appropriate adult and child population sizes. we have the "total" popstat variable here so missing child and adult data does not affect our ability to calculate the total population attack rate in terms of missing data in the denominator. we assume that there were were no ILI cases for that age group during that season (affects the numerator but not the denominator when calculating attack rate)

unique(d2$zip3)# check that the correct zip3s were removed

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
write.csv(d2,file = 'zip3_incid_season.txt', row.names=FALSE) # cleaned incidence by season data exported 7/19/13



#######################################################
## INCIDENCE by WEEK MOVIE ## # 7/23/13
# how many zip3s are present in the choropleth_v7-1-13.csv (weekly) data?
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export')
d<- read.csv('choropleth_v7-1-13.csv', colClasses='character')
names(d)<-c('season','week','zip3','ILI','popstat')
zip3cts<-table(d$zip3)
length(zip3cts[zip3cts<496]) # show zip3s that do not appear every week for 10 seasons (343 zip3s)
length(unique(d$zip3)) # 936 unique zip3s appear

# how many zip3s will be included if we have the popstat variables for the entire season?
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
d2<-read.csv('zip3_incid_season.txt', colClasses='character',header=TRUE)
length(unique(d2$zip3)) # data for 843 zip3s could be calculated

# drop data from d if zip3 does not appear in d2
includethese<-unique(d2$zip3)
d_cl<-d[(d$zip3 %in% includethese),]

# compare popstat data in d_cl and d2
d2[d2$zip3 == '200',]
unique(d_cl[d_cl$zip3 == '200',]$popstat)
# the values are the same except the values in d2 show only the popstat value for the first year in the flu season. There is one less value in the d2 list of values because it has dropped the popstat value for the calendar year 2010.

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/mapping_code/cleanedmapdata')
write.csv(d_cl, file = 'zip3_incid_week.txt', row.names=FALSE) # cleaned incidence by week data exported 7/23/13 # includes only the 843 zip3s that have popstat data for each season in the zip3_incid_season.txt file (the popstat data in this file should be ignored)



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

