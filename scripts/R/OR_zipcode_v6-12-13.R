
## Name: Elizabeth Lee
## Date: 6/12/13
## Update from 5-16-13 version
### Need to re-clean new zipcode_bysseas data that has the correct popstat values
### Check the magnitude of effect of missing 5/10 yr age group entries on the calculation of OR. How many zipcodes are afflicted with missing age group data each season?

## Function: 
### 1. delete season 0 data # 6/12 and zip3="TOT" data
### 2. delete zip3s for which A or C values are missing for that season
### 3. create a clean dataset with season, age group marker, zip3, ILI counts, and popstat by agegroup and zip3
#### note: popstat will be missing values if certain smaller age groups were not present in the dataset (underestimation)
## Input Filenames: zipcode_bysseas.csv
## Output Filenames: zipcode_bysseas_cl.csv 
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

## read data
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/SQL_export')
d<-read.csv('zipcode_bysseas_6-12-13.csv', header=FALSE, col.names=c('season','c_m','zip3','agegroup','ILI','popstat'), colClasses='character') # 6/12 added agegroup column
dfsumm(d)

## program
#remove season 0s
d1<-d[!(d$season=='0'),]
dim(d[d$season=='0',]) # 6189 6 # number of rows removed matches number of season 0 rows
dim(d1) # 58619 6
dim(d) # 64808 6
dim(d)[1]-dim(d1)[1] # == 6189 so this is correct
#6/12 remove zip3="TOT"
test<-d1[!(d1$zip3=="TOT"),] # 58549 6
TOT<-d1[d1$zip3=="TOT",] # 70 6 # 1 row per age group (7) per season (10)
dim(d1)[1]-dim(TOT)[1] # 58549 so TOT removal worked correctly
d1<-test # reassign to d1

# 6/12 remove separation of d1 into seasonal datasets at this time
# 6/12 don't need to drop "O" age group data because that was already removed in the new mysql export

d2<-d1 # 6/12 reassign d1 to d2 so don't have to rewrite all code
# separate all seasons into different datasets
d2_1<-d2[d2$season=='1',]
d2_2<-d2[d2$season=='2',]
d2_3<-d2[d2$season=='3',]
d2_4<-d2[d2$season=='4',]
d2_5<-d2[d2$season=='5',]
d2_6<-d2[d2$season=='6',]
d2_7<-d2[d2$season=='7',]
d2_8<-d2[d2$season=='8',]
d2_9<-d2[d2$season=='9',]
d2_10<-d2[d2$season=='10',]
# for each season, identify zipcodes with fewer than 2 rows (ie. don't have both A&C data)
d2_1nage<-ddply(.data=d2_1, .variables='zip3', summarise, nagegrp=length(unique(c_m))) # number of unique age group markers for each zip3 (possibilites are only 1 or 2)
d2_1mz<-d2_1nage[d2_1nage$nagegrp<2,1] #list of zip3s that need to be removed due to missing data 
length(d2_1mz) #61 zip3s need to be removed
# how many of these are children vs adults?
table(d2_1$c_m) # A: 2966, C: 2234

d2_2nage<-ddply(.data=d2_2, .variables='zip3', summarise, nagegrp=length(unique(c_m))) 
d2_2mz<-d2_2nage[d2_2nage$nagegrp<2,1]
length(d2_2mz) #50 zip3s need to be removed
table(d2_2$c_m) # A: 3127, C: 2349

d2_3nage<-ddply(.data=d2_3, .variables='zip3', summarise, nagegrp=length(unique(c_m))) 
d2_3mz<-d2_3nage[d2_3nage$nagegrp<2,1]
length(d2_3mz) #34 zip3s need to be removed
table(d2_3$c_m) # A: 3235, C: 2466

d2_4nage<-ddply(.data=d2_4, .variables='zip3', summarise, nagegrp=length(unique(c_m))) 
d2_4mz<-d2_4nage[d2_4nage$nagegrp<2,1]
length(d2_4mz) #13 zip3s need to be removed
table(d2_4$c_m) # A: 3380, C: 2523

