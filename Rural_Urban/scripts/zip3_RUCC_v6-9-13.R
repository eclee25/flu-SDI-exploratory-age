
## Name: Elizabeth Lee
## Date: 6/9/13 
## Function: simple matrix of unique zip3, state, RUCC 2013 avg, and urban marker
## Export Filenames: zip3_RUCC2013avg_crosswalk.csv (/home/elee/Dropbox/Elizabeth_Bansal_Lab/Rural_Urban)
## Import Filenames: zip3_RUCC2013avg.csv
## Data Source: USDA ERS rural urban continuum codes 2013 (ruralurbancodes2013.csv), zip_code_database.csv (free zipcode database)

## Notes: zip3_RUCC2013avg.csv was created in zip_code_database.R
## Codebook:
#### RUCCavg_m: 1= very populous urban metro area, 2= includes a smaller urban metro area, 3= rural non-metro area
## 


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

####
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/Rural_Urban/R_export') # 10/29/13 changed folder name
og<-read.csv('zip3_RUCC2013avg.csv', header=T, colClasses='character')
dfsumm(og)
og2<-cbind(og$zip3, og$state_ers, og$RUCC_mn, og$RUCCavg_m)
colnames(og2)<-c('zip3', 'state_ers', 'RUCC_mn', 'RUCCavg_m') # zipcode prefix, state of zip3, mean of all rural-urban continuum codes within zipcode prefix, marker of RUCC mean

dfsumm(og2)
head(og2)
og2[100:140,] # spotcheck certain areas; each zip3 has same state, RUCC_mn, and RUCCavg_m?
og2[30000:30100,] # check
cl<-og2[!(duplicated(og2[,1])),] # 910x4
length(unique(og2[,1])) # 910, check
dfsumm(cl)
head(cl)
tail(cl)

## cross check the RUCC zip3s with the zip3s in the SDI dataset for which we will calculate ORs
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/R_export')
sdi<-read.csv('zipcode_bysseas_cl.csv', header=T, colClasses='character')
unique(sdi[,3]) %in% cl[,1] # all are TRUE so everything checks out
cl2<-as.data.frame(cl) 
length(unique(cl2$zip3)) # 910
length(unique(sdi$zip3)) # 885, fewer zip3s in actual dataset
cl3<-cl2[(cl2$zip3 %in% sdi$zip3),]
dfsumm(cl3)
# does cl3 include only zip3s in sdi data?
setdiff(cl3$zip3, sdi$zip3) # empty, check
cl3$zip3<-as.character(cl3$zip3)
dfsumm(sdi)
dfsumm(cl3)
unique(cl3$zip3) == unique(sdi$zip3) # are they sorted in the same order? no - not every zip3 is present for each season of data
write.csv(cl3, row.names=FALSE, file='zip3_RUCC2013avg_crosswalk.csv')

## 6/10/13 
# how many RUCCs are categorized as urban metro - small urban metro - rural?
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/Rural_Urban/R_export')
data<-read.csv('zip3_RUCC2013avg_crosswalk.csv', colClasses='character', header=T)
dfsumm(data)
table(data$RUCCavg_m) # 396 - 322 - 167