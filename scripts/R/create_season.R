
## Name: Elizabeth Lee
## Date: 7/8/13 
## Function: create new season table for sdi database in mysql which appends an additional column that represents the season +/- 6 weeks around the peak week, where 
## Filenames: season2.csv, season3,csv
## Data Source: SDI
## Notes: 
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


setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/SDI_Data/explore/SQL_import')
s2<-read.csv('season2.csv', colClasses='character', header=F)
swk6<-read.csv('season3bad.csv', colClasses='character', header=F) # rightmost column has the correct values for the peak-based season definitions
s2[1:100,1] 
swk6[1:100,1] # dates are in a different format but in the same order
s3<-cbind(s2,swk6[,5])
dfsumm(s3)
head(s3)
s3[1:50,]

write.csv(s3, file='season3.csv', row.names=FALSE, quote=FALSE) # exported with column names but no quotation marks