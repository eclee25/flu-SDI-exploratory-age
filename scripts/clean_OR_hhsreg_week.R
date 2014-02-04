
## Name: Elizabeth Lee
## Date: 2/1/14
## Function: Clean SDI data so OR can be calculated by HHS regions for each week
### Create two datasets: 1) popstat by season, zip3, agegroup, 2) child and adult ILI cases by week, zip3, agegroup

## Filenames: /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code/cleanedmapdata/Coord3digits.csv, /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/OR_zip3_week.csv, /home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/popstat_zip3_season.csv
## Data Source: 
## Notes: OR_zip3_week.csv and popstat_zip3_season.csv were both exported using OR_zip3_week.sql
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

# import data
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/mapping_code')
states <- read.csv('Coord3digits.csv', colClasses = 'character')
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_export/')
OR <- read.csv('OR_zip3_week.csv', colClasses = 'character', header = FALSE)
pop <- read.csv('popstat_zip3_season.csv', colClasses = 'character', header = FALSE)

# bulk cleaning
names(pop) <- c('season', 'zip3', 'age', 'popstat')
names(OR) <- c('season', 'wk', 'zip3', 'agegroup', 'ILI')
pop$popstat <- as.numeric(pop$popstat)
OR$ILI <- as.numeric(OR$ILI)
OR$wk2 <- as.Date(OR$wk, format = '%Y-%m-%d')

####################################################
## pop data cleaning ##
# clean pop data such that there is a popstat for each zip3 for children and adults
pop$agegroup <- 'E'
pop[pop$age == '5-9 YEARS',]$agegroup <- 'C'
pop[pop$age == '10-14 YEARS',]$agegroup <- 'C'
pop[pop$age == '15-19 YEARS',]$agegroup <- 'C'
pop[pop$age == '20-29 YEARS',]$agegroup <- 'A'
pop[pop$age == '30-39 YEARS',]$agegroup <- 'A'
pop[pop$age == '40-49 YEARS',]$agegroup <- 'A'
pop[pop$age == '50-59 YEARS',]$agegroup <- 'A'

# how many zip3s have all 7 ages for every season? 886-254 = 632
numages <- aggregate(season~zip3, data = pop, length) # 886 zip3s total
dim(numages[numages$season < 70,]) # 254 zip3s do not have all 7 ages in pop
# impose a strict requirement on popstat data availability - include only data where popstat was available for every age group for every season (one could imagine an alternative requirement where data had to be available for every age group for at least one season, and popstat for one age group was applied to multiple season. That OR calculation would be less accurate, however.)
# list of zip3s to remove from pop dataset (and ILI dataset for that matter)
zip3rm <- numages[numages$season < 70,]$zip3 
# rm zip3s that do not have all 7 age groups
pop2 <- pop[!(pop$zip3 %in% zip3rm),]

# aggregate popstat by agegroup by zip3 by season
pop2$uqsza <- paste(pop2$season, pop2$zip3, pop2$agegroup, sep = '')
pop2a <- pop2[pop2$season == '10',]
pop2b <- pop2[pop2$season != '10',]
# S10 data only - pull season, zip3, agegroup from uqsza variable
pop_agga <- aggregate(popstat ~ uqsza, data = pop2a, sum)
pop_agga$season <- substr(pop_agga$uqsza, 1, 2)
pop_agga$zip3 <- substr(pop_agga$uqsza, 3, 5)
pop_agga$agegroup <- substr(pop_agga$uqsza, 6, 6)
# non S10 data - pull season, zip3, agegroup from uqsza variable
pop_aggb <- aggregate(popstat ~ uqsza, data = pop2b, sum)
pop_aggb$season <- paste('0', substr(pop_aggb$uqsza, 1, 1), sep = '')
pop_aggb$zip3 <- substr(pop_aggb$uqsza, 2, 4)
pop_aggb$agegroup <- substr(pop_aggb$uqsza, 5, 5)
# rebind data
pop_agg <- rbind(pop_aggb, pop_agga)

# rewrite uqsza so that it has the same number of characters throughout all seasons
pop_agg2 <- pop_agg
pop_agg2$uqsza <- paste(pop_agg$season, pop_agg$zip3, pop_agg$agegroup, sep = '')

#######################
## clean states data ##
# add leading zeros to zip3 where missing
states$z3cl <- as.numeric(states$zip3)
s1 <- states[states$z3cl < 10,]
s2 <- states[(states$z3cl > 9 & states$z3cl < 100),]
s3 <- states[(states$z3cl > 99),]
s1$z3cl <- paste('00', s1$zip3, sep='')
s2$z3cl <- paste('0', s2$zip3, sep='')
s3$z3cl <- as.character(s3$z3cl)
states2 <- rbind(s1, s2, s3)

# new data frame with only relevant information
states3 <- data.frame(zip3 = states2$z3cl, state = states2$STATE, lat = states2$lat, long = states2$long, stringsAsFactors = FALSE)

#place NAs where lat/long are 0 or blank or where state is blank
s3a <- states3[states3$lat=='0',]
s3a$lat <- NA
s3a$long <-NA
s3b <- states3[!(states3$lat=='0'),]
states4 <- rbind(s3a, s3b)
s4a <- states4[states4$state=='',]
s4a$state <- NA
s4a$lat <- NA
s4a$long <- NA
s4b <- states4[!(states4$state==''),]
states5 <- rbind(s4a, s4b)

