###################################################
## Elizabeth Lee
## Date: 5/31/13
## Function: Manipulate data to create a zipcode to county/FIPS crosswalk
## filenames: 1) zip_code_database.csv, 2) ruralurbancodes2013.csv
## exported data: zip3_RUCC2013.csv

## Data Sources: 
## 1) Free zipcode database from http://www.unitedstateszipcodes.org/zip-code-database/
## 2) USDA ERS rural-urban continuum codes from http://www.ers.usda.gov/data-products/rural-urban-continuum-codes.aspx
## Notes:
# 2013 Rural-Urban Continuum Codes
# Code   Description
# Metro counties:
# 1 	Counties in metro areas of 1 million population or more
# 2 	Counties in metro areas of 250,000 to 1 million population
# 3 	Counties in metro areas of fewer than 250,000 population
# Nonmetro counties:
# 4 	Urban population of 20,000 or more, adjacent to a metro area
# 5 	Urban population of 20,000 or more, not adjacent to a metro area
# 6 	Urban population of 2,500 to 19,999, adjacent to a metro area
# 7 	Urban population of 2,500 to 19,999, not adjacent to a metro area
# 8 	Completely rural or less than 2,500 urban population, adjacent to a metro area
# 9 	Completely rural or less than 2,500 urban population, not adjacent to a metro area
## define 'urban' as being a metro county

# http://www.ers.usda.gov/topics/rural-economy-population/rural-classifications/what-is-rural.aspx#.UbFaoBUUx2M
# Census urban-rural designation is based on land use while USDA ERS classification refers to social and economic change

# 2013 Rural-Urban Continuum Codes, number of counties and population
# Code   Number of counties 	2010 population
# Metro 	1,167 	262,452,132
# 1 	    432 	  168,523,961
# 2 	    379   	65,609,956
# 3 	    356   	28,318,215
# Nonmetro 	1,976 	46,293,406
# 4 	    214   	13,538,322
# 5 	    92 	    4,953,810
# 6 	    593   	14,784,976
# 7 	    433   	8,248,674
# 8 	    220   	2,157,448
# 9 	    424   	2,610,176
# U.S. total 	3,143 	308,745,538
###################################################
setwd('/home/elee/Downloads')

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

zcd<-read.csv('zip_code_database.csv',  header=T, colClasses = c(zip='character', county='factor'), na.strings = "")
ers<-read.csv('ruralurbancodes2013.csv', header=T, colClasses = c(County_Name='factor', FIPS='character'))

zcd$county<-tolower(zcd$county) # all lower case
ers$County_Name<-tolower(ers$County_Name)
length(unique(zcd$county)) # 1914 counties
length(unique(ers$County_Name)) # 1954 counties

zcd_cnty<-sort(unique(zcd$county))
ers_cnty<-sort(unique(ers$County_Name))

cbind(zcd_cnty[1:10],ers_cnty[1:10]) # some differences

# drop data for each dataset that corresponds to territories
sort(unique(zcd$state)) #what uq states?
# AA, AE, AP, AS, FM, GU, MH, MP, PR, PW, VI
terr<-c('AA','AE','AP','AS','FM','GU','MH','MP','PR','PW','VI')
zcd2<-zcd[!(zcd$state %in% terr),]
zcd2$state<-factor(zcd2$state)
sort(unique(ers$State))
ers2<-ers[!(ers$State %in% terr),]
ers2$State<-factor(ers2$State)

# check counties again
zcd_cnty<-sort(unique(zcd2$county))
ers_cnty<-sort(unique(ers2$County_Name))
cbind(zcd_cnty[1:100],ers_cnty[1:100])
cbind(zcd_cnty[101:200],ers_cnty[101:200])
cbind(zcd_cnty[1200:1476],ers_cnty[1200:1476])
# still diff numbers
match<-intersect(zcd2$county, ers2$County_Name)
notmatch<-setdiff(zcd2$county, ers2$County_Name)
sts<-match[grep("st", match)]