d2_5nage<-ddply(.data=d2_5, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_5mz<-d2_5nage[d2_5nage$nagegrp<2,1]
length(d2_5mz) #11 zip3s need to be removed
table(d2_5$c_m) # A: 3423, C: 2560

d2_6nage<-ddply(.data=d2_6, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_6mz<-d2_6nage[d2_6nage$nagegrp<2,1]
length(d2_6mz) #12 zip3s need to be removed
table(d2_6$c_m) # A: 3417, C: 2567

d2_7nage<-ddply(.data=d2_7, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_7mz<-d2_7nage[d2_7nage$nagegrp<2,1]
length(d2_7mz) #12 zip3s need to be removed
table(d2_7$c_m) # A: 3391, C: 2563

d2_8nage<-ddply(.data=d2_8, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_8mz<-d2_8nage[d2_8nage$nagegrp<2,1]
length(d2_8mz) #5 zip3s need to be removed
table(d2_8$c_m) # A: 3477, C: 2591
length(unique(d2_8nage$zip3)) # 881 zip3s

d2_9nage<-ddply(.data=d2_9, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_9mz<-d2_9nage[d2_9nage$nagegrp<2,1]
length(d2_9mz) #2 zip3s need to be removed
table(d2_9$c_m) # A: 3483, C: 2618
length(unique(d2_9nage$zip3)) # 882 zip3s present

d2_10nage<-ddply(.data=d2_10, .variables='zip3', summarise, nagegrp=length(unique(c_m)))
d2_10mz<-d2_10nage[d2_10nage$nagegrp<2,1]
length(d2_10mz) #1 zip3s need to be removed
table(d2_10$c_m) # A: 3531, C: 2648
length(unique(d2_10nage$zip3)) # 885 zip3s present in dataset

# check these in the original d1 data
d1[d1$zip3=='821',]
d2[d2$zip3=='821',]

# 6/12/13 Are there zip3s for which at least one complete age groups is missing every season? Take the intersect of all the mz lists.
u<-intersect(d2_1mz, d2_2mz) # 20
u2<-intersect(d2_3mz, d2_4mz) # 2
u3<-intersect(d2_5mz, d2_6mz) # 1
u4<-intersect(d2_7mz, d2_8mz) # 1
u5<-intersect(d2_9mz, d2_10mz) # none
# 6/12/13 How many total zip3s are affected by missing data in one complete age groups across all 10 seasons?
u<-union(d2_1mz, d2_2mz) 
u2<-union(d2_3mz, d2_4mz) 
u3<-union(d2_5mz, d2_6mz) 
u4<-union(d2_7mz, d2_8mz) 
u5<-union(d2_9mz, d2_10mz)
uu2<-union(u,u2)
u3u4<-union(u3, u4)
uu2u5<-union(uu2, u5)
allu<-union(uu2u5, u3u4) # 112 total zipcodes affected
# note that these mz lists only refer to the zip3s that had one age group between A&C present in the dataset; those with 0 age groups would not appear at all
d2_1b<-d2_1nage$zip3[!(d2_1nage$zip3 %in% d2_1mz)]
intersect(d2_1b, d2_1mz) # check for empty vector
d2_2b<-d2_2nage$zip3[!(d2_2nage$zip3 %in% d2_2mz)]
intersect(d2_2b, d2_2mz) # check for empty vector
d2_3b<-d2_3nage$zip3[!(d2_3nage$zip3 %in% d2_3mz)]
intersect(d2_3b, d2_3mz) # check for empty vector
d2_4b<-d2_4nage$zip3[!(d2_4nage$zip3 %in% d2_4mz)]
intersect(d2_4b, d2_4mz) # check for empty vector
d2_5b<-d2_5nage$zip3[!(d2_5nage$zip3 %in% d2_5mz)]
intersect(d2_5b, d2_5mz) # check for empty vector
d2_6b<-d2_6nage$zip3[!(d2_6nage$zip3 %in% d2_6mz)]
intersect(d2_6b, d2_6mz) # check for empty vector
d2_7b<-d2_7nage$zip3[!(d2_7nage$zip3 %in% d2_7mz)]
intersect(d2_7b, d2_7mz) # check for empty vector
d2_8b<-d2_8nage$zip3[!(d2_8nage$zip3 %in% d2_8mz)]
intersect(d2_8b, d2_8mz) # check for empty vector
d2_9b<-d2_9nage$zip3[!(d2_9nage$zip3 %in% d2_9mz)]
intersect(d2_9b, d2_9mz) # check for empty vector
d2_10b<-d2_10nage$zip3[!(d2_10nage$zip3 %in% d2_10mz)]
intersect(d2_10b, d2_10mz) # check for empty vector

## 6/12 Remove all zip3s that are missing data for one complete age group (children or adults) within a single season
d3_1<-d2_1[(d2_1$zip3 %in% d2_1b), ]
d3_2<-d2_2[(d2_2$zip3 %in% d2_2b), ]
d3_3<-d2_3[(d2_3$zip3 %in% d2_3b), ]
d3_4<-d2_4[(d2_4$zip3 %in% d2_4b), ]
d3_5<-d2_5[(d2_5$zip3 %in% d2_5b), ]
d3_6<-d2_6[(d2_6$zip3 %in% d2_6b), ]
d3_7<-d2_7[(d2_7$zip3 %in% d2_7b), ]
d3_8<-d2_8[(d2_8$zip3 %in% d2_8b), ]
d3_9<-d2_9[(d2_9$zip3 %in% d2_9b), ]
d3_10<-d2_10[(d2_10$zip3 %in% d2_10b), ]

## 6/12/13 For each season, how many zip3s have fewer than 7 entries, meaning that these zip3s are missing at least one age group value for that season
d3_1tab<-table(d3_1$zip3)
d3_1mz3<-names(d3_1tab)[d3_1tab<7] # which zip3s have fewer than 7? (season 1 missing zip3s)
length(d3_1mz3) # 154 of 786 zip3s had missing data in s1
dim(d3_1tab)

d3_2tab<-table(d3_2$zip3)
d3_2mz3<-names(d3_2tab)[d3_2tab<7] 
length(d3_2mz3) # 118 of 813 zip3s had missing data in s2
dim(d3_2tab)

d3_3tab<-table(d3_3$zip3)
d3_3mz3<-names(d3_3tab)[d3_3tab<7] 
length(d3_3mz3) # 99 of 841 zip3s had missing data in s3
dim(d3_3tab)

d3_4tab<-table(d3_4$zip3)
d3_4mz3<-names(d3_4tab)[d3_4tab<7] 
length(d3_4mz3) # 69 of 864 zip3s had missing data in s4
dim(d3_4tab)

d3_5tab<-table(d3_5$zip3)
d3_5mz3<-names(d3_5tab)[d3_5tab<7] 
length(d3_5mz3) # 62 of 871 zip3s had missing data in s5
dim(d3_5tab)

d3_6tab<-table(d3_6$zip3)
d3_6mz3<-names(d3_6tab)[d3_6tab<7] 
length(d3_6mz3) # 66 of 871 zip3s had missing data in s6
dim(d3_6tab)

d3_7tab<-table(d3_7$zip3)
d3_7mz3<-names(d3_7tab)[d3_7tab<7] 
length(d3_7mz3) # 69 of 869 zip3s had missing data in s7
dim(d3_7tab)

d3_8tab<-table(d3_8$zip3)
d3_8mz3<-names(d3_8tab)[d3_8tab<7] 
length(d3_8mz3) # 36 of 876 zip3s had missing data in s8
dim(d3_8tab)

d3_9tab<-table(d3_9$zip3)
d3_9mz3<-names(d3_9tab)[d3_9tab<7] 
length(d3_9mz3) # 32 of 880 zip3s had missing data in s9
dim(d3_9tab)

d3_10tab<-table(d3_10$zip3)
d3_10mz3<-names(d3_10tab)[d3_10tab<7] 
length(d3_10mz3) # 5 of 884 zip3s had missing data in s10
dim(d3_10tab)

## 6/12 Are there certain zip3s that are missing at least one small agegroup entry across all 10 seasons?
i<-intersect(d3_1mz3, d3_2mz3) # 64
i2<-intersect(d3_3mz3, d3_4mz3) # 40
i3<-intersect(d3_5mz3, d3_6mz3) # 30
i4<-intersect(d3_7mz3, d3_8mz3) # 25
i5<-intersect(d3_9mz3, d3_10mz3) # 3
## 6/12 How many unique zip3s are missing at least one small agegroup entry across all 10 seasons?
u<-union(d3_1mz3, d3_2mz3) 
u2<-union(d3_3mz3, d3_4mz3) 
u3<-union(d3_5mz3, d3_6mz3) 
u4<-union(d3_7mz3, d3_8mz3) 
u5<-union(d3_9mz3, d3_10mz3)
uu2<-union(u,u2)
u3u4<-union(u3, u4)
uu2u5<-union(uu2, u5)
allu<-union(uu2u5, u3u4) # 273 zip3s missing at least one small agegroup data across all 10 seasons (after removing the ones missing complete agegroup data)

# 6/12 rm subset based on d2_b sets because that was already done above near line 170

# 6/14 drop a zip3 on a season-by-season basis when missing at least one small agegroup popstat
# checks
d4_1<-d3_1[!(d3_1$zip3 %in% d3_1mz3), ]
d4_2<-d3_2[!(d3_2$zip3 %in% d3_2mz3), ]
d4_3<-d3_3[!(d3_3$zip3 %in% d3_3mz3), ]
d4_4<-d3_4[!(d3_4$zip3 %in% d3_4mz3), ]
d4_5<-d3_5[!(d3_5$zip3 %in% d3_5mz3), ]
d4_6<-d3_6[!(d3_6$zip3 %in% d3_6mz3), ]
d4_7<-d3_7[!(d3_7$zip3 %in% d3_7mz3), ]
d4_8<-d3_8[!(d3_8$zip3 %in% d3_8mz3), ]
d4_9<-d3_9[!(d3_9$zip3 %in% d3_9mz3), ]
d4_10<-d3_10[!(d3_10$zip3 %in% d3_10mz3), ]
# check zip3 removal
length(unique(d4_1$zip3)) # 632 
length(unique(d2_1$zip3)) # 847
length(union(d3_1mz3, d2_1mz)) # 215 zip3s were removed (847-632, check)

# 6/14 Doesn't matter if ILI count is zero for a particular age group in one season as long as the popstat values are there
# 6/14 recombine dataset
d4cl<-rbind(d4_1, d4_2, d4_3, d4_4, d4_5, d4_6, d4_7, d4_8, d4_9, d4_10)
dfsumm(d1)
dfsumm(d4cl)
setdiff(d1$zip3, d4cl$zip3) # only 6 zip3s were completely removed from the dataset, but some of them may be present only in a few of the seasons # 059, 203, 556, 595, 893, 821 # all zip3s have pretty small population sizes
d1[d1$zip3=="059",] # this checks out
d1[d1$zip3=="203",] # this checks out
d1[d1$zip3=="556",] # this checks out
d1[d1$zip3=="595",] # this checks out
d1[d1$zip3=="893",] # this checks out
d1[d1$zip3=="821",] # this checks out

# 6/14 rm check on how many "Other" age groups are missing because Other age group data was dropped in mysql export

# 6/14 check whether ILI attack rates are 0 for any one age group for each season (identified in 6/10 additional checks in previous version of code); these data should not be present in the cleaned datasets
d4_1[d4_1$zip3=='133',] # empty
d4_1[d4_1$zip3=='137',] # empty
d4_3[d4_3$zip3=='6145',] # empty\\

# 6/14 rm additional checks conducted on 6/10 because these issues were addressed in the above code. 

# 6/14 aggregate data by A and C for each season (instead of listing all age groups)
## for each zip3 within a season dataset, sum ILI and popstat values for A and C
d4_1a<-ddply(.data=d4_1, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_1b=data.frame(cbind(season=rep("1", dim(d4_1a)[1]), c_m=d4_1a$c_m, zip3=d4_1a$zip3, ILIsum=d4_1a$ILIsum, popstatsum=d4_1a$popstatsum), stringsAsFactors = FALSE)

d4_2a<-ddply(.data=d4_2, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_2b=data.frame(cbind(season=rep("2", dim(d4_2a)[1]), c_m=d4_2a$c_m, zip3=d4_2a$zip3, ILIsum=d4_2a$ILIsum, popstatsum=d4_2a$popstatsum), stringsAsFactors = FALSE)

d4_3a<-ddply(.data=d4_3, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_3b=data.frame(cbind(season=rep("3", dim(d4_3a)[1]), c_m=d4_3a$c_m, zip3=d4_3a$zip3, ILIsum=d4_3a$ILIsum, popstatsum=d4_3a$popstatsum), stringsAsFactors = FALSE)

d4_4a<-ddply(.data=d4_4, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_4b=data.frame(cbind(season=rep("4", dim(d4_4a)[1]), c_m=d4_4a$c_m, zip3=d4_4a$zip3, ILIsum=d4_4a$ILIsum, popstatsum=d4_4a$popstatsum), stringsAsFactors = FALSE)

d4_5a<-ddply(.data=d4_5, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_5b=data.frame(cbind(season=rep("5", dim(d4_5a)[1]), c_m=d4_5a$c_m, zip3=d4_5a$zip3, ILIsum=d4_5a$ILIsum, popstatsum=d4_5a$popstatsum), stringsAsFactors = FALSE)

d4_6a<-ddply(.data=d4_6, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_6b=data.frame(cbind(season=rep("6", dim(d4_6a)[1]), c_m=d4_6a$c_m, zip3=d4_6a$zip3, ILIsum=d4_6a$ILIsum, popstatsum=d4_6a$popstatsum), stringsAsFactors = FALSE)

d4_7a<-ddply(.data=d4_7, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_7b=data.frame(cbind(season=rep("7", dim(d4_7a)[1]), c_m=d4_7a$c_m, zip3=d4_7a$zip3, ILIsum=d4_7a$ILIsum, popstatsum=d4_7a$popstatsum), stringsAsFactors = FALSE)

d4_8a<-ddply(.data=d4_8, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_8b=data.frame(cbind(season=rep("8", dim(d4_8a)[1]), c_m=d4_8a$c_m, zip3=d4_8a$zip3, ILIsum=d4_8a$ILIsum, popstatsum=d4_8a$popstatsum), stringsAsFactors = FALSE)

d4_9a<-ddply(.data=d4_9, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_9b=data.frame(cbind(season=rep("9", dim(d4_9a)[1]), c_m=d4_9a$c_m, zip3=d4_9a$zip3, ILIsum=d4_9a$ILIsum, popstatsum=d4_9a$popstatsum), stringsAsFactors = FALSE)

d4_10a<-ddply(.data=d4_10, .(zip3, c_m), summarise, ILIsum=sum(as.numeric(ILI)), popstatsum=sum(as.numeric(popstat)))
d4_10b=data.frame(cbind(season=rep("10", dim(d4_10a)[1]), c_m=d4_10a$c_m, zip3=d4_10a$zip3, ILIsum=d4_10a$ILIsum, popstatsum=d4_10a$popstatsum), stringsAsFactors = FALSE)

# 6/14 bind data together again
d4cl2<-rbind(d4_1b, d4_2b, d4_3b, d4_4b, d4_5b, d4_6b, d4_7b, d4_8b, d4_9b, d4_10b)
dfsumm(d4cl2)

### export cleaned data in whole and by season ###
write.csv(d4cl2, file="zipcode_bysseas_cl_v6-12-13.csv", row.names=FALSE)
write.csv(d4_1b, file="zipcode_cl_1v6-12-13.csv", row.names=FALSE)
write.csv(d4_2b, file="zipcode_cl_2v6-12-13.csv", row.names=FALSE)
write.csv(d4_3b, file="zipcode_cl_3v6-12-13.csv", row.names=FALSE)
write.csv(d4_4b, file="zipcode_cl_4v6-12-13.csv", row.names=FALSE)
write.csv(d4_5b, file="zipcode_cl_5v6-12-13.csv", row.names=FALSE)
write.csv(d4_6b, file="zipcode_cl_6v6-12-13.csv", row.names=FALSE)
write.csv(d4_7b, file="zipcode_cl_7v6-12-13.csv", row.names=FALSE)
write.csv(d4_8b, file="zipcode_cl_8v6-12-13.csv", row.names=FALSE)
write.csv(d4_9b, file="zipcode_cl_9v6-12-13.csv", row.names=FALSE)
write.csv(d4_10b, file="zipcode_cl_10v6-12-13.csv", row.names=FALSE)

#### 6/14 check outliers in script: OR_urbanmetro_v6-14-13.py ####
## Season 7, zip3 363 has an OR near 100
d2_7[d2_7$zip3=='363',] ## very low ILI for adults
d[d$zip3=='363',] ## this trend is observed in the original dataset across all seasons (very few adult ILI cases relative to children ILI cases)
## Examine a few of the zip3s that are visual outliers in the OR_RUCC2013bin_v6-14-13 charts
d[d$zip3=='142',] # Buffalo, NY: relatively low child attack rates
d[d$zip3=='084',] # Atlantic City, NJ: small ILI counts across the board so variations make more of an impact
d[d$zip3=='363',] # Dothan, AL: relatively low child attack rates but also small ILI counts
d[d$zip3=='159',] # Johnstown, PA: low ILI counts, not represented in every season

#### 6/14 debug OR_vaxmatch_v6-12-13.py ####
# line 229, list index out of range at season 6
table(d4cl2$season)
dim(d4cl2)
d4_6b[1:100,]
dfsumm(d4_6b)
dfsumm(d4cl2)
d4_6b[d4_6b$ILIsum=='0',]