# combine pop_agg2 data with state data from coord3digits
pop_agg3 <- merge(pop_agg2, states5, by = 'zip3')

# there are 40 more rows in the merged dataset than in the original pop_agg2 file
# remove duplicates
pop_agg3[duplicated(pop_agg3$uqsza),] # zip3s 063 (500-550) and 967 (12200-12250)
pop_agg3[500:550,] #063 is in CT and NY
pop_agg3[12200:12250,] # 967 is in HI and American Samoa (AS)
# how many other zip3s are Armed services areas? none
pop_agg3[pop_agg3$state == 'AS',] 
# rm AS entries because they are duplicates
pop_agg4 <- pop_agg3[!(pop_agg3$state=='AS'),]
# rm NY entries for zip3 063
pop_agg5 <- pop_agg4[!duplicated(pop_agg4$uqsza),]

######################
## add hhs regions ##
pop_agg5$hhs <- 0
pop_agg5[which(pop_agg5$state == 'CT' | pop_agg5$state == 'ME' | pop_agg5$state == 'MA' | pop_agg5$state == 'NH' | pop_agg5$state == 'RI' | pop_agg5$state == 'VT'),]$hhs <- 1
pop_agg5[which(pop_agg5$state == 'NY' | pop_agg5$state == 'NJ' | pop_agg5$state == 'PR' | pop_agg5$state == 'VI'),]$hhs <- 2
pop_agg5[which(pop_agg5$state == 'DE' | pop_agg5$state == 'DC' | pop_agg5$state == 'MD' | pop_agg5$state == 'PA' | pop_agg5$state == 'VA' | pop_agg5$state == 'WV'),]$hhs <- 3
pop_agg5[which(pop_agg5$state == 'AL' | pop_agg5$state == 'FL' | pop_agg5$state == 'GA' | pop_agg5$state == 'KY' | pop_agg5$state == 'MS' | pop_agg5$state == 'NC' | pop_agg5$state == 'SC' | pop_agg5$state == 'TN'),]$hhs <- 4
pop_agg5[which(pop_agg5$state == 'IL' | pop_agg5$state == 'IN' | pop_agg5$state == 'MI' | pop_agg5$state == 'MN' | pop_agg5$state == 'OH' | pop_agg5$state == 'WI'),]$hhs <- 5
pop_agg5[which(pop_agg5$state == 'AR' | pop_agg5$state == 'LA' | pop_agg5$state == 'NM' | pop_agg5$state == 'OK' | pop_agg5$state == 'TX'),]$hhs <- 6
pop_agg5[which(pop_agg5$state == 'IA' | pop_agg5$state == 'KS' | pop_agg5$state == 'MO' | pop_agg5$state == 'NE'),]$hhs <- 7
pop_agg5[which(pop_agg5$state == 'CO' | pop_agg5$state == 'MT' | pop_agg5$state == 'ND' | pop_agg5$state == 'SD' | pop_agg5$state == 'UT' | pop_agg5$state == 'WY'),]$hhs <- 8
pop_agg5[which(pop_agg5$state == 'AZ' | pop_agg5$state == 'CA' | pop_agg5$state == 'HI' | pop_agg5$state == 'NV' | pop_agg5$state == 'AS' | pop_agg5$state == 'MP' | pop_agg5$state == 'FM' | pop_agg5$state == 'GU' | pop_agg5$state == 'MH' | pop_agg5$state == 'PW'),]$hhs <- 9
pop_agg5[which(pop_agg5$state == 'AK' | pop_agg5$state == 'ID' | pop_agg5$state == 'OR' | pop_agg5$state == 'WA'),]$hhs <- 10

# write data to file: uqsza, popstat, season, zip3, agegroup, state, lat, long, hhsregion
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(pop_agg5, 'popstat_zip3_season_cl.csv', row.names = FALSE) # 2/3/14, 14:41

#######################################################
## OR data cleaning ##
# there are 934 unique zip3s in OR and 886 in pop -- why?
# list of zip3s that are in OR and not in pop
unique(OR$zip3)[!(unique(OR$zip3) %in% unique(pop$zip3))]
# examined a sample of these zip3s in mysql database -- they have 0 for popstat but there were some ILI cases
OR2 <- OR[(OR$zip3 %in% pop$zip3),]

# rm zip3s that did not have all 7 age groups for every season in pop dataset (denominator for OR calculation would be wrong)
OR3 <- OR2[!(OR2$zip3 %in% zip3rm),]
# check that the 632 zip3s are the same in OR3 and pop2
sum(unique(pop2$zip3) %in% unique(OR3$zip3))

# make season variable 2 characters long
OR3$season <- as.numeric(OR3$season)
OR3a <- OR3[OR3$season < 10,]
OR3b <- OR3[OR3$season == 10,]
OR3a$season <- paste('0', OR3a$season, sep='')
OR3b$season <- as.character(OR3b$season)
OR4 <- rbind(OR3a, OR3b)

# write data to file: season, wk-characterformat, zip3, agegroup, ILI, wk-dateformat
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/R_export')
write.csv(OR4, 'OR_zip3_week_cl.csv', row.names = FALSE) # 2/3/14 16:59