# remove punctuation characters
zcd2$county<-gsub('[[:punct:]]','', zcd2$county)
ers2$County_Name<-gsub('[[:punct:]]','', ers2$County_Name)
match<-intersect(zcd2$county, ers2$County_Name)
notmatch<-setdiff(zcd2$county, ers2$County_Name)
length(unique(zcd2$county)) #1880 (excluding NA)
length(unique(ers2$County_Name)) #1876

# check data where county = NA # decommissioned zipcodes
NAdata<-zcd2[zcd2$county=='NA',] #it appears to be completely empty -- turns out it is decommissioned data
nas<-zcd2[is.na(zcd2$county),]
# drop this data
zcd3<-zcd2[!is.na(zcd2$county),]

# create a new cleaned county var for both datasets and clean the rest of the data in notmatch
zcd3$county_cl<-zcd3$county
ers2$county_cl<-ers2$County_Name

notmatch<-setdiff(zcd3$county, ers2$County_Name)
#[1] "coas county"
sort(ers2[agrep("coas county", ers2$County_Name, max.distance=0.1),3])
zcd3[zcd3$county=='coãs county',] # rowindex 1149 and 1154, 03589 and 03597 zipcodes; aka 'coos county'
ers2[ers2$County_Name=='coos county',] # verified that coos and coãs are in the same state and area
zcd3$county_cl[zcd3$county_cl=='coãs county']<-'coos county'
zcd3[zcd3$county_cl=='coos county',]
ers2[ers2$county_cl=='coos county',]
#[2] "james city"
sort(ers2[agrep("james city", ers2$County_Name, max.distance=0.1),3]) # james city (zcd) - james city county (ers)? 
zcd3[zcd3$county=='james city',]
zcd3[zcd3$county=='james city county',] # looks the same as james city in zcd3
ers2[ers2$County_Name=='james city county',] # verifed that james city==james city county
zcd3$county_cl[zcd3$county_cl=='james city']<-'james city county'
zcd3[zcd3$county_cl=='james city county',]
ers2[ers2$county_cl=='james city county',]
#[3] "charles city"
sort(ers2[agrep("charles city", ers2$County_Name, max.distance=0.1),3]) # charles city (zcd) - charles city county (ers)? 
zcd3[zcd3$county=='charles city',]
zcd3[zcd3$county=='charles city county',] # looks the same as charles city in zcd3
ers2[ers2$County_Name=='charles city',]
ers2[ers2$County_Name=='charles city county',] # verified
zcd3$county_cl[zcd3$county=='charles city']<-'charles city county'
zcd3[zcd3$county_cl=='charles city county',]
ers2[ers2$county_cl=='charles city county',]
#[4] "de kalb county"
sort(ers2[agrep("de kalb county", ers2$County_Name, max.distance=0.1),3]) # de kalb county (zcd) = dekalb county (ers)?
zcd3[zcd3$county=='de kalb county',] # located in TN, IN # should remove the spaces, verified
zcd3[zcd3$county=='dekalb county',] # located in GA, AL, IL, MO
ers2[ers2$County_Name=='dekalb county',] # AL, GA, IL, IN, MO, TN 
zcd3$county_cl[zcd3$county=='de kalb county']<-'dekalb county'
zcd3[zcd3$county_cl=='dekalb county',]
ers2[ers2$county_cl=='dekalb county',]
#[5] "la porte county"
sort(ers2[agrep("la porte county", ers2$County_Name, max.distance=0.1),3])
zcd3[zcd3$county=='la porte county',] # IN
zcd3[zcd3$county=='laporte county',] # none
ers2[ers2$County_Name=='laporte county',] # located in IN
ers2[ers2$County_Name=='la porte county',] # none
zcd3$county_cl[zcd3$county=='la porte county']<-'laporte county'
zcd3[zcd3$county_cl=='laporte county',]
ers2[ers2$county_cl=='laporte county',]
#[6] "doãa ana county"
sort(ers2[agrep("doãa ana county", ers2$County_Name, max.distance=0.1),3]) # only similar is dona ana county
zcd3[zcd3$county=='doãa ana county',] # must be the n with enye symbol that is read incorrectly
ers2[ers2$County_Name=='dona ana county',]
zcd3[zcd3$county=='dona ana county',]
zcd3$county_cl[zcd3$county=='doãa ana county']<-'dona ana county'
zcd3[zcd3$county_cl=='dona ana county',]
#[7] "anchorage borough" [8] "municipality of anchorage" 
sort(ers2[agrep("anchorage borough", ers2$County_Name, max.distance=0.3),3]) 
ers2[ers2$County_Name=='anchorage municipality',] # anchorage is a city-borough, AK uses boroughs instead of counties
zcd3[zcd3$county=='anchorage borough',] # 995
zcd3[zcd3$county=='anchorage municipality',] # none
zcd3[zcd3$county=='municipality of anchorage',] # 995
ers2[ers2$County_Name=='anchorage municipality',] # verified
zcd3$county_cl[zcd3$county=='anchorage borough']<-'anchorage municipality'
zcd3$county_cl[zcd3$county=='municipality of anchorage']<-'anchorage municipality'
zcd3[zcd3$county_cl=='anchorage municipality',]

