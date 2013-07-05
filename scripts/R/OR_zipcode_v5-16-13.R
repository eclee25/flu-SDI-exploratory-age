
## Name: Elizabeth Lee
## Date: 6/7/13
## Function: 
### 1. delete season 0 data
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
d<-read.csv('zipcode_bysseas.csv', header=FALSE, col.names=c('season','c_m','zip3','ILI','popstat'), colClasses='character')

## program
#remove season 0s
d1<-d[!(d$season=='0'),]
dim(d[d$season=='0',]) # 2654 5 # number of rows removed matches number of season 0 rows
dim(d1) # 26022 5
dim(d) # 28676 5
# separate these into different datasets
d1_1<-d1[d1$season=='1',]
d1_2<-d1[d1$season=='2',]
d1_3<-d1[d1$season=='3',]
d1_4<-d1[d1$season=='4',]
d1_5<-d1[d1$season=='5',]
d1_6<-d1[d1$season=='6',]
d1_7<-d1[d1$season=='7',]
d1_8<-d1[d1$season=='8',]
d1_9<-d1[d1$season=='9',]
d1_10<-d1[d1$season=='10',]

# within each season, remove the zip3s that don't have A & C data
# drop all "O" data
d2<-d1[!(d1$c_m=="O"),]
dim(d2) # 17311 5
dim(d1) # 26022 5
dim(d1[d1$c_m=="O",]) # 8711 5 # number of rows removed matches number of "O" rows

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
d2_1nage<-ddply(.data=d2_1, .variables='zip3', summarise, nagegrp=length(c_m)) # number of age groups for each zip3 (0 to 2 only)
d2_1mz<-d2_1nage[d2_1nage$nagegrp<2,1] #list of zip3s that need to be removed
d2_2nage<-ddply(.data=d2_2, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_2mz<-d2_2nage[d2_2nage$nagegrp<2,1]
d2_3nage<-ddply(.data=d2_3, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_3mz<-d2_3nage[d2_3nage$nagegrp<2,1]
d2_4nage<-ddply(.data=d2_4, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_4mz<-d2_4nage[d2_4nage$nagegrp<2,1]
d2_5nage<-ddply(.data=d2_5, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_5mz<-d2_5nage[d2_5nage$nagegrp<2,1]
d2_6nage<-ddply(.data=d2_6, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_6mz<-d2_6nage[d2_6nage$nagegrp<2,1]
d2_7nage<-ddply(.data=d2_7, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_7mz<-d2_7nage[d2_7nage$nagegrp<2,1]
d2_8nage<-ddply(.data=d2_8, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_8mz<-d2_8nage[d2_8nage$nagegrp<2,1]
d2_9nage<-ddply(.data=d2_9, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_9mz<-d2_9nage[d2_9nage$nagegrp<2,1]
d2_10nage<-ddply(.data=d2_10, .variables='zip3', summarise, nagegrp=length(c_m)) 
d2_10mz<-d2_10nage[d2_10nage$nagegrp<2,1]
d2_1mz # 61
d2_2mz # 50
d2_3mz # 34
length(d2_4mz) # 13
length(d2_5mz) # 11
length(d2_6mz) # 12
length(d2_7mz) # 12
length(d2_8mz) # 5
d2_9mz # 2
d2_10mz # 1
# check these in the original d1 data
d1[d1$zip3=='821',]
d2[d2$zip3=='821',]
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

# among the d1 datasets (includes the "Other" agegroup data), subset to include only the zip3s in the d2_#b datasets
d1_1c<-d1_1[(d1_1$zip3 %in% d2_1b), ]
d2_1mz # check that this worked, "033", "637" shouldn't be in d1_1c
d1_1c[d1_1c$zip3=='033',] # empty (check)
d1_1c[d1_1c$zip3=='637',] # empty (check)
d1_1[d1_1$zip3=='033',] # has only C (check)
d1_1[d1_1$zip3=='637',] # has only A (check)
# continue this subsetting for each season
d1_2c<-d1_2[(d1_2$zip3 %in% d2_2b), ]
d1_3c<-d1_3[(d1_3$zip3 %in% d2_3b), ]
d1_4c<-d1_4[(d1_4$zip3 %in% d2_4b), ]
d1_5c<-d1_5[(d1_5$zip3 %in% d2_5b), ]
d1_6c<-d1_6[(d1_6$zip3 %in% d2_6b), ]
d1_7c<-d1_7[(d1_7$zip3 %in% d2_7b), ]
d1_8c<-d1_8[(d1_8$zip3 %in% d2_8b), ]
d1_9c<-d1_9[(d1_9$zip3 %in% d2_9b), ]
d1_10c<-d1_10[(d1_10$zip3 %in% d2_10b), ]
d1_10c[d1_10c$zip3=='821',] # check s10, empty (check)

# recombine all of these datasets to have a complete set
d1_cl<-rbind(d1_1c, d1_2c, d1_3c, d1_4c, d1_5c, d1_6c, d1_7c, d1_8c, d1_9c, d1_10c)
dfsumm(d1)
dfsumm(d1_cl)
setdiff(d1$zip3, d1_cl$zip3) # 203 was removed from the dataset
d1[d1$zip3=="203",] # this checks out

# how many "Other" ages are missing?
table(d1_cl$c_m) # 24 are missing

### export cleaned data ###
write.csv(d1_cl, file="zipcode_bysseas_cl.csv", row.names=FALSE)


########################################################
## 6/10/13 additional checks ##
## Rationale: When calculating OR from this data (OR_urbanmetro_v6-7-13.py), it was found that two values of adult ILI attack rates were equal to zero, which prevented the proper calculation of an OR for those two zipcode-seasons. The python indexes were 101 and 104, which should translate into R indexes 102 and 105 among all A values. Check these indexes to ensure that this is true and determine whether it is okay to drop these data points.

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export')
d<-read.csv('zipcode_bysseas_cl.csv', header=TRUE, colClasses='character')
dfsumm(d)
dA<-d[d$c_m=="A",]
dA[100:110,] # indexes 102 and 105 among all adult values have ILI counts of 0
# corresponds to zip3s 133 and 137 (S1 Utica and S1 Binghamton NY)
dA[dA$ILI==0,] # those two zip3-seasons are the only two values with ILI counts of 0
# are there any zip3-seasons where children have ILI counts of 0?
which(dA$ILI==0) # 102 and 105 in adultlist
dC<-d[d$c_m=='C',]
dC[dC$ILI==0,] # S3 zip3=645 (St. Joseph, MO)
which(dC$ILI==0) # 2163 in childlist
## This value should also be dropped or the OR will = 0 for this zip3-season

## three values need to be dropped from the dataset: S1 133, S1 137, and S3 645
which(d$season==1 & d$zip3 == '133') # 301-303
which(d$season==1 & d$zip3 == '137') # 310-312
which(d$season==3 & d$zip3 == '645') # 6468-6470
rmidx<-c(301,302,303,310,311,312,6468,6469,6470)
d[rmidx,]
d2<-d[-rmidx,]
dim(d)
dfsumm(d2)
# did it work? yes
which(d$ILI==0)
which(d2$ILI==0)
d2[which(d2$ILI==0),] # includes only c_m=='O'
write.csv(d2, file="zipcode_bysseas_cl2.csv", row.names=FALSE)

## check values of all zip3s ##
## there was an error where one zip3 was "10" in python
d[d$zip3=='10',] # fixed when changed data import to character

## 6/10/13 split zipcode_bysseas_cl2 data into a dataset per season
## this will enable a chart or a different color on the same chart to be drawn for each season
table(d2$season)
d2s1<-d2[d2$season=='1',]
d2s2<-d2[d2$season=='2',]
d2s3<-d2[d2$season=='3',]
d2s4<-d2[d2$season=='4',]
d2s5<-d2[d2$season=='5',]
d2s6<-d2[d2$season=='6',]
d2s7<-d2[d2$season=='7',]
d2s8<-d2[d2$season=='8',]
d2s9<-d2[d2$season=='9',]
d2s10<-d2[d2$season=='10',]
write.csv(d2s1, file="zipcode_cl2_s1.csv", row.names=FALSE)
write.csv(d2s2, file="zipcode_cl2_s2.csv", row.names=FALSE)
write.csv(d2s3, file="zipcode_cl2_s3.csv", row.names=FALSE)
write.csv(d2s4, file="zipcode_cl2_s4.csv", row.names=FALSE)
write.csv(d2s5, file="zipcode_cl2_s5.csv", row.names=FALSE)
write.csv(d2s6, file="zipcode_cl2_s6.csv", row.names=FALSE)
write.csv(d2s7, file="zipcode_cl2_s7.csv", row.names=FALSE)
write.csv(d2s8, file="zipcode_cl2_s8.csv", row.names=FALSE)
write.csv(d2s9, file="zipcode_cl2_s9.csv", row.names=FALSE)
write.csv(d2s10, file="zipcode_cl2_s10.csv", row.names=FALSE)



