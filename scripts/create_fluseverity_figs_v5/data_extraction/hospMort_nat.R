
## Name: Elizabeth Lee
## Date: 11/11/14
## Function: create CDC dataset for national level figure 5 (sigma_r vs. total hosp rate/deaths)
## Filenames: Import_Data/all_cdc_source_data.csv
## Data Source: multiple CDC sources (see Source_Data folder)
## Notes: 
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


setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
imp <- read.csv('all_cdc_source_data.csv', colClasses = c(rep('character', 3), rep('numeric', 35)), header = TRUE)
preindex <- imp[as.numeric(imp$uqid) > 200039 & as.numeric(imp$uqid) < 201020,] 
preindex2 <- preindex[as.numeric(preindex$wk) > 39 | as.numeric(preindex$wk) < 18,] # CDC does not collect data for weeks after 17 in certain seasons. for consistency, do not include weeks 18-20 as "flu season" in the index
preindex2$num_pos <- preindex2$num_samples * preindex2$perc_pos/100

# index is not time-dependent; there is one value per season, so this data needs to be aggregated
who <- aggregate(cbind(num_pos, num_samples) ~ season, data = preindex2, sum, na.rm = TRUE)
pi_mort <- aggregate(cbind(pi_only, allcoz_all) ~ season, data = preindex2, sum, na.rm = TRUE) 
ped <- aggregate(ped_deaths ~ season, data = preindex2, sum, na.rm = TRUE)                    
ili <- aggregate(cbind(ilitot, patients) ~ season, data = preindex2, sum, na.rm = TRUE)
hosp_c <- aggregate(hosp_5.17 ~ season, data = preindex2, max, na.rm = TRUE)
hosp_a <- aggregate(hosp_18.49 ~ season, data = preindex2, max, na.rm = TRUE)
hosp_tot <- aggregate(hosp_tot ~ season, data = preindex2, max, na.rm = TRUE)

# create final metrics that will be used to create index
who$perc_pos <- who$num_pos/who$num_samples*100
pi_mort$prop_pi <-pi_mort$pi_only/pi_mort$allcoz_all
ili$ili_prop <- ili$ilitot/ili$patients

########################################################################
### module ###
# 8/28/14 try excess P&I mortality (above baseline/expected) from Matt
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/from_Matt')
excesspi <- read.csv('p_i.csv', colClasses='numeric', header=TRUE)
names(excesspi) <- c('year', 'week', 'perc_ILI_mort', 'expected_BL', 'threshold', 'total_deaths', 'p_deaths', 'i_deaths')
excesspi$pi_deaths <- excesspi$p_deaths + excesspi$i_deaths
excesspi$expected_pi_deaths <- excesspi$expected_BL/100 * excesspi$total_deaths
excesspi$excess_pi_deaths <- excesspi$pi_deaths - excesspi$expected_pi_deaths
# add season variable for flu weeks
excesspi$season <- 0
yr1s <- which(excesspi$week >= 40 & excesspi$week <=53)
season_yr1s <- as.numeric(substr(excesspi[yr1s,]$year, 3, 4)) + 1 # season number is 2nd year of flu season
excesspi[yr1s,]$season <- season_yr1s
yr2s <- which(excesspi$week >=1 & excesspi$week <=20)
season_yr2s <- as.numeric(substr(excesspi[yr2s,]$year, 3, 4))
excesspi[yr2s,]$season <- season_yr2s

# aggregate to season level
newpi_mort <- aggregate(excess_pi_deaths ~ season, data=excesspi, sum, na.rm=TRUE)
newpi_mort_sub <- newpi_mort[newpi_mort$season >=2 & newpi_mort$season <=9,]
########################################################################

# merge data
i1 <- merge(who, pi_mort, by = 'season', all.y = TRUE, all.x = TRUE)
i2 <- merge(i1, ped, by = 'season', all.y = TRUE, all.x = TRUE)
i3 <- merge(i2, ili, by = 'season', all.y = TRUE, all.x = TRUE)
i4 <- merge(i3, hosp_c, by = 'season', all.y = TRUE, all.x = TRUE)
i7 <- merge(i4, hosp_a, by = 'season', all.y = TRUE, all.x = TRUE)
i5 <- merge(i7, hosp_tot, by = 'season', all.y = TRUE, all.x = TRUE)

# rearrange data to include only values used to make index
index <- data.frame(season = i5$season, perc_pos = i5$perc_pos, prop_pi = i5$prop_pi, ped_deaths = i5$ped_deaths, ili_prop = i5$ili_prop, hosp_5.17 = i5$hosp_5.17, hosp_18.49 = i5$hosp_18.49, hosp_tot = i5$hosp_tot)

# plot formatting
slabels <- c('00-1', '01-2', '02-3', '03-4', '04-5', '05-6', '06-7', '07-8', '08-9', '09-10')
slabels2 <- c('01-2', '02-3', '03-4', '04-5', '05-6', '06-7', '07-8', '08-9')

########################################################################
# excess pi add-on
i6 <- merge(i5, newpi_mort_sub, by='season', all.y=TRUE, all.x=TRUE)
index_excess <- data.frame(season = i6$season, perc_pos = i6$perc_pos, prop_pi = i6$prop_pi, ped_deaths = i6$ped_deaths, ili_prop = i6$ili_prop, hosp_5.17 = i6$hosp_5.17, hosp_18.49 = i6$hosp_18.49, hosp_tot = i6$hosp_tot, excess_pi_deaths=i6$excess_pi_deaths)

setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
write.csv(i6, 'cdc_severity_measures_hospMort_nat.csv', row.names=FALSE)