## explore AK more ##
sort(unique(ers2[ers2$State=="AK",3])) 
# anchorage municipality, juneau city and borough, hoonahangoon census area ak, 
# petersburg census area, price of wales hyder census area, sitka city and borough, skagway municipality
# wrangell city and borough, yakutat city and borough
sort(unique(zcd3[zcd3$state=="AK",7])) 
# anchorage borough && muncipality of anchorage, city and borough of juneau && juneau borough, hoonahangoon borough
# petersburg borough, prince of walesouter ketchikan borough, sitka borough, skagway borough
# wrangell borough, yakutat borough

#[9] yakutat borough (zcd), yakutat city and borough (ers)
zcd3$county_cl[zcd3$county=='yakutat borough']<-'yakutat city and borough'
zcd3[zcd3$county_cl=='yakutat city and borough',]
ers2[ers2$County_Name=='yakutat city and borough',]
zcd3[zcd3$county=='yakutat city',] # none
#[10] "juneau borough" [11] "city and borough of juneau" (zcd); "juneau city and borough" (ers)
zcd3$county_cl[zcd3$county=='juneau borough']<-'juneau city and borough'
zcd3$county_cl[zcd3$county=='city and borough of juneau']<-'juneau city and borough'
zcd3[zcd3$county=='juneau city',] # none
zcd3[zcd3$county_cl=='juneau city and borough',] # 998
ers2[ers2$county_cl=='juneau city and borough',]

# [12] hoonahangoon borough (zcd); hoonahangoon census area ak (ers)
zcd3[grep('hoonahangoon', zcd3$county),] # hoonahangoon borough is the only related area in zcd3
ers2[grep('hoonahangoon', ers2$County_Name),] # census areas is the only related area in ers
zcd3$county_cl[zcd3$county=='hoonahangoon borough']<-'hoonahangoon census area ak'
zcd3[zcd3$county_cl=='hoonahangoon census area ak',] # 998 (same prefix as juneau but with different fips codes)
ers2[ers2$county_cl=='hoonahangoon census area ak',]
# [13] petersburg borough (zcd); petersburg census area (ers)
ers2[grep('petersburg', ers2$County_Name),] 
zcd3[grep('petersburg', zcd3$county),] 
zcd3$county_cl[zcd3$county=='petersburg borough']<-'petersburg census area'
zcd3[zcd3$county_cl=='petersburg census area',] # 998
ers2[ers2$county_cl=='petersburg census area',] # diff fips code than other 998
# [14] sitka borough (zcd), sitka city and borough (ers)
ers2[grep('sitka', ers2$County_Name),] 
zcd3[grep('sitka', zcd3$county),] 
zcd3$county_cl[zcd3$county=='sitka borough']<-'sitka city and borough'
zcd3[zcd3$county_cl=='sitka borough',] # check that conversion occurred
zcd3[zcd3$county_cl=='sitka city and borough',]
# [15] skagway borough (zcd); skagway municipality (ers)
ers2[grep('skagway', ers2$County_Name),] # check
zcd3[grep('skagway', zcd3$county),] # 998
zcd3$county_cl[zcd3$county=='skagway borough']<-'skagway municipality'
zcd3[zcd3$county_cl=='skagway municipality',]
# [16] prince of walesouter ketchikan borough (zcd); price of wales hyder census area (ers)
ers2[grep('wales', ers2$County_Name),] # check
zcd3[grep('wales', zcd3$county),]
zcd3$county_cl[zcd3$county=='prince of walesouter ketchikan borough']<-'prince of wales hyder census area'
ers2$county_cl[ers2$County_Name=='price of wales hyder census area']<-'prince of wales hyder census area'
ers2[grep('wales', ers2$county_cl),] # check
zcd3[grep('wales', zcd3$county_cl),]
# [17] wrangell borough (zcd); wrangell city and borough (ers)
ers2[grep('wrangell', ers2$County_Name),] # check
zcd3[grep('wrangell', zcd3$county),]
zcd3$county_cl[zcd3$county=='wrangell borough']<-'wrangell city and borough'
zcd3[grep('wrangell', zcd3$county_cl),] # check

