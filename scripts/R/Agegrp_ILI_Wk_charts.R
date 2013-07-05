##############################################
###R template
###Author: Elizabeth Lee
###Date: 9/21/12	
###Function: clean and cast data to look at information by age group by year for the symptoms of interest. draw bar plots of information.
###Import data: Agegrp_ILI_Wk.csv (9/20/12: 4:16:36 PM EDT)
###Outputs: Any_cts_wk.ps, ILI_cts_wk.ps, Prop_cts_wk.ps

###Command Line: R
##############################################

### packages ###
library(reshape)
library(RColorBrewer)

### functions ###

### data structures ###

### import data ###
data<-read.csv('Agegrp_ILI_Wk.csv', colClasses='character')
colnames(data)<-c('AGEGROUP', 'WEEK', 'sum_ILI_m', 'sum_ANY_DIAG_VISIT_CT', 'ILI_prop')

### figure template ###
agecol<-brewer.pal(12,"Set3")
yrcol<-brewer.pal(11, "Spectral")
weeknum<-seq(1,496)
agelab<-c("<2 YEARS", "2-4 YEARS", "5-9 YEARS", "10-14 YEARS", "15-19 YEARS", "20-29 YEARS", "30-39 YEARS", "40-49 YEARS", "50-59 YEARS", "60-69 YEARS", "70-79 YEARS", ">80 YEARS")

### program ###
#rm TOTAL agegroup data
data2<-data[data$AGEGROUP!="TOTAL",]

#reshape data for barplot format
colnames(data2)<-c("AGEGROUP", "WEEK", "value", "sum_ANY_DIAG_VISIT_CT", "ILI_prop")
ILI<-data.frame(cast(data2, WEEK~AGEGROUP))
ILI2<-apply(ILI[,2:13],2,as.numeric)
rownames(ILI2)<-ILI[,1]

colnames(data2)<-c("AGEGROUP", "WEEK", "sum_ILI_m", "value", "ILI_prop")
Any<-data.frame(cast(data2, WEEK~AGEGROUP))
Any2<-apply(Any[,2:13],2,as.numeric)
rownames(Any2)<-ILI[,1]

colnames(data2)<-c("AGEGROUP", "WEEK", "sum_ILI_m", "sum_ANY_DIAG_VISIT_CT", "value")
Prop<-data.frame(cast(data2, WEEK~AGEGROUP))
Prop2<-apply(Prop[,2:13],2,as.numeric)
rownames(Prop2)<-ILI[,1]

####### module to bin by different age groups (10/15/12) ######
#charts are not drawn in R
YRS.5.19<-cbind(ILI2[,1:2],ILI2[,9])
X.5.19.YEARS<-apply(YRS.5.19,1,sum,na.rm=TRUE)
YRS.30.49<-ILI2[,6:7]
X.30.49.YEARS<-apply(YRS.30.49,1,sum,na.rm=TRUE)
YRS.50.69<-cbind(ILI2[,8],ILI2[,10])
X.50.69.YEARS<-apply(YRS.50.69,1,sum,na.rm=TRUE)
YRS.70.plus<-ILI2[,11:12]
X.70.plus.YEARS<-apply(YRS.70.plus,1,sum,na.rm=TRUE)
ILI3<-data.frame(X.2.YEARS=ILI2[,5], X.2.4.YEARS=ILI2[,4], X.5.19.YEARS=X.5.19.YEARS,X.20.29.YEARS=ILI2[,3], X.30.49.YEARS=X.30.49.YEARS, X.50.69.YEARS=X.50.69.YEARS, X.70.plus.YEARS=X.70.plus.YEARS)
write.csv(t(ILI3), '/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C1.csv')

YRS.5.19<-cbind(Any2[,1:2],Any2[,9])
X.5.19.YEARS<-apply(YRS.5.19,1,sum,na.rm=TRUE)
YRS.30.49<-Any2[,6:7]
X.30.49.YEARS<-apply(YRS.30.49,1,sum,na.rm=TRUE)
YRS.50.69<-cbind(Any2[,8],Any2[,10])
X.50.69.YEARS<-apply(YRS.50.69,1,sum,na.rm=TRUE)
YRS.70.plus<-Any2[,11:12]
X.70.plus.YEARS<-apply(YRS.70.plus,1,sum,na.rm=TRUE)
Any3<-data.frame(X.2.YEARS=Any2[,5], X.2.4.YEARS=Any2[,4], X.5.19.YEARS=X.5.19.YEARS,X.20.29.YEARS=Any2[,3], X.30.49.YEARS=X.30.49.YEARS, X.50.69.YEARS=X.50.69.YEARS, X.70.plus.YEARS=X.70.plus.YEARS)
write.csv(t(Any3), '/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C2.csv')

Prop3<-ILI3/Any3
write.csv(t(Prop3), '/home/elizabeth/Documents/Georgetown/Bansal/SDI/R_export/C3.csv')

#############################################################

#organize data for lineplots (x-axis = week)
ageorder<-c(5,4,9,1,2,3,6,7,8,10,11,12)
ILIbp<-ILI2[,ageorder]/100
Anybp<-Any2[,ageorder]/1000
Propbp<-Prop2[,ageorder]

#draw lineplot over weeks
postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/ILI_cts_wk.ps")
plot(weeknum,ILIbp[,3],type='n', ylab="ILI counts in 100s",xlab="week number (2000-12-31 to 2010-06-27)")
for (i in 1:length(agecol)){
	lines(weeknum,ILIbp[,i], col=agecol[i], cex=3)
}
legend(8,800,agelab, col=agecol, lwd=3)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/Any_cts_wk.ps")
plot(weeknum,Anybp[,9],type='n', ylab="Any Visit counts in 1000s",xlab="week number (2000-12-31 to 2010-06-27)")
for (i in 1:length(agecol)){
	lines(weeknum,Anybp[,i], col=agecol[i], cex=3)
}
legend(9,2600,agelab, col=agecol, lwd=3)
dev.off()

postscript("/home/elizabeth/Documents/Georgetown/Bansal/SDI/graph_outputs/Prop_cts_wk.ps")
plot(weeknum,Propbp[,4],type='n', ylab="ILI as a proportion of all visits", xlab="week number (2000-12-31 to 2010-06-27)")
for (i in 1:length(agecol)){
	lines(weeknum,Propbp[,i], col=agecol[i], cex=3)
}
legend(10, 0.1,agelab, col=agecol, lwd=3)
dev.off()


