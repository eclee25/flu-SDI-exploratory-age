
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

########################################
# 12/4/14
setwd('/home/elee/R/source_functions')
source("dfsumm.R")
# identifies index of maximum value in a vector
whichMax <- function(vector){
  return (which(vector == max(vector, na.rm=TRUE)))
}
########################################
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
imp <- read.csv('all_cdc_source_data.csv', colClasses = c(rep('character', 3), rep('numeric', 35)), header = TRUE)

preindex <- imp # All data
# preindex <- imp[as.numeric(imp$uqid) > 200039 & as.numeric(imp$uqid) < 201020,] # SDI seasons only

preindex2 <- preindex[as.numeric(preindex$wk) > 39 | as.numeric(preindex$wk) < 18,] # CDC does not collect data for weeks after 17 in certain seasons. for consistency, do not include weeks 18-20 as "flu season" in the index
preindex2$num_pos <- preindex2$num_samples * preindex2$perc_pos/100

## index is not time-dependent; there is one value per season, so this data needs to be aggregated ##
who <- aggregate(cbind(num_pos, num_samples) ~ season, data = preindex2, sum, na.rm = TRUE)
ped <- aggregate(ped_deaths ~ season, data = preindex2, sum, na.rm = TRUE)
hosp_c <- aggregate(hosp_5.17 ~ season, data = preindex2, max, na.rm = TRUE)
hosp_a <- aggregate(hosp_18.49 ~ season, data = preindex2, max, na.rm = TRUE)
hosp_tot <- aggregate(hosp_tot ~ season, data = preindex2, max, na.rm = TRUE)
########################### code not working ######################################
# ## 12/4/14: include peak week p&i mortality portion instead of sum across season ##
# dummy <- preindex2[duplicated(preindex2$pi_only), 20]
# dup2 <- dummy[!is.na(dummy)]
# dim(preindex2[preindex2$pi_only %in% dup2, c(20,14)]) # 12/4/14: 126 pi_mort values are duplicated
# test_agg <- aggregate(pi_only ~ season, data = preindex2, max, na.rm=TRUE)
# test_agg$pi_only %in% dup2 # many are duplicates -- alt solution is to write whichMax funciton
# pkIndexes <- data.frame(aggregate(pi_only ~ season, data = preindex2, whichMax))
# pk_pi_mort <- data.frame(season=rep(NA, 17), pk_pi_mort=rep(NA, 17), pkPiMort_allcoz=rep(NA, 17))
# for (s in -2:14){
#   print (s)
#   dummyData <- preindex2[preindex2$season == s, c(20,14)]
#   if (s == 2){
#     ix <- (pkIndexes[pkIndexes$season == s,2])
#     pk_pi_mort <- dummyData[ix[[1]][2],]
#   } else{
#     ix <- (pkIndexes[pkIndexes$season == s,2])
#     print (ix)
#     pk_pi_mort <- dummyData[ix[[1]],]
#   } 
#   
# }
###########################################################################
## p&i mortality (sum across season) ##
pi_mort <- aggregate(cbind(pi_only, allcoz_all) ~ season, data = preindex2, sum, na.rm = TRUE) 

## 12/4/14 include peak week outpatient ILI proportion instead of sum across season ##
preindex2[duplicated(preindex2$ilitot),28:29] # check for dups
dup <- c(1570, 347, 997, 2417, 3097, 3631, 14031)
preindex2[preindex2$ilitot %in% dup,28:29] # 12/4/14: 7 ILI values are duplicated
pk_ili_inc <- aggregate(ilitot ~ season, data = preindex2, max, na.rm=TRUE) 
pk_ili_inc$ilitot %in% dup # 12/4/14: but they aren't max ilitot values so it's okay to ignore this problem
patients <- preindex2[preindex2$ilitot %in% pk_ili_inc$ilitot,28:29]
pk_ili <- merge(pk_ili_inc, patients, by='ilitot')
names(pk_ili) <- c('pk_ilitot', 'season', 'pkili_patients')
## ILI proportion (sum of ilitot across season) ##
ili <- aggregate(cbind(ilitot, patients) ~ season, data = preindex2, sum, na.rm=TRUE)


# create final metrics that will be used to create index
who$perc_pos <- who$num_pos/who$num_samples*100
pi_mort$prop_pi <-pi_mort$pi_only/pi_mort$allcoz_all
ili$ili_prop <- ili$ilitot/ili$patients
pk_ili$pk_ili_prop <- pk_ili$pk_ilitot/pk_ili$pkili_patients

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
i8 <- merge(i7, hosp_tot, by = 'season', all.y = TRUE, all.x = TRUE)
i5 <- merge(i8, pk_ili, by = 'season', all.y = TRUE, all.x = TRUE)


# rearrange data to include only values used to make index
index <- data.frame(season = i5$season, perc_pos = i5$perc_pos, prop_pi = i5$prop_pi, ped_deaths = i5$ped_deaths, ili_prop = i5$ili_prop, hosp_5.17 = i5$hosp_5.17, hosp_18.49 = i5$hosp_18.49, hosp_tot = i5$hosp_tot, pk_ili_prop = i5$pk_ili_prop)

# plot formatting
slabels <- c('00-1', '01-2', '02-3', '03-4', '04-5', '05-6', '06-7', '07-8', '08-9', '09-10')
slabels2 <- c('01-2', '02-3', '03-4', '04-5', '05-6', '06-7', '07-8', '08-9')

########################################################################
# excess pi add-on
i6 <- merge(i5, newpi_mort_sub, by='season', all.y=TRUE, all.x=TRUE)
index_excess <- data.frame(season = i6$season, perc_pos = i6$perc_pos, prop_pi = i6$prop_pi, ped_deaths = i6$ped_deaths, ili_prop = i6$ili_prop, hosp_5.17 = i6$hosp_5.17, hosp_18.49 = i6$hosp_18.49, hosp_tot = i6$hosp_tot, excess_pi_deaths=i6$excess_pi_deaths, pk_ili_prop = i6$pk_ili_prop)

## 12/4/14: export with pk_ili_prop 
setwd('/home/elee/Dropbox/Elizabeth_Bansal_Lab/CDC_Source/Import_Data')
write.csv(index_excess, 'cdc_severity_measures_hospMort_nat.csv', row.names=FALSE)