length(unique(zcd3$county_cl)) # still a difference of 3
length(unique(ers2$county_cl))
notmatch2<-setdiff(ers2$county_cl, zcd3$county_cl) # 3 items in ers2 not in zcd3

#[1] dewitt county (ers); de witt county (zcd)
ers2[grep('dewitt', ers2$County_Name),] # TX
zcd3[grep('dewitt', zcd3$county),] # none
sort(zcd3[agrep("dewitt county", zcd3$county, max.distance=0.1),7]) 
zcd3[grep('de witt', zcd3$county),] # IL, TX # remove space for both
ers2[grep('de witt', ers2$County_Name),] # IL # remove space for IL
zcd3$county_cl[zcd3$county=='de witt county']<-'dewitt county'
ers2$county_cl[ers2$County_Name=='de witt county']<-'dewitt county'
ers2[grep('dewitt', ers2$county_cl),] # check
zcd3[grep('dewitt', zcd3$county_cl),] # check
#[2] covington city (ers)
zcd3[grep('covington', zcd3$county),] # AL, MS have covington county
ers2[grep('covington', ers2$County_Name),] # AL, MS have covington county, VA has covington city (zip = 24426 according to google maps)
zcd3[zcd3$zip=='24426',] # labeled under alleghany county
ers2[ers2$County_Name=='alleghany county',] # the ers designation appears to be more correct because the area around covington city looks like it is not part of alleghany county in the border drawn in google maps
zcd3[substring(zcd3$zip, 1, 3)=='244',] # includes multiple counties
zcd3$county_cl[zcd3$zip=='24426']<- 'covington city'
zcd3[grep('covington', zcd3$county_cl),]
ers2[grep('covington', ers2$county_cl),]
#[3] lexington city (ers)
zcd3[grep('lexington', zcd3$county),] # lexington county in SC
ers2[grep('lexington', ers2$County_Name),] # lexington county in SC, lexington city in VA (zipcode ==24450, google maps)
ers2[ers2$County_Name=='lexington city',]
zcd3[zcd3$zip=='24450',] # rockbridge county, excludes lexington city
zcd3$county_cl[zcd3$zip=='24450']<-'lexington city'
zcd3[grep('lexington', zcd3$county_cl),]
ers2[grep('lexington', ers2$county_cl),]
# look at nearby buena vista which does not appear to be in rockbridge county either
zcd3[grep('buena vista', zcd3$county),] # listed as buena vista city - must have been changed prior to 2008
ers2[grep('buena vista', ers2$County_Name),] # listed as buena vista city too
# is roanoke an urban area?
ers2[grep('roanoke', ers2$county_cl),] # yes

length(unique(ers2$FIPS)) # 3143
length(unique(zcd3$county_cl)) # 1875
length(unique(ers2$county_cl)) # 1875, but are they equal??
sort(unique(zcd3$county_cl))==sort(unique(ers2$county_cl)) # yes they are equal

zcd3$zip3<-substring(zcd3$zip,1,3) # create zipcode prefix variable

### merge the zcd3 and ers2 datasets ###
# rename the ers2 variables with ers2 at the end of each of the variable names in order to keep track of the data sources of the variables
names(ers2)<-c('FIPS_ers', 'state_ers', 'county_ers', 'pop2010_ers', 'RUCC_2013_ers', 'descrip_RUCC_ers', 'county_cl_ers')
# unique merge IDs can be created from a string that combines the state and county name
zcd3$mergeID<-paste(zcd3$state, zcd3$county_cl) # there won't be different counties of the same name in a single state
ers2$mergeID<-paste(ers2$state_ers, ers2$county_cl_ers)

# why are there 3151 uq mergeIDs in zcd3 and 3143 uq mergeIDs in ers2?
notmatch3<-setdiff(zcd3$mergeID, ers2$mergeID) 
# [1] "PA monongalia county" "PA mahoning county"   "MD mineral county"    "VA mcdowell county"   "WV washington county" "WV martin county"    
[7] "GA cleburne county"   "LA chicot county" 
notmatch4<-setdiff(ers2$mergeID, zcd3$mergeID) # empty vector
# PA monongalia county
ers2[grep('monongalia', ers2$mergeID),] # 15439 == fayette county (zip-codes.com); monongalia county no longer exists in PA (only exists in WV now)
zcd3[grep('monongalia', zcd3$mergeID),] # change from monongalia to fayette county (change county_cl and mergeID)
ers2[ers2$mergeID=='PA fayette county',]
zcd3[zcd3$mergeID=='PA fayette county',] # includes 154 prefixes
zcd3[zcd3$mergeID=='PA monongalia county',]
zcd3$county_cl[zcd3$mergeID=='PA monongalia county']<-'fayette county'
zcd3$mergeID[zcd3$mergeID=='PA monongalia county']<-'PA fayette county'
# PA mahoning county
ers2[grep('mahoning', ers2$mergeID),] # 16140, 16155 == lawrence county (zip-codes.com); mahoning county no longer exists in PA (only exists in OH now)
zcd3[grep('mahoning', zcd3$mergeID),]
ers2[ers2$mergeID=='PA lawrence county',]
zcd3[zcd3$mergeID=='PA lawrence county',] # includes 161 prefixes
zcd3$county_cl[zcd3$mergeID=='PA mahoning county']<-'lawrence county'
zcd3$mergeID[zcd3$mergeID=='PA mahoning county']<-'PA lawrence county'
# MD mineral county
ers2[grep('mineral', ers2$mergeID),] # 21560 == allegany county (zip-codes.com), mineral county no longer in MD
zcd3[grep('mineral', zcd3$mergeID),]
ers2[ers2$mergeID=='MD allegany county',]
zcd3[zcd3$mergeID=='MD allegany county',] # includes 215 prefixes
zcd3$county_cl[zcd3$mergeID=='MD mineral county']<-'allegany county'
zcd3$mergeID[zcd3$mergeID=='MD mineral county']<-'MD allegany county'
# "VA mcdowell county"  
ers2[grep('mcdowell', ers2$mergeID),] # 24619 == tazewell county (zip-codes.com), mcdowell county no longer in VA
zcd3[grep('mcdowell', zcd3$mergeID),]
ers2[ers2$mergeID=='VA tazewell county',]
zcd3[zcd3$mergeID=='VA tazewell county',] # includes 246 prefixes
zcd3$county_cl[zcd3$mergeID=='VA mcdowell county']<-'tazewell county'
zcd3$mergeID[zcd3$mergeID=='VA mcdowell county']<-'VA tazewell county'
# "WV washington county" 
ers2[grep('washington county', ers2$mergeID),] # 25410 == jefferson county (zip-codes.com), washington county no longer in WV
zcd3[grep('WV washington county', zcd3$mergeID),]
ers2[ers2$mergeID=='WV jefferson county',]
zcd3[zcd3$mergeID=='WV jefferson county',] # includes 254 prefixes
zcd3$county_cl[zcd3$mergeID=='WV washington county']<-'jefferson county'
zcd3$mergeID[zcd3$mergeID=='WV washington county']<-'WV jefferson county'
# "WV martin county"    
ers2[grep('martin county', ers2$mergeID),] # 25685 == mingo county (zip-codes.com), washington county no longer in WV
zcd3[grep('WV martin county', zcd3$mergeID),]
ers2[ers2$mergeID=='WV mingo county',]
zcd3[zcd3$mergeID=='WV mingo county',] # includes 256 prefixes
zcd3$county_cl[zcd3$mergeID=='WV martin county']<-'mingo county'
zcd3$mergeID[zcd3$mergeID=='WV martin county']<-'WV mingo county'
# "GA cleburne county" 
ers2[grep('cleburne', ers2$mergeID),] # 30138 == polk county (zip-codes.com), washington county no longer in WV
zcd3[grep('cleburne county', zcd3$mergeID),]
ers2[ers2$mergeID=='GA polk county',]
zcd3[zcd3$mergeID=='GA polk county',] # includes 256 prefixes
zcd3$county_cl[zcd3$mergeID=='GA cleburne county']<-'polk county'
zcd3$mergeID[zcd3$mergeID=='GA cleburne county']<-'GA polk county'
# "LA chicot county" ## investigate 6/5/13 18:02 
ers2[grep('chicot county', ers2$mergeID),] # 71253 == west carroll parish (zip-codes.com), washington county no longer in WV
zcd3[grep('chicot county', zcd3$mergeID),]
ers2[ers2$mergeID=='LA west carroll county',] # none with west carroll county
zcd3[zcd3$mergeID=='LA west carroll county',] # none
ers2[ers2$mergeID=='LA kilbourne',] # none with kilbourne or kilbourne county
zcd3[zcd3$mergeID=='LA kilbourne',] # none with kilbourne or kilbourne county
ers2[grep('west carroll',ers2$mergeID),] # west carroll is a parish, not a county
zcd3[grep('west carroll',zcd3$mergeID),] # other 712 prefixes
zcd3$county_cl[zcd3$mergeID=='LA chicot county']<-'west carroll parish'
zcd3$mergeID[zcd3$mergeID=='LA chicot county']<-'LA west carroll parish'

dfsumm(zcd3) # 3143
dfsumm(ers2) # 3143
sort(unique(zcd3$mergeID))==sort(unique(ers2$mergeID)) # are they equal? yes

# ers data should be right joined to the zcd3 data just in case the same zipcode is in multiple counties; mult zipcodes could theoretically have the same fips code
# but one zipcode prefix could have multiple fips codes and consequently multiple urban/rural designations
zedat<-merge(zcd3, ers2, by.x = 'mergeID', by.y = 'mergeID')
dfsumm(zedat)
zedat$urbanmarker<-0 # 0 == rural, 1 == urban
zedat$urbanmarker[zedat$RUCC_2013_ers==1]<-1
zedat$urbanmarker[zedat$RUCC_2013_ers==2]<-1
zedat$urbanmarker[zedat$RUCC_2013_ers==3]<-1
sum(zedat$urbanmarker) 
table(zedat$RUCC_2013_ers) #check that these were coded correctly

attach(zedat)
# create a new data frame with only the relevant variables
zedat2<-data.frame(mergeID, zip, state_ers, county_cl_ers, zip3, FIPS_ers, pop2010_ers, RUCC_2013_ers, urbanmarker)
#### export data ####
write.csv(zedat2, file="zip3_RUCC2013.csv", row.names=FALSE)

# import a few packages
library(reshape2)
library(plyr)

## show zip3s that have more than 1 FIPS code ##
table(zedat$FIPS) # number of rows associated with each FIPS code
multFIPS<-sort(unique(zedat$FIPS[table(zedat$FIPS)>1])) # 3139; all but 4 FIPS codes have greater than 1 zipcode associated with it
### what is the ddply output giving?
test<-zedat2[1:100,]
ddply(.data=test, .variables='zip3', summarise, numFIPS=length(unique(FIPS_ers)))
unique(test[test$zip3=='995',6]) # 995 has 5 associated FIPS codes in the test dataset
# zip3s with more than 1 FIPS code
multFIPSzip3s<-ddply(.data=zedat2, .variables='zip3', summarise, numFIPS=length(unique(FIPS_ers)))
# number of zip3s with more than 1 FIPS code
length(multFIPSzip3s$numFIPS[multFIPSzip3s$numFIPS>1]) # 699 zip3s with more than 1 FIPS code
zedat2[zedat2$zip3=='996',] # check
zedat2[zedat2$zip3=='796',] # check

## show zip3s that have more than 1 RUCC code ##
multRUCCzip3s<-ddply(.data=zedat2, .variables='zip3', summarise, numRUCC=length(unique(RUCC_2013_ers)))
length(multRUCCzip3s$numRUCC[multRUCCzip3s$numRUCC>1]) # 598 zip3s with more than 1 RUCC code
zedat2[zedat2$zip3=='273',] # check (5 RUCC codes)
zedat2[zedat2$zip3=='274',] # check (1 RUCC code)

# show zip3s that have both urban and rural designations
URzip3s<-ddply(.data=zedat2, .variables='zip3', summarise, both=length(unique(urbanmarker)))
length(URzip3s$both[URzip3s$both>1]) # 427 zip3s with more both an urban and rural designation
zedat2[zedat2$zip3=='510',] # check (urban and rural)
zedat2[zedat2$zip3=='504',] # check (one only)

# 427 of 910 zipcode prefixes have both urban and rural designations according to the metro/nonmetro designations
# which RUCC codes with both urban and rural designations are likely to be associated with each other?
# subset zedat2 data where the zip3 has both urban and rural designations
URs<-URzip3s$zip3[URzip3s$both>1] # grab list of zip3s that have both urban and rural designations
URs<-factor(URs) # drop factor levels that are not present
ze_UR<-zedat2[zedat2$zip3 %in% URs,] # subset zedat2 data where the zipcodes have both urban and rural designations
ze_UR$zip3<-factor(ze_UR$zip3) # drop zip3 factor levels that are not present

# # reshape the data to wide format where each zip3 is a single row and RUCC codes are columns and data is indicator of which codes are associated with each zip3
# table(ze_UR$zip3, ze_UR$RUCC_2013_ers) # represents count of fips codes by RUCC code for each zip3
# ze_UR[ze_UR$zip3=='013',]# check (31 rows, RUCCs == 2, 3, 4) yes

# take the average of the RUCC codes within a single zip3
ze_avgRUCC<-ddply(.data=zedat2, .variables='zip3', summarise, RUCC_mn=mean(RUCC_2013_ers))
hist(ze_avgRUCC$RUCC_mn, breaks=9)
# spot check some of the zip3s to see if 1-3, 4-6, 7-9 designations might work
zedat2[zedat2$zip3=='981',] # 1.02, 1s and 2s
zedat2[zedat2$zip3=='999',] # 8.69, 7s and 9s
zedat2[zedat2$zip3=='995',] # 5.6, anchorage + surrounding, 2, 7, 9
zedat2[zedat2$zip3=='225',] # 5.3, 1, 6, 9 because it includes areas outside Richmond
zedat2[zedat2$zip3=='232',] # richmond, va ==1
zedat2[zedat2$zip3=='224',] # 4.6, near Fredericksburg and Richmond
zedat2[zedat2$zip3=='245',] # 3.5, 2, 3, 4, 6, 7

# check 225 less populous areas categorized as 1?
zcd3[zcd3$zip3=='225',]
ers2[ers2$mergeID=='VA stafford county',]
ers2[ers2$mergeID=='VA richmond county',]
ers2[ers2$mergeID=='VA westmoreland county',]

# seems reasonable to use RUCC averages for the zip3s
zedat3<-merge(zedat2, ze_avgRUCC, by.x='zip3', by.y='zip3')
zedat3$RUCCavg_m<-0
zedat3$RUCCavg_m[zedat3$RUCC_mn<3]<-1
zedat3$RUCCavg_m[(zedat3$RUCC_mn<6) & (zedat3$RUCC_mn>=3)]<-2
zedat3$RUCCavg_m[(zedat3$RUCC_mn>=6)]<-3

# export data
write.csv(zedat3, file="zip3_RUCC2013avg.csv", row.names=FALSE)

# there is going to be a problem where a single zipcode prefix will correspond to multiple fips codes and the fips codes will have different urban/rural classifications
# zipcodes refer to 2008 county names in zcd database.. slightly older than the usda ers data by fips code so it will not be exact